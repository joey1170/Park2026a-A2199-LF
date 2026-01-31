#!/usr/bin/env python3
"""
K-Correction and Absolute Magnitude Calculation for A2199 Galaxy Catalog

This script performs k-corrections on SDSS photometry to compute absolute magnitudes
for galaxies in the A2199 cluster catalog.

Input:
    - 04f.A2199_mastercat_within35arcmin_flag_update.csv

Output:
    - A2199_mastercat_within35arcmin.csv

The script:
1. Loads the photometric catalog with spectroscopic redshifts
2. Filters galaxies with valid redshifts
3. Applies Galactic extinction correction to Petrosian magnitudes
4. Converts magnitudes to flux in maggies using asinh transformation
5. Runs kcorrect to compute k-corrections and absolute magnitudes
6. Merges the r-band absolute magnitude back to the original catalog
7. Saves the final catalog with absolute magnitudes
"""

import os
import numpy as np
import pandas as pd
from astropy.cosmology import LambdaCDM
from kcorrect.kcorrect import Kcorrect


# Softening parameters b in maggies for SDSS asinh magnitudes
_B_TABLE = {
    'u': 1.4e-10,
    'g': 0.9e-10,
    'r': 1.2e-10,
    'i': 1.8e-10,
    'z': 7.4e-10
}


def asinh_mag_to_flux_maggies(m, band):
    """
    Convert SDSS asinh magnitude to flux in maggies.
    
    Parameters
    ----------
    m : array-like
        Magnitude values
    band : str
        SDSS band ('u', 'g', 'r', 'i', or 'z')
    
    Returns
    -------
    flux : array-like
        Flux in maggies
    """
    b = _B_TABLE[band.lower()]
    return 2 * b * np.sinh((np.log(10) / -2.5) * m - np.log(b))


def asinh_flux_error(f, dm, band):
    """
    Propagate magnitude error to flux error for SDSS asinh magnitudes.
    
    Parameters
    ----------
    f : array-like
        Flux in maggies
    dm : array-like
        Magnitude error
    band : str
        SDSS band ('u', 'g', 'r', 'i', or 'z')
    
    Returns
    -------
    flux_err : array-like
        Flux error in maggies
    """
    b = _B_TABLE[band.lower()]
    term = f / (2 * b)
    factor = (np.log(10) / 2.5) * 2 * b * np.sqrt(1 + term**2)
    return factor * dm


def load_catalog(input_file='./04f.A2199_mastercat_within35arcmin_flag_update.csv'):
    """
    Load the photometric catalog and filter for valid redshifts.
    
    Parameters
    ----------
    input_file : str
        Path to input CSV file
    
    Returns
    -------
    df0 : DataFrame
        Original full catalog
    df : DataFrame
        Filtered catalog with valid redshifts only
    """
    print(f"Loading catalog from {input_file}")
    df0 = pd.read_csv(input_file)
    print(f"Total objects in catalog: {len(df0)}")
    
    # Filter for valid redshifts (z_tot_z != -9 and z_tot_z > 0)
    df = df0[(df0['z_tot_z'] != -9) & (df0['z_tot_z'] > 0)].copy()
    print(f"Objects with valid redshifts: {len(df)}")
    
    return df0, df


def apply_extinction_correction(df, bands=['u', 'g', 'r', 'i', 'z']):
    """
    Apply Galactic extinction correction to Petrosian magnitudes.
    
    Parameters
    ----------
    df : DataFrame
        Galaxy catalog
    bands : list
        List of SDSS bands
    
    Returns
    -------
    df : DataFrame
        Catalog with dereddened magnitudes added
    """
    print("Applying Galactic extinction correction")
    
    for b in bands:
        # Deredden: subtract extinction from observed magnitude
        df[f'p_petromag_{b}_0'] = df[f'p_petromag_{b}'] - df[f'p_extinction_{b}']
        # Error remains the same
        df[f'p_petromagerr_{b}_0'] = df[f'p_petromagerr_{b}']
    
    return df


def convert_mag_to_flux(df, bands=['u', 'g', 'r', 'i', 'z']):
    """
    Convert dereddened magnitudes to flux in maggies and compute inverse variance.
    
    Parameters
    ----------
    df : DataFrame
        Galaxy catalog with dereddened magnitudes
    bands : list
        List of SDSS bands
    
    Returns
    -------
    df : DataFrame
        Catalog with flux, flux error, and inverse variance columns added
    """
    print("Converting magnitudes to flux (maggies)")
    
    for band in bands:
        mag_col = f'p_petromag_{band}_0'          # dereddened magnitude
        magerr_col = f'p_petromagerr_{band}_0'     # magnitude error
        
        flux_col = f'p_petromag_{band}_flux'       # flux in maggies
        ferr_col = f'p_petromag_{band}_fluxerr'    # flux error
        ivar_col = f'p_petromag_{band}_ivar'       # inverse variance
        
        # Compute flux in maggies
        df[flux_col] = asinh_mag_to_flux_maggies(df[mag_col].values, band)
        
        # Compute 1-sigma flux error
        df[ferr_col] = asinh_flux_error(df[flux_col].values,
                                        df[magerr_col].values,
                                        band)
        
        # Compute inverse variance = 1 / (sigma_f)^2
        df[ivar_col] = 1.0 / (df[ferr_col] ** 2)
    
    return df


