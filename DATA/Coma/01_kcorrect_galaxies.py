#!/usr/bin/env python3
"""
K-correction and Absolute Magnitude Calculation for Coma Cluster Galaxies

This script performs k-corrections on SDSS photometry using the kcorrect package:
1. Loads photometric and spectroscopic catalogs
2. Applies Galactic extinction correction
3. Converts SDSS asinh magnitudes to flux (maggies)
4. Runs kcorrect to compute rest-frame absolute magnitudes
5. Outputs cleaned catalog with photometry and absolute magnitudes

Requirements:
    - kcorrect (Python package)
    - astropy
    - pandas
    - numpy

Author: Jongin Park
Date: 2026
"""

import os
import numpy as np
import pandas as pd
from astropy.cosmology import LambdaCDM
from kcorrect.kcorrect import Kcorrect

# Set cosmology (H0=70, Omega_m=0.3, Omega_Lambda=0.7)
cosmo = LambdaCDM(H0=70, Om0=0.3, Ode0=0.7)


# ============================================================================
# SDSS Asinh Magnitude Conversion Functions
# ============================================================================

# Softening parameters b in maggies for each SDSS band
_B_TABLE = {
    'u': 1.4e-10,
    'g': 0.9e-10,
    'r': 1.2e-10,
    'i': 1.8e-10,
    'z': 7.4e-10
}


def asinh_mag_to_flux_maggies(mag, band):
    """
    Convert SDSS asinh magnitude to flux in maggies.
    
    The SDSS asinh magnitude system is defined as:
        m = -2.5/ln(10) * [asinh((f/f0)/(2b)) + ln(b)]
    
    Parameters
    ----------
    mag : array-like
        SDSS asinh magnitudes
    band : str
        Band name ('u', 'g', 'r', 'i', or 'z')
    
    Returns
    -------
    flux : array-like
        Flux in maggies (1 maggie = 3631 Jy)
    """
    b = _B_TABLE[band.lower()]
    flux = 2 * b * np.sinh((np.log(10) / -2.5) * mag - np.log(b))
    return flux


def asinh_flux_error(flux, mag_err, band):
    """
    Propagate magnitude error to flux error.
    
    Parameters
    ----------
    flux : array-like
        Flux in maggies
    mag_err : array-like
        Magnitude error (1-sigma)
    band : str
        Band name ('u', 'g', 'r', 'i', or 'z')
    
    Returns
    -------
    flux_err : array-like
        Flux error in maggies
    """
    b = _B_TABLE[band.lower()]
    term = flux / (2 * b)
    factor = (np.log(10) / 2.5) * 2 * b * np.sqrt(1 + term**2)
    flux_err = factor * mag_err
    return flux_err


# ============================================================================
# Main Processing Functions
# ============================================================================

def load_and_merge_catalogs(redshift_file, photometry_file):
    """
    Load redshift and photometry catalogs and merge them.
    
    Parameters
    ----------
    redshift_file : str
        Path to CSV file with redshift data
    photometry_file : str
        Path to CSV file with photometry data
    
    Returns
    -------
    df_merged : pd.DataFrame
        Merged catalog
    """
    print("Loading catalogs...")
    
    # Load redshift catalog
    df_redshift = pd.read_csv(redshift_file)
    
    # Rename columns for consistency
    df_redshift = df_redshift.rename(columns={
        'z': 'z_tot_z',
        'e_z': 'z_tot_zerr',
    })
    
    # Load photometry catalog (suppress mixed types warning)
    df_phot = pd.read_csv(photometry_file, low_memory=False)
    
    # Select relevant photometry columns
    phot_columns = [
        'p_radgal', 'p_objid', 'p_probpsf',
        # Petrosian magnitudes (ugriz)
        'p_petromag_u', 'p_petromagerr_u',
        'p_petromag_g', 'p_petromagerr_g',
        'p_petromag_r', 'p_petromagerr_r',
        'p_petromag_i', 'p_petromagerr_i',
        'p_petromag_z', 'p_petromagerr_z',
        # Model magnitudes (ugriz)
        'p_modelmag_u', 'p_modelmagerr_u',
        'p_modelmag_g', 'p_modelmagerr_g',
        'p_modelmag_r', 'p_modelmagerr_r',
        'p_modelmag_i', 'p_modelmagerr_i',
        'p_modelmag_z', 'p_modelmagerr_z',
        # Fiber magnitudes (ugriz)
        'p_fibermag_u', 'p_fibermagerr_u',
        'p_fibermag_g', 'p_fibermagerr_g',
        'p_fibermag_r', 'p_fibermagerr_r',
        'p_fibermag_i', 'p_fibermagerr_i',
        'p_fibermag_z', 'p_fibermagerr_z',
        # Extinction corrections
        'p_extinction_u', 'p_extinction_g', 'p_extinction_r',
        'p_extinction_i', 'p_extinction_z'
    ]
    
    df_phot = df_phot[phot_columns]
    
    # Merge on object ID
    df_merged = df_redshift.merge(
        df_phot,
        how='right',
        left_on='ObjID',
        right_on='p_objid'
    )
    
    print(f"  Loaded {len(df_redshift):,} redshift entries")
    print(f"  Loaded {len(df_phot):,} photometry entries")
    print(f"  Merged catalog: {len(df_merged):,} objects")
    
    return df_merged


