#!/usr/bin/env python3
"""
Cluster Membership Determination using Caustic Method

This script determines cluster membership for A2199 galaxies using
the caustic method (CausticSNUpy package):
1. Loads master catalog with combined redshifts (z_tot_z)
2. Converts redshifts to velocities
3. Runs caustic analysis to identify cluster members
4. Saves caustic parameters
5. Adds membership flags to catalog

Input files:
    - A2199_mastercat_intermediate_file0.csv (merged catalog with z_tot_z)
    - ../AllHeCS_VAC_updated.csv (cluster properties)

Output files:
    - A2199_caustics.csv (caustic envelope parameters)
    - A2199_mastercat_intermediate_file1.csv (catalog with membership)

Requirements:
    pip install causticsnupy astropy pandas numpy

Author: Jongin Park
Date: 2026
"""

import numpy as np
import pandas as pd
from astropy import constants as const
from astropy.cosmology import LambdaCDM
from causticsnupy.caustics import run_from_array

# Set cosmology (H0=70, Omega_m=0.3, Omega_Lambda=0.7)
cosmo = LambdaCDM(H0=70, Om0=0.3, Ode0=0.7)


def redshift_to_radial_velocity(z):
    """
    Convert redshift to radial velocity using v = cz approximation.
    
    Valid for low redshifts (z < 0.1).
    
    Parameters
    ----------
    z : float or array
        Redshift
    
    Returns
    -------
    float or array
        Radial velocity in km/s
    """
    return z * const.c.to('km/s').value


def load_data(cluster_name='A2199'):
    """
    Load master catalog and cluster properties.
    
    Parameters
    ----------
    cluster_name : str, optional
        Target cluster name (default: 'A2199')
    
    Returns
    -------
    tuple
        (df_main, df_sample, cluster_params)
    """
    print("="*70)
    print(f"LOADING DATA FOR {cluster_name}")
    print("="*70)
    
    # Load AllHeCS VAC for cluster properties
    print("\n1. Loading cluster properties...")
    allhecs = pd.read_csv('../AllHeCS_VAC_updated.csv')
    cluster_info = allhecs[allhecs['CLID'] == cluster_name].iloc[0]
    
    print(f"   → Cluster: {cluster_name}")
    print(f"   → Redshift: {cluster_info['Z']:.6f}")
    print(f"   → RA: {cluster_info['RA']:.6f} deg")
    print(f"   → Dec: {cluster_info['DEC']:.6f} deg")
    
    # Load master catalog
    print("\n2. Loading master catalog...")
    df_main = pd.read_csv('A2199_mastercat_intermediate_file3_kcorrection.csv')
    print(f"   → Total objects: {len(df_main):,}")
    
    # Filter for objects with valid redshifts
    df_sample = df_main[df_main['z_tot_z'] != -9].copy()
    print(f"   → Objects with redshift: {len(df_sample):,}")
    
    # Convert redshift to velocity
    print("\n3. Converting redshifts to velocities...")
    df_sample['VEL'] = df_sample['z_tot_z'].apply(redshift_to_radial_velocity)
    df_sample = df_sample[df_sample['VEL'] > 0]
    print(f"   → Objects with positive velocity: {len(df_sample):,}")
    
    # Extract cluster parameters
    cluster_params = {
        'z': cluster_info['Z'],
        'ra': cluster_info['RA'],
        'dec': cluster_info['DEC'],
        'vel': redshift_to_radial_velocity(cluster_info['Z'])
    }
    
    print(f"\nCluster velocity: {cluster_params['vel']:.1f} km/s")
    
    return df_main, df_sample, cluster_params