def run_kcorrect(df, cosmo, bands=['u', 'g', 'r', 'i', 'z']):
    """
    Run kcorrect to compute k-corrections and absolute magnitudes.
    
    Parameters
    ----------
    df : DataFrame
        Galaxy catalog with flux measurements
    cosmo : astropy.cosmology
        Cosmology model
    bands : list
        List of SDSS bands
    
    Returns
    -------
    df : DataFrame
        Catalog with absolute magnitudes added
    """
    print("Running kcorrect to compute absolute magnitudes")
    
    # Initialize Kcorrect with SDSS responses
    responses = [f'sdss_{b}0' for b in bands]
    kc = Kcorrect(
        responses=responses,
        redshift_range=[0.0, 5.0],
        nredshift=6000,
        cosmo=cosmo
    )
    
    # Extract inputs from DataFrame
    redshifts = df['z_tot_z'].values
    maggies = df[[f'p_petromag_{b}_flux' for b in bands]].values
    ivars = df[[f'p_petromag_{b}_ivar' for b in bands]].values
    
    # Fit template coefficients
    print("  Fitting SED coefficients...")
    coeffs = kc.fit_coeffs(redshift=redshifts, maggies=maggies, ivar=ivars)
    
    # Compute k-corrections and absolute magnitudes
    print("  Computing k-corrections and absolute magnitudes...")
    kcorrs = kc.kcorrect(redshift=redshifts, coeffs=coeffs, band_shift=0.1)
    absmags = kc.absmag(redshift=redshifts, maggies=maggies, ivar=ivars,
                       coeffs=coeffs, band_shift=0.1)
    
    # Store absolute magnitudes in DataFrame
    for i, b in enumerate(bands):
        df[f'p_petromag_{b}_absmag'] = absmags[:, i]
    
    print("K-correction completed")
    
    return df


def clean_intermediate_columns(df, bands=['u', 'g', 'r', 'i', 'z']):
    """
    Drop intermediate columns used for k-correction.
    Keep only the r-band absolute magnitude.
    
    Parameters
    ----------
    df : DataFrame
        Galaxy catalog with all computed columns
    bands : list
        List of SDSS bands
    
    Returns
    -------
    df : DataFrame
        Catalog with intermediate columns removed
    """
    print("Removing intermediate columns")
    
    # List of columns to drop
    columns_to_drop = []
    
    for b in bands:
        columns_to_drop.extend([
            f'p_petromag_{b}_0',
            f'p_petromagerr_{b}_0',
            f'p_petromag_{b}_flux',
            f'p_petromag_{b}_fluxerr',
            f'p_petromag_{b}_ivar'
        ])
        # Drop absolute magnitudes for all bands except r
        if b != 'r':
            columns_to_drop.append(f'p_petromag_{b}_absmag')
    
    # Drop columns that exist in the dataframe
    columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    df.drop(columns=columns_to_drop, inplace=True)
    
    return df


def merge_and_save(df0, df, output_file='./A2199_mastercat_within35arcmin.csv'):
    """
    Merge the r-band absolute magnitude back to the original catalog and save.
    
    Parameters
    ----------
    df0 : DataFrame
        Original full catalog
    df : DataFrame
        Processed catalog with r-band absolute magnitude
    output_file : str
        Path to output CSV file
    
    Returns
    -------
    df_final : DataFrame
        Final merged catalog
    """
    print("Merging results back to original catalog")
    
    # Merge only the r-band absolute magnitude
    df_final = df0.merge(df[['p_objid', 'p_petromag_r_absmag']],
                        on='p_objid',
                        how='left')
    
    print(f"Saving final catalog to {output_file}")
    df_final.to_csv(output_file, index=False)
    print(f"Final catalog saved with {len(df_final)} objects")
    
    return df_final


def main():
    """
    Main function to run the k-correction pipeline.
    """
    print("=" * 70)
    print("K-Correction and Absolute Magnitude Calculation")
    print("=" * 70)
    
    # Set cosmology (WMAP)
    cosmo = LambdaCDM(H0=70, Om0=0.3, Ode0=0.7)
    print(f"Using cosmology: H0={cosmo.H0.value}, Om0={cosmo.Om0}, Ode0={cosmo.Ode0}")
    print()
    
    # Load catalog
    df0, df = load_catalog()
    print()
    
    # Apply extinction correction
    df = apply_extinction_correction(df)
    print()
    
    # Convert magnitudes to flux
    df = convert_mag_to_flux(df)
    print()
    
    # Run k-correction
    df = run_kcorrect(df, cosmo)
    print()
    
    # Clean up intermediate columns
    df = clean_intermediate_columns(df)
    print()
    
    # Merge and save
    df_final = merge_and_save(df0, df)
    print()
    
    print("=" * 70)
    print("K-correction pipeline completed successfully!")
    print("=" * 70)
    
    return df_final


if __name__ == '__main__':
    df_final = main()