def apply_extinction_correction_and_convert_to_flux(df):
    """
    Apply Galactic extinction correction and convert magnitudes to flux.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input catalog with photometry
    
    Returns
    -------
    df_corrected : pd.DataFrame
        Catalog with dereddened magnitudes, fluxes, and inverse variances
    """
    print("\nApplying extinction correction and converting to flux...")
    
    # Filter for objects with valid redshifts
    mask = (
        ~df['z_tot_z'].isna() &
        (df['z_tot_z'] != -9) &
        (df['z_tot_z'] > 0) &
        (df['z_tot_z'] < 5)
    )
    
    df_kcorr = df[mask].copy()
    print(f"  Selected {len(df_kcorr):,} objects with valid redshifts (0 < z < 5)")
    
    bands = ['u', 'g', 'r', 'i', 'z']
    
    # Apply extinction correction (create dereddened magnitudes)
    for band in bands:
        mag_col = f'p_petromag_{band}'
        ext_col = f'p_extinction_{band}'
        magerr_col = f'p_petromagerr_{band}'
        
        # Dereddened magnitude = observed magnitude - extinction
        df_kcorr[f'p_petromag_{band}_0'] = df_kcorr[mag_col] - df_kcorr[ext_col]
        df_kcorr[f'p_petromagerr_{band}_0'] = df_kcorr[magerr_col]
    
    # Convert dereddened magnitudes to flux (maggies) and inverse variance
    for band in bands:
        mag_col = f'p_petromag_{band}_0'
        magerr_col = f'p_petromagerr_{band}_0'
        
        flux_col = f'p_petromag_{band}_flux'
        ferr_col = f'p_petromag_{band}_fluxerr'
        ivar_col = f'p_petromag_{band}_ivar'
        
        # Compute flux in maggies
        df_kcorr[flux_col] = asinh_mag_to_flux_maggies(
            df_kcorr[mag_col].values, band
        )
        
        # Compute flux error
        df_kcorr[ferr_col] = asinh_flux_error(
            df_kcorr[flux_col].values,
            df_kcorr[magerr_col].values,
            band
        )
        
        # Compute inverse variance = 1 / sigma^2
        df_kcorr[ivar_col] = 1.0 / (df_kcorr[ferr_col] ** 2)
    
    print(f"  Computed fluxes and inverse variances for {len(bands)} bands")
    
    return df_kcorr


