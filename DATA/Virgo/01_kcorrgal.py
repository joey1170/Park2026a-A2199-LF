#!/usr/bin/env python3
"""
Virgo Cluster K-Correction and Absolute Magnitude Calculation Script

This script applies k-corrections and calculates absolute magnitudes for
Virgo cluster galaxies using the kcorrect package.

Steps:
1. Load photometric catalog from previous step
2. Clean data (fill NaNs, fix negative redshifts)
3. Apply extinction correction (dereddening)
4. Convert magnitudes to fluxes (in maggies)
5. Calculate k-corrections using kcorrect package
6. Compute absolute magnitudes
7. Create final master catalog

Input:  Virgo_core_photcat.csv (from 00_read.py)
Output: Virgo_core_mastercat.csv (final catalog with absolute magnitudes)

Author: Jongin Park
Date: 2026
"""

# ==============================================================================
# Import Libraries
# ==============================================================================
import numpy as np
import pandas as pd
from astropy.cosmology import LambdaCDM
from kcorrect.kcorrect import Kcorrect

# ==============================================================================
# Configuration
# ==============================================================================

# Set cosmology (H0=70 km/s/Mpc, Omega_M=0.3, Omega_Lambda=0.7)
cosmo = LambdaCDM(H0=70, Om0=0.3, Ode0=0.7)

# Pandas configuration - show all columns
pd.set_option('display.max_columns', None)

# ==============================================================================
# Define Asinh Magnitude-Flux Conversion Functions
# ==============================================================================

# Softening parameters b in maggies for SDSS bands
# These are used in the asinh magnitude system
_b_table = {
    'u': 1.4e-10, 
    'g': 0.9e-10, 
    'r': 1.2e-10,
    'i': 1.8e-10, 
    'z': 7.4e-10
}

def asinh_mag_to_flux_maggies(m, band):
    """
    Convert asinh magnitude to flux in maggies.
    
    The SDSS asinh magnitude system uses a softening parameter b to handle
    negative fluxes and very faint objects.
    
    Parameters
    ----------
    m : float or array
        Asinh magnitude
    band : str
        Band name ('u', 'g', 'r', 'i', or 'z')
    
    Returns
    -------
    flux : float or array
        Flux in maggies
    """
    b = _b_table[band.lower()]
    return 2 * b * np.sinh((np.log(10) / -2.5) * m - np.log(b))

def asinh_flux_error(f, dm, band):
    """
    Calculate flux error from magnitude error in the asinh system.
    
    Parameters
    ----------
    f : float or array
        Flux in maggies
    dm : float or array
        Magnitude error
    band : str
        Band name ('u', 'g', 'r', 'i', or 'z')
    
    Returns
    -------
    flux_err : float or array
        Flux error in maggies
    """
    b = _b_table[band.lower()]
    term = f / (2 * b)
    factor = (np.log(10) / 2.5) * 2 * b * np.sqrt(1 + term**2)
    return factor * dm

# ==============================================================================
# STEP 1: Load Photometric Catalog
# ==============================================================================
print("="*80)
print("STEP 1: Loading Photometric Catalog")
print("="*80)

input_file = './Virgo_core_photcat.csv'
df = pd.read_csv(input_file)
print(f"Loaded {len(df)} galaxies from {input_file}")
print(f"Columns: {list(df.columns)}")

# ==============================================================================
# STEP 2: Clean Data
# ==============================================================================
print("\n" + "="*80)
print("STEP 2: Cleaning Data (Fix Negative Redshifts and Fill NaNs)")
print("="*80)

# Fix negative redshifts (set to 0)
# Negative redshifts are unphysical and likely due to measurement errors
n_negative = (df['Redshift'] < 0).sum()
if n_negative > 0:
    print(f"Found {n_negative} galaxies with negative redshift - setting to 0")
    df.loc[df['Redshift'] < 0, 'Redshift'] = 0

# List of columns to fill NaN values with column mean
cols_to_fill = [
    'extinction_u', 'extinction_g', 'extinction_r', 'extinction_i', 'extinction_z',
    'petroMagErr_u', 'petroMagErr_g', 'petroMagErr_r', 'petroMagErr_i', 'petroMagErr_z',
    'Redshift', 'Redshift_Err'
]

# Fill NaNs with column-wise mean
print("\nFilling NaN values with column means:")
for col in cols_to_fill:
    n_nan = df[col].isna().sum()
    if n_nan > 0:
        mean_val = df[col].mean(skipna=True)
        df[col] = df[col].fillna(mean_val)
        print(f"  {col}: {n_nan} NaNs filled with mean = {mean_val:.6f}")