def run_caustic_analysis(df_sample, cluster_params):
    """
    Run caustic method for membership determination.
    
    Parameters
    ----------
    df_sample : pd.DataFrame
        Galaxy sample with redshifts and positions
    cluster_params : dict
        Cluster properties (z, ra, dec, vel)
    
    Returns
    -------
    result
        CausticSNUpy result object
    """
    print("\n" + "="*70)
    print("RUNNING CAUSTIC ANALYSIS")
    print("="*70)
    
    # Caustic analysis parameters
    v_lower = 4000   # Lower velocity limit (km/s)
    v_upper = 14000  # Upper velocity limit (km/s)
    v_max = 15000    # Maximum l.o.s. velocity for diagram
    r_max = 4        # Maximum projected distance (Mpc)
    
    # Cosmology parameters
    H0 = cosmo.H0.value
    Om0 = cosmo.Om0
    Ode0 = cosmo.Ode0
    Tcmb0 = cosmo.Tcmb0.value
    
    # Grid resolution parameters
    q = 100
    r_res = 100      # Resolution of radius grid
    v_res = 100      # Resolution of velocity grid
    BT_thr = "ALS"   # Binary Tree threshold
    center_given = False  # Calculate center from data
    
    print(f"\nParameters:")
    print(f"  Velocity range: {v_lower} - {v_upper} km/s")
    print(f"  Max radius: {r_max} Mpc")
    print(f"  Grid resolution: r={r_res}, v={v_res}")
    print(f"  Center given: {center_given}")
    
    # Extract galaxy coordinates and velocities
    ra_gal = np.array(df_sample['p_ra'])
    dec_gal = np.array(df_sample['p_dec'])
    v_gal = np.array(df_sample['VEL'])
    
    # Cluster center
    ra_cl = cluster_params['ra']
    dec_cl = cluster_params['dec']
    v_cl = cluster_params['vel']
    
    print(f"\nRunning CausticSNUpy on {len(df_sample):,} galaxies...")
    print("(This may take 1-2 minutes...)\n")
    
    # Run caustic analysis
    result = run_from_array(
        ra_gal=ra_gal,
        dec_gal=dec_gal,
        v_gal=v_gal,
        ra_cl=ra_cl,
        dec_cl=dec_cl,
        v_cl=v_cl,
        v_lower=v_lower,
        v_upper=v_upper,
        v_max=v_max,
        r_max=r_max,
        center_given=center_given,
        H0=H0,
        Om0=Om0,
        Ode0=Ode0,
        Tcmb0=Tcmb0,
        q=q,
        r_res=r_res,
        v_res=v_res
    )
    
    # Print results
    n_members = result.member.sum()
    print(f"\n{'='*70}")
    print("CAUSTIC ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nResults:")
    print(f"  Total members identified: {n_members:,} / {len(df_sample):,}")
    print(f"  Membership fraction: {n_members/len(df_sample)*100:.1f}%")
    
    if hasattr(result, 'sigma_v') and result.sigma_v is not None:
        print(f"  Velocity dispersion: {result.sigma_v:.1f} km/s")
    
    return result


def save_caustic_parameters(result):
    """
    Save caustic envelope parameters to CSV.
    
    Parameters
    ----------
    result
        CausticSNUpy result object
    """
    print("\n" + "="*70)
    print("SAVING CAUSTIC PARAMETERS")
    print("="*70)
    
    # Extract caustic parameters
    r_grid = result.r_grid  # Radius grid (Mpc)
    A = result.A            # Amplitude of caustics (km/s)
    
    # Convert radius to arcminutes
    # Note: r_grid is in Mpc, need to convert using angular diameter distance
    from astropy import constants as const

    # Speed of light
    c = const.c.to('km/s').value  # 299792.458 km/s

    # Calculate cluster redshift from velocity
    z_cluster = result.v_cl / c
    d_A = cosmo.angular_diameter_distance(z_cluster).value  # Mpc
    r_grid_arcmin = np.degrees(r_grid / d_A) * 60  # arcmin
    
    # Create DataFrame
    df_caustics = pd.DataFrame({
        'r': r_grid,              # Radius in Mpc
        'r_arcmin': r_grid_arcmin, # Radius in arcmin
        'A_upper': A,             # Upper caustic envelope
        'A_lower': -A             # Lower caustic envelope
    })
    
    # Save to CSV
    output_file = 'A2199_caustics.csv'
    df_caustics.to_csv(output_file, index=False)
    
    print(f"\n✅ Saved caustic parameters to: {output_file}")
    print(f"   Grid points: {len(df_caustics)}")
    print(f"   Radius range: {r_grid.min():.3f} - {r_grid.max():.3f} Mpc")
    print(f"   Amplitude range: {A.min():.1f} - {A.max():.1f} km/s")