def run_kcorrect(df_kcorr, cosmo):
    """
    Run kcorrect to compute rest-frame absolute magnitudes.
    
    Parameters
    ----------
    df_kcorr : pd.DataFrame
        Catalog with flux measurements
    cosmo : astropy.cosmology
        Cosmology object
    
    Returns
    -------
    df_kcorr : pd.DataFrame
        Catalog with added absolute magnitude columns
    """
    print("\nRunning kcorrect...")
    
    bands = ['u', 'g', 'r', 'i', 'z']
    
    # Initialize Kcorrect with SDSS filter responses
    kc = Kcorrect(
        responses=['sdss_u0', 'sdss_g0', 'sdss_r0', 'sdss_i0', 'sdss_z0'],
        redshift_range=[0.0, 5.0],
        nredshift=6000,
        cosmo=cosmo
    )
    
    # Extract arrays from DataFrame
    redshifts = df_kcorr['z_tot_z'].values
    maggies = df_kcorr[[f'p_petromag_{b}_flux' for b in bands]].values
    ivars = df_kcorr[[f'p_petromag_{b}_ivar' for b in bands]].values
    
    print(f"  Fitting {len(redshifts):,} galaxies...")
    
    # Fit template coefficients
    coeffs = kc.fit_coeffs(redshift=redshifts, maggies=maggies, ivar=ivars)
    
    # Compute k-corrections and absolute magnitudes
    # band_shift=0.1 means we're computing 0.1z absolute magnitudes
    kcorrs = kc.kcorrect(redshift=redshifts, coeffs=coeffs, band_shift=0.1)
    absmags = kc.absmag(
        redshift=redshifts,
        maggies=maggies,
        ivar=ivars,
        coeffs=coeffs,
        band_shift=0.1
    )
    
    # Store absolute magnitudes in DataFrame
    for i, band in enumerate(bands):
        df_kcorr[f'p_petromag_{band}_absmag'] = absmags[:, i]
    
    print(f"  Computed absolute magnitudes for {len(bands)} bands")
    
    return df_kcorr


def create_final_catalog(df_full, df_kcorr):
    """
    Create final output catalog with cleaned columns.
    
    Parameters
    ----------
    df_full : pd.DataFrame
        Full merged catalog
    df_kcorr : pd.DataFrame
        Subset with kcorrect results
    
    Returns
    -------
    maindf : pd.DataFrame
        Final cleaned catalog
    """
    print("\nCreating final catalog...")
    
    # Select final columns from full catalog
    final_columns = [
        'p_radgal', 'p_objid', 'p_probpsf',
        'z_tot_z', 'z_tot_zerr', 'r_z', 'Member',
        'p_petromag_u', 'p_petromagerr_u',
        'p_petromag_g', 'p_petromagerr_g',
        'p_petromag_r', 'p_petromagerr_r',
        'p_petromag_i', 'p_petromagerr_i',
        'p_petromag_z', 'p_petromagerr_z',
        'p_modelmag_u', 'p_modelmagerr_u',
        'p_modelmag_g', 'p_modelmagerr_g',
        'p_modelmag_r', 'p_modelmagerr_r',
        'p_modelmag_i', 'p_modelmagerr_i',
        'p_modelmag_z', 'p_modelmagerr_z',
        'p_fibermag_u', 'p_fibermagerr_u',
        'p_fibermag_g', 'p_fibermagerr_g',
        'p_fibermag_r', 'p_fibermagerr_r',
        'p_fibermag_i', 'p_fibermagerr_i',
        'p_fibermag_z', 'p_fibermagerr_z',
        'p_extinction_u', 'p_extinction_g',
        'p_extinction_r', 'p_extinction_i', 'p_extinction_z'
    ]
    
    df_final = df_full[final_columns].copy()
    
    # Fill NaN values
    df_final[['z_tot_z', 'z_tot_zerr', 'r_z']] = \
        df_final[['z_tot_z', 'z_tot_zerr', 'r_z']].fillna(-9)
    df_final['Member'] = df_final['Member'].fillna(0)
    
    # Rename Member column
    df_final = df_final.rename(columns={'Member': 'member'})
    
    # Merge with kcorrect results (add absolute magnitude)
    maindf = df_final.merge(
        df_kcorr[['p_objid', 'p_petromag_r_absmag']],
        how='left',
        on='p_objid'
    )
    
    # Fill missing absolute magnitudes with -99.0
    maindf['p_petromag_r_absmag'] = maindf['p_petromag_r_absmag'].fillna(-99.0)
    
    print(f"  Final catalog: {len(maindf):,} objects")
    print(f"  Objects with absolute magnitudes: {(maindf['p_petromag_r_absmag'] != -99.0).sum():,}")
    
    return maindf