# ==============================================================================
# STEP 3: Prepare DataFrame for K-Correction
# ==============================================================================
print("\n" + "="*80)
print("STEP 3: Preparing DataFrame for K-Correction")
print("="*80)

# Select relevant columns and create a new DataFrame
df_kcorr = df[[
    'NGVS', 'Class',
    'u_SDSS', 'g_SDSS', 'r_SDSS', 'i_SDSS', 'z_SDSS',
    'extinction_u', 'extinction_g', 'extinction_r', 'extinction_i', 'extinction_z',
    'petroMagErr_u', 'petroMagErr_g', 'petroMagErr_r', 'petroMagErr_i', 'petroMagErr_z',
    'Redshift', 'Redshift_Err', 'p_radgal'
]].copy()

# Rename columns for clarity
# p_mag = petrosian magnitude, p_extinction = extinction, p_magerr = magnitude error
df_kcorr.rename(columns={
    'u_SDSS': 'p_mag_u',
    'g_SDSS': 'p_mag_g',
    'r_SDSS': 'p_mag_r',
    'i_SDSS': 'p_mag_i',
    'z_SDSS': 'p_mag_z',
    'extinction_u': 'p_extinction_u',
    'extinction_g': 'p_extinction_g',
    'extinction_r': 'p_extinction_r',
    'extinction_i': 'p_extinction_i',
    'extinction_z': 'p_extinction_z',
    'petroMagErr_u': 'p_magerr_u',
    'petroMagErr_g': 'p_magerr_g',
    'petroMagErr_r': 'p_magerr_r',
    'petroMagErr_i': 'p_magerr_i',
    'petroMagErr_z': 'p_magerr_z'
}, inplace=True)

print(f"Created k-correction DataFrame with {len(df_kcorr)} galaxies")

# ==============================================================================
# STEP 4: Apply Extinction Correction (Dereddening)
# ==============================================================================
print("\n" + "="*80)
print("STEP 4: Applying Extinction Correction (Dereddening)")
print("="*80)

# Define SDSS bands
bands = ['u', 'g', 'r', 'i', 'z']

# Apply extinction correction: m_0 = m_obs - A_lambda
# where m_0 is dereddened magnitude, m_obs is observed magnitude, A_lambda is extinction
for b in bands:
    df_kcorr[f'p_mag_{b}_0'] = df_kcorr[f'p_mag_{b}'] - df_kcorr[f'p_extinction_{b}']
    df_kcorr[f'p_magerr_{b}_0'] = df_kcorr[f'p_magerr_{b}']

print("Applied extinction correction to all 5 bands (ugriz)")
print("  Dereddened magnitudes stored in columns: p_mag_X_0")

# ==============================================================================
# STEP 5: Convert Magnitudes to Fluxes
# ==============================================================================
print("\n" + "="*80)
print("STEP 5: Converting Magnitudes to Fluxes (in maggies)")
print("="*80)

# For each band, convert dereddened magnitudes to fluxes
for band in bands:
    mag_col = f'p_mag_{band}_0'        # dereddened magnitude
    magerr_col = f'p_magerr_{band}_0'  # magnitude error
    
    flux_col = f'p_mag_{band}_flux'     # flux in maggies
    ferr_col = f'p_mag_{band}_fluxerr'  # flux error in maggies
    ivar_col = f'p_mag_{band}_ivar'     # inverse variance = 1/σ²
    
    # Compute flux in maggies using asinh magnitude system
    df_kcorr[flux_col] = asinh_mag_to_flux_maggies(df_kcorr[mag_col].values, band)
    
    # Compute 1-sigma flux error
    df_kcorr[ferr_col] = asinh_flux_error(
        df_kcorr[flux_col].values,
        df_kcorr[magerr_col].values,
        band
    )
    
    # Compute inverse variance = 1 / (σ_flux)²
    df_kcorr[ivar_col] = 1.0 / (df_kcorr[ferr_col] ** 2)

print("Converted magnitudes to fluxes for all 5 bands")
print("  Created columns: p_mag_X_flux, p_mag_X_fluxerr, p_mag_X_ivar")

# ==============================================================================
# STEP 6: Calculate K-Corrections and Absolute Magnitudes
# ==============================================================================
print("\n" + "="*80)
print("STEP 6: Calculating K-Corrections and Absolute Magnitudes")
print("="*80)