def add_membership_to_catalog(df_main, df_sample, member_flags):
    """
    Add membership flags to the main catalog.
    
    Parameters
    ----------
    df_main : pd.DataFrame
        Full catalog (all objects)
    df_sample : pd.DataFrame
        Sample used for caustic analysis
    member_flags : array
        Boolean membership flags from caustic
    
    Returns
    -------
    pd.DataFrame
        Main catalog with 'member' column
    """
    print("\n" + "="*70)
    print("ADDING MEMBERSHIP FLAGS TO CATALOG")
    print("="*70)
    
    # Add membership flags to sample
    df_sample_copy = df_sample.copy()
    df_sample_copy['member'] = member_flags
    df_sample_copy['member'] = df_sample_copy['member'].map({True: 'Y', False: 'N'})
    
    # Drop temporary VEL column
    df_sample_copy = df_sample_copy.drop(columns=['VEL'])
    
    # Merge membership back into main catalog
    # Match on all common columns except 'member'
    common_cols = [col for col in df_sample_copy.columns if col != 'member']
    
    df_merged = df_main.merge(
        df_sample_copy[common_cols + ['member']],
        on=common_cols,
        how='left'
    )
    
    # Fill missing membership values with 'N' (no redshift or not analyzed)
    df_merged['member'] = df_merged['member'].fillna('N')
    
    # Print statistics
    n_members = (df_merged['member'] == 'Y').sum()
    n_non_members = (df_merged['member'] == 'N').sum()
    
    print(f"\nMembership statistics:")
    print(f"  Members (Y): {n_members:,} ({n_members/len(df_merged)*100:.1f}%)")
    print(f"  Non-members (N): {n_non_members:,} ({n_non_members/len(df_merged)*100:.1f}%)")
    print(f"  Total objects: {len(df_merged):,}")
    
    return df_merged


def main():
    """
    Main function to run the complete membership determination pipeline.
    """
    print("="*70)
    print("A2199 CLUSTER MEMBERSHIP DETERMINATION")
    print("Using Caustic Method (CausticSNUpy)")
    print("="*70)
    
    # Step 1: Load data
    df_main, df_sample, cluster_params = load_data('A2199')
    
    # Step 2: Run caustic analysis
    result = run_caustic_analysis(df_sample, cluster_params)
    
    # Step 3: Save caustic parameters
    save_caustic_parameters(result)
    
    # Step 4: Add membership to catalog
    df_final = add_membership_to_catalog(df_main, df_sample, result.member)
    
    # Step 5: Save final catalog
    print("\n" + "="*70)
    print("SAVING FINAL CATALOG")
    print("="*70)
    
    output_file = 'A2199_mastercat_within35arcmin.csv'
    df_final.to_csv(output_file, index=False)
    
    print(f"\n✅ Saved final catalog to: {output_file}")
    print(f"   Total objects: {len(df_final):,}")
    print(f"   Total columns: {len(df_final.columns)}")
    print(f"   Members: {(df_final['member'] == 'Y').sum():,}")
    
    print("\n" + "="*70)
    print("PIPELINE COMPLETE")
    print("="*70)
    print("\nOutput files created:")
    print("  1. A2199_caustics.csv - Caustic envelope parameters")
    print("  2. A2199_mastercat_intermediate_file1.csv - Catalog with membership")
    print("\nReady for downstream analysis (galaxy selection, k-corrections, LF)")


if __name__ == "__main__":
    main()