def main():
    """
    Main function to run the complete k-correction pipeline.
    """
    print("="*70)
    print("Coma Cluster K-correction Pipeline")
    print("="*70)
    
    # Define input file paths
    redshift_file = './coma_datafile2.csv'
    photometry_file = './coma_woody_master_catalog.csv'
    output_file = 'Coma_mastercat.csv'
    
    # Step 1: Load and merge catalogs
    print("\nSTEP 1: Loading and merging catalogs")
    print("-"*70)
    df_merged = load_and_merge_catalogs(redshift_file, photometry_file)
    
    # Step 2: Apply extinction correction and convert to flux
    print("\nSTEP 2: Extinction correction and flux conversion")
    print("-"*70)
    df_kcorr = apply_extinction_correction_and_convert_to_flux(df_merged)
    
    # Step 3: Run kcorrect
    print("\nSTEP 3: Computing k-corrections and absolute magnitudes")
    print("-"*70)
    df_kcorr = run_kcorrect(df_kcorr, cosmo)
    
    # Step 4: Create final catalog
    print("\nSTEP 4: Creating final catalog")
    print("-"*70)
    maindf = create_final_catalog(df_merged, df_kcorr)
    
    # Step 5: Save to CSV (entire catalog)
    print("\nSTEP 5: Saving output")
    print("-"*70)
    maindf.to_csv(output_file, index=False)
    print(f"  Saved final catalog to: {output_file}")

    # Save only objects with p_radgal < 35 into a separate file
    mask_within35 = maindf['p_radgal'] < 35
    maindf_within35 = maindf[mask_within35].copy()
    output_within35_file = 'Coma_mastercat_within35arcmin.csv'
    maindf_within35.to_csv(output_within35_file, index=False)
    print(f"  Saved catalog for p_radgal < 35 arcmin to: {output_within35_file}")

    # Print summary statistics
    print("\n" + "="*70)
    print("PROCESSING COMPLETE")
    print("="*70)
    print(f"\nTotal objects in catalog: {len(maindf):,}")
    print(f"Objects with redshifts: {(maindf['z_tot_z'] > 0).sum():,}")
    print(f"Objects with absolute magnitudes: {(maindf['p_petromag_r_absmag'] != -99.0).sum():,}")

    print(f"\nObjects within 35 arcmin (p_radgal < 35): {len(maindf_within35):,}")
    print(f"  ...with absolute magnitudes: {(maindf_within35['p_petromag_r_absmag'] != -99.0).sum():,}")
    print(f"  ...with redshifts: {(maindf_within35['z_tot_z'] > 0).sum():,}")
    
    # Redshift statistics
    z_data = maindf[maindf['z_tot_z'] > 0]['z_tot_z']
    if len(z_data) > 0:
        print(f"\nRedshift range: {z_data.min():.4f} - {z_data.max():.4f}")
        print(f"Median redshift: {z_data.median():.4f}")
    
    # Absolute magnitude statistics
    absmag_data = maindf[maindf['p_petromag_r_absmag'] != -99.0]['p_petromag_r_absmag']
    if len(absmag_data) > 0:
        print(f"\nAbsolute r-band magnitude range: {absmag_data.min():.2f} - {absmag_data.max():.2f}")
        print(f"Median M_r: {absmag_data.median():.2f}")

    absmag_within35_data = maindf_within35[maindf_within35['p_petromag_r_absmag'] != -99.0]['p_petromag_r_absmag']
    if len(absmag_within35_data) > 0:
        print(f"\n(Within 35 arcmin) Absolute r-band magnitude range: {absmag_within35_data.min():.2f} - {absmag_within35_data.max():.2f}")
        print(f"(Within 35 arcmin) Median M_r: {absmag_within35_data.median():.2f}")

    print("\n" + "="*70)


if __name__ == "__main__":
    main()