# Define SDSS filter responses for kcorrect
responses = [f'sdss_{b}0' for b in bands]

# Initialize Kcorrect object
print("Initializing Kcorrect...")
kc = Kcorrect(
    responses=responses,
    redshift_range=[0.0, 5.0],   # extend z_max to 5.0
    nredshift=6000,              # number of redshift samples
    cosmo=cosmo
)

# Extract inputs from DataFrame
redshifts = df_kcorr['Redshift'].values
maggies = df_kcorr[[f'p_mag_{b}_flux' for b in bands]].values
ivars = df_kcorr[[f'p_mag_{b}_ivar' for b in bands]].values

print(f"Fitting {len(redshifts)} galaxies...")
print("  This may take a few minutes...")

# Fit template coefficients
# These coefficients represent the best-fit linear combination of templates
coeffs = kc.fit_coeffs(redshift=redshifts, maggies=maggies, ivar=ivars)
print("  Template coefficients fitted")

# Compute k-corrections with band_shift = 0.1 (rest-frame at z=0.1)
# K-correction allows us to correct observed magnitudes to a common rest-frame
kcorrs = kc.kcorrect(redshift=redshifts, coeffs=coeffs, band_shift=0.1)
print("  K-corrections computed")

# Compute absolute magnitudes
# Absolute magnitude is the magnitude an object would have at a standard distance (10 pc)
absmags = kc.absmag(
    redshift=redshifts, 
    maggies=maggies, 
    ivar=ivars, 
    coeffs=coeffs, 
    band_shift=0.1
)
print("  Absolute magnitudes computed")

# Store results back in DataFrame
for i, b in enumerate(bands):
    df_kcorr[f'p_mag_{b}_absmag'] = absmags[:, i]

print("\nK-correction complete!")
print(f"  Absolute magnitudes stored in columns: p_mag_X_absmag")

# ==============================================================================
# STEP 7: Create Final Master Catalog
# ==============================================================================
print("\n" + "="*80)
print("STEP 7: Creating Final Master Catalog")
print("="*80)

# Select only the essential columns for the final catalog
df_main = df_kcorr[[
    'NGVS',              # Galaxy identifier
    'Class',             # Galaxy classification
    'Redshift',          # Redshift
    'Redshift_Err',      # Redshift error
    'p_mag_u_0',         # Dereddened u-band magnitude
    'p_magerr_u_0',      # u-band magnitude error
    'p_mag_g_0',         # Dereddened g-band magnitude
    'p_magerr_g_0',      # g-band magnitude error
    'p_mag_r_0',         # Dereddened r-band magnitude
    'p_magerr_r_0',      # r-band magnitude error
    'p_mag_i_0',         # Dereddened i-band magnitude
    'p_magerr_i_0',      # i-band magnitude error
    'p_mag_z_0',         # Dereddened z-band magnitude
    'p_magerr_z_0',      # z-band magnitude error
    'p_mag_r_absmag',    # Absolute r-band magnitude
    'p_radgal'           # Projected radial distance from M87
]]

# Sort by absolute r-band magnitude (brightest first)
df_main = df_main.sort_values(by='p_mag_r_absmag')

print(f"Final catalog contains {len(df_main)} galaxies")
print(f"Columns: {list(df_main.columns)}")

# Display summary statistics
print("\nAbsolute r-band magnitude statistics:")
print(f"  Brightest: {df_main['p_mag_r_absmag'].min():.2f}")
print(f"  Faintest:  {df_main['p_mag_r_absmag'].max():.2f}")
print(f"  Mean:      {df_main['p_mag_r_absmag'].mean():.2f}")
print(f"  Median:    {df_main['p_mag_r_absmag'].median():.2f}")

# ==============================================================================
# STEP 8: Save Final Catalog
# ==============================================================================
print("\n" + "="*80)
print("STEP 8: Saving Final Master Catalog")
print("="*80)

output_file = './Virgo_core_mastercat.csv'
df_main.to_csv(output_file, index=False)

print(f"Successfully saved: {output_file}")
print(f"\nFinal catalog summary:")
print(f"  Number of galaxies: {len(df_main)}")
print(f"  Number of columns: {len(df_main.columns)}")

# Display first few rows
print("\nFirst 5 galaxies (sorted by absolute magnitude):")
print(df_main.head(5).to_string())

print("\n" + "="*80)
print("K-CORRECTION PROCESSING COMPLETE!")
print("="*80)
