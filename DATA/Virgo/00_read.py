#!/usr/bin/env python3
"""
Virgo Cluster Photometric Catalog Processing Script

This script processes Virgo cluster galaxy data from Ferrarese+2020 tables,
queries SDSS for extinction values, and creates a master photometric catalog.

Steps:
1. Read Ferrarese+2020 tables (Tables 4-7)
2. Query SDSS DR18 for extinction values and photometry (within 1 arcsec)
3. Calculate projected radial distance from Virgo cluster center (M87)
4. Calculate redshifts from velocities
5. Convert MegaCam magnitudes to SDSS system
6. Merge all data and create final photometric catalog

Output: 02.Virgo_core_photcat.csv

Author: Jongin Park
Date: 2026
"""

# ==============================================================================
# Import Libraries
# ==============================================================================
import os
from pathlib import Path
import numpy as np
import pandas as pd
from astropy import coordinates as coords
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.table import Table
from astropy.io import fits
from astropy.cosmology import LambdaCDM
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ==============================================================================
# Configuration
# ==============================================================================

# Set cosmology (H0=70 km/s/Mpc, Omega_M=0.3, Omega_Lambda=0.7)
cosmo = LambdaCDM(H0=70, Om0=0.3, Ode0=0.7)

# Configure matplotlib plotting parameters
plt.rcParams.update({
    "font.family": 'STIXGeneral',
    'text.usetex': False,
    "mathtext.fontset": 'cm',
    "axes.labelweight": "normal",
    'font.size': 25,
    'font.weight': 'normal',
    
    # Tick direction and appearance
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.top': True,            # show top ticks
    'ytick.right': True,          # show right ticks
    'xtick.minor.visible': True,  # show minor x ticks
    'ytick.minor.visible': True,  # show minor y ticks
    'xtick.major.size': 10,
    'xtick.minor.size': 6,
    'ytick.major.size': 10,
    'ytick.minor.size': 6,
    'xtick.major.width': 1.6,
    'xtick.minor.width': 1.6,
    'ytick.major.width': 1.6,
    'ytick.minor.width': 1.6,
    
    # Axes and line properties
    'lines.linewidth': 2,
    'axes.linewidth': 3.5,
    'axes.labelpad': 4,
    'xtick.major.pad': 7,
    'image.origin': 'lower'
})

# Pandas configuration - show all columns
pd.set_option('display.max_columns', None)

# ==============================================================================
# 1. Load HeCS VAC Data
# ==============================================================================
print("="*80)
print("STEP 1: Loading HeCS VAC Data")
print("="*80)

# Load HeCS (Hectospec Cluster Survey) Value Added Catalog
hecs_vac_data = pd.read_csv('../AllHeCS_VAC_updated.csv')
print(f"Loaded {len(hecs_vac_data)} entries from HeCS VAC")

# Virgo Cluster redshift (corresponds to 1100 km/s, found from member galaxies)
Z_CLID = 0.0036

# Calculate physical size corresponding to 90 arcmin at Virgo cluster distance
d_A = cosmo.angular_diameter_distance(Z_CLID)  # Angular diameter distance in Mpc
angle = (90 * u.arcmin).to(u.radian).value     # Convert 90 arcmin to radians
physical_size = (angle * d_A).to(u.Mpc)        # Physical size in Mpc
print(f"Physical size corresponding to 90 arcmin at z={Z_CLID}: {physical_size:.2f}")

# ==============================================================================
# 2. Read Ferrarese+2020 Tables
# ==============================================================================
print("\n" + "="*80)
print("STEP 2: Reading Ferrarese+2020 NGVS Virgo Core Tables")
print("="*80)

# -----------------------------
# Table 4: NGVS Virgo Core Region Galaxies - Basic Parameters
# -----------------------------
print("\nReading Table 4: Basic Parameters...")

# Define column specifications for fixed-width format
colspecs = [
    (0, 27), (28, 39), (40, 50), (51, 53), (54, 56), (57, 62), (63, 64),
    (64, 66), (67, 69), (70, 74), (75, 76), (77, 81), (82, 88), (89, 94),
    (95, 99), (100, 105), (106, 110), (111, 112)
]

# Define column names
columns = [
    "NGVS",      # NGVS identifier
    "RAdeg",     # Right Ascension (degrees)
    "DEdeg",     # Declination (degrees)
    "RAh",       # RA hours
    "RAm",       # RA minutes
    "RAs",       # RA seconds
    "DE_sign",   # Dec sign
    "DEd",       # Dec degrees
    "DEm",       # Dec arcmin
    "DEs",       # Dec arcsec
    "Class",     # Galaxy classification
    "VCC",       # VCC number
    "Vel",       # Heliocentric velocity (km/s)
    "e_Vel",     # Velocity error
    "r_Vel",     # Velocity reference
    "E(B-V)",    # Reddening
    "FWHM",      # Seeing FWHM
    "Det"        # Detection flag
]

# Read Table 4 from fixed-width file
df_tab4 = pd.read_fwf(
    'Ferrarese2020_tab4.txt',
    colspecs=colspecs,
    names=columns,
    skiprows=60  # Skip header lines
)
print(f"  Loaded {len(df_tab4)} galaxies from Table 4")

# -----------------------------
# Table 5: Structural Parameters
# -----------------------------
print("\nReading Table 5: Structural Parameters...")

colspecs_tab5 = [
    (0, 27), (28, 29), (30, 35), (36, 40), (41, 46), (47, 52),
    (53, 58), (59, 64), (65, 70), (71, 74), (75, 81), (82, 87),
    (88, 93), (94, 95), (95, 96), (97, 102)
]

column_names_tab5 = [
    "NGVS",       # NGVS identifier
    "Class",      # Galaxy classification
    "gmagCG",     # Curve of Growth g-band magnitude
    "C80_20",     # Concentration index C80/20
    "reCG",       # Effective radius from CoG (arcsec)
    "mue",        # Mean surface brightness within re
    "mean_mue",   # Mean surface brightness
    "mu0",        # Central surface brightness
    "gmagS",      # Sersic g-band magnitude
    "n",          # Sersic index
    "reS",        # Sersic effective radius (arcsec)
    "mueS",       # Sersic surface brightness at re
    "mean_mueS",  # Mean Sersic surface brightness
    "NucID",      # Nucleus ID
    "u_NucID",    # Nucleus ID uncertainty flag
    "gmagNuc"     # Nucleus g-band magnitude
]

df_tab5 = pd.read_fwf(
    'Ferrarese2020_tab5.txt',
    colspecs=colspecs_tab5,
    names=column_names_tab5,
    skiprows=56
)
print(f"  Loaded {len(df_tab5)} entries from Table 5")

# -----------------------------
# Table 6: Ellipticities and Isophotal Parameters
# -----------------------------
print("\nReading Table 6: Ellipticities and Isophotal Parameters...")

colspecs_tab6 = [
    (0, 28), (29, 30), (31, 35), (36, 40), (41, 46), (47, 51),
    (52, 58), (59, 64), (65, 69), (70, 74), (75, 80), (81, 85)
]

column_names_tab6 = [
    "NGVS",      # NGVS identifier
    "Class",     # Galaxy classification
    "eps_T",     # Total ellipticity
    "e_eps_T",   # Error in total ellipticity
    "thetaT",    # Position angle (degrees)
    "e_thetaT",  # Error in position angle
    "B4_T",      # Boxyness/Diskyness parameter
    "e_B4_T",    # Error in B4
    "eps_GF",    # Gaussian-filtered ellipticity
    "e_eps_GF",  # Error in GF ellipticity
    "thetaGF",   # GF position angle
    "e_thetaGF"  # Error in GF position angle
]

df_tab6 = pd.read_fwf(
    'Ferrarese2020_tab6.txt',
    colspecs=colspecs_tab6,
    names=column_names_tab6,
    skiprows=37
)
print(f"  Loaded {len(df_tab6)} entries from Table 6")

# -----------------------------
# Table 7: Photometric Colors
# -----------------------------
print("\nReading Table 7: Photometric Colors...")

colspecs_tab7 = [
    (0, 27), (28, 29), (30, 35), (36, 40), (41, 46), (47, 52), (53, 58)
]

column_names_tab7 = [
    "NGVS",  # NGVS identifier
    "Class", # Galaxy classification
    "gmag",  # g-band magnitude (MegaCam)
    "u_g",   # (u-g) color
    "g_r",   # (g-r) color
    "g_i",   # (g-i) color
    "g_z"    # (g-z) color
]

df_tab7 = pd.read_fwf(
    'Ferrarese2020_tab7.txt',
    colspecs=colspecs_tab7,
    names=column_names_tab7,
    skiprows=28
)
print(f"  Loaded {len(df_tab7)} entries from Table 7")

# ==============================================================================
# 3. Query SDSS for Extinction Values
# ==============================================================================
print("\n" + "="*80)
print("STEP 3: Querying SDSS DR18 for Extinction and Photometry")
print("="*80)
print("This step may take a while (querying 404 galaxies)...")

from astroquery.sdss import SDSS

# SQL query template to get SDSS photometry and extinction within 1 arcsec
sql_select = """
SELECT TOP 1
    p.objid, p.ra, p.dec, 
    p.type, p.probPSF, p.clean, p.insideMask, p.flags,
    p.u, p.g, p.r, p.i, p.z,
    p.cModelMag_u, p.cModelMag_g, p.cModelMag_r, p.cModelMag_i, p.cModelMag_z,
    p.cModelMagErr_u, p.cModelMagErr_g, p.cModelMagErr_r, p.cModelMagErr_i, p.cModelMagErr_z,
    p.extinction_u, p.extinction_g, p.extinction_r, p.extinction_i, p.extinction_z,
    p.cModelFlux_u, p.cModelFlux_g, p.cModelFlux_r, p.cModelFlux_i, p.cModelFlux_z,
    p.cModelFluxIvar_u, p.cModelFluxIvar_g, p.cModelFluxIvar_r, p.cModelFluxIvar_i, p.cModelFluxIvar_z,
    p.fiberMag_u, p.fiberMag_g, p.fiberMag_r, p.fiberMag_i, p.fiberMag_z,
    p.fiberMagErr_u, p.fiberMagErr_g, p.fiberMagErr_r, p.fiberMagErr_i, p.fiberMagErr_z,
    p.psfMag_u, p.psfMag_g, p.psfMag_r, p.psfMag_i, p.psfMag_z, 
    p.psfMagErr_u, p.psfMagErr_g, p.psfMagErr_r, p.psfMagErr_i, p.psfMagErr_z,
    p.petroMag_u, p.petroMag_g, p.petroMag_r, p.petroMag_i, p.petroMag_z,
    p.petroMagErr_u, p.petroMagErr_g, p.petroMagErr_r, p.petroMagErr_i, p.petroMagErr_z
FROM PhotoObj AS p
WHERE
    p.ra BETWEEN {ra_min} AND {ra_max} AND
    p.dec BETWEEN {dec_min} AND {dec_max}
ORDER BY
    SQRT(POWER(p.ra - {ra}, 2) + POWER(p.dec - {dec}, 2))
"""

results = []

# Loop through each galaxy and query SDSS
for index, row in tqdm(df_tab4.iterrows(), total=len(df_tab4), desc="Querying SDSS"):
    ra = row['RAdeg']
    dec = row['DEdeg']
    
    # Create coordinate object for input galaxy
    input_coord = SkyCoord(ra=ra*u.deg, dec=dec*u.deg)

    # Define search box (1 arcsec = 1/3600 degrees)
    radius_deg = 1.0 / 3600.0
    ra_min, ra_max = ra - radius_deg, ra + radius_deg
    dec_min, dec_max = dec - radius_deg, dec + radius_deg

    # Format SQL query with coordinates
    query = sql_select.format(
        ra=ra,
        dec=dec,
        ra_min=ra_min,
        ra_max=ra_max,
        dec_min=dec_min,
        dec_max=dec_max
    )

    try:
        # Execute SDSS query
        query_result = SDSS.query_sql(query, timeout=60)
        
        if query_result is not None and len(query_result) > 0:
            # Match found - extract data
            row_dict = dict(query_result[0])
            
            # Calculate angular separation between input and matched coordinates
            matched_coord = SkyCoord(ra=row_dict['ra']*u.deg, dec=row_dict['dec']*u.deg)
            sep_arcsec = input_coord.separation(matched_coord).to(u.arcsec).value
            
            # Add separation and index to result
            row_dict['match_dist_arcsec'] = sep_arcsec
            row_dict['Index'] = index
            results.append(row_dict)
        else:
            # No match found
            results.append({'Index': index, 'match_dist_arcsec': None})
            
    except Exception as e:
        # Query failed
        print(f"\nQuery failed at index {index}: {e}")
        results.append({'Index': index, 'match_dist_arcsec': None})

# Convert results to DataFrame and merge with original Table 4
df_results = pd.DataFrame(results)
df_tab4_matched = df_tab4.merge(df_results, left_index=True, right_on='Index')
print(f"\nSuccessfully matched {len(df_tab4_matched)} galaxies with SDSS")

# ==============================================================================
# 4. Calculate Projected Radial Distance from Virgo Cluster Center
# ==============================================================================
print("\n" + "="*80)
print("STEP 4: Calculating Projected Radial Distances from M87")
print("="*80)

# Define Virgo cluster center coordinates (M87)
virgo_center = SkyCoord(ra=187.7058 * u.deg, dec=12.3911 * u.deg, frame='icrs')
print(f"Virgo center (M87): RA={187.7058} deg, Dec={12.3911} deg")

# Convert each galaxy position to SkyCoord
galaxy_coords = SkyCoord(
    ra=df_tab4_matched['RAdeg'].values * u.deg,
    dec=df_tab4_matched['DEdeg'].values * u.deg, 
    frame='icrs'
)

# Calculate angular separation in arcminutes
separations = virgo_center.separation(galaxy_coords).to(u.arcmin)

# Add projected radial distance to DataFrame
df_tab4_matched['p_radgal'] = separations.value
print(f"Calculated projected distances for {len(df_tab4_matched)} galaxies")
print(f"  Distance range: {separations.value.min():.2f} - {separations.value.max():.2f} arcmin")

# ==============================================================================
# 5. Calculate Redshifts from Velocities
# ==============================================================================
print("\n" + "="*80)
print("STEP 5: Calculating Redshifts from Velocities")
print("="*80)

# Speed of light in km/s
c = 2.998e5

# Calculate redshift: z = v/c
df_tab4_matched['Redshift'] = df_tab4_matched['Vel'] / c
df_tab4_matched['Redshift_Err'] = df_tab4_matched['e_Vel'] / c

print(f"Calculated redshifts for {len(df_tab4_matched)} galaxies")
print(f"  Redshift range: {df_tab4_matched['Redshift'].min():.6f} - {df_tab4_matched['Redshift'].max():.6f}")

# ==============================================================================
# 6. Select Relevant Columns from Matched Data
# ==============================================================================
print("\n" + "="*80)
print("STEP 6: Selecting Relevant Columns")
print("="*80)

# Select columns needed for final catalog
df_tab4_matched_rip = df_tab4_matched[[
    'NGVS',              # Galaxy identifier
    'RAdeg',             # Right Ascension
    'DEdeg',             # Declination
    'match_dist_arcsec', # SDSS match distance
    'Index',             # Original index
    'extinction_u',      # SDSS extinction in u-band
    'extinction_g',      # SDSS extinction in g-band
    'extinction_r',      # SDSS extinction in r-band
    'extinction_i',      # SDSS extinction in i-band
    'extinction_z',      # SDSS extinction in z-band
    'petroMagErr_u',     # Petrosian magnitude error in u-band
    'petroMagErr_g',     # Petrosian magnitude error in g-band
    'petroMagErr_r',     # Petrosian magnitude error in r-band
    'petroMagErr_i',     # Petrosian magnitude error in i-band
    'petroMagErr_z',     # Petrosian magnitude error in z-band
    'Redshift',          # Galaxy redshift
    'Redshift_Err',      # Redshift error
    'p_radgal'           # Projected radial distance from M87
]]

print(f"Selected {len(df_tab4_matched_rip.columns)} columns from matched data")

# ==============================================================================
# 7. Fix Erroneous Values in Table 7
# ==============================================================================
print("\n" + "="*80)
print("STEP 7: Applying Corrections to Table 7")
print("="*80)

# Note: These values in table 7 are NaN (Error)
# We correct them to make r-band magnitude consistent with SDSS r-band magnitude
df_tab7.loc[df_tab7['NGVS'] == "NGVSJ12:28:14.87+11:47:23.6", 'g_r'] = 13.06 - 13.49174
df_tab7.loc[df_tab7['NGVS'] == "NGVSJ12:32:33.49+12:11:55.5", 'g_z'] = 0

print("Applied corrections to 2 galaxies with erroneous color values")

# ==============================================================================
# 8. Convert MegaCam Magnitudes to SDSS System
# ==============================================================================
print("\n" + "="*80)
print("STEP 8: Converting MegaCam Magnitudes to SDSS System")
print("="*80)

df_tab7_rip = df_tab7.copy()

# Step 1: Reconstruct individual MegaCam magnitudes from g-band and color indices
df_tab7_rip['g_Mega'] = df_tab7_rip['gmag']
df_tab7_rip['u_Mega'] = df_tab7_rip['u_g'] + df_tab7_rip['g_Mega']  # u = (u-g) + g
df_tab7_rip['r_Mega'] = df_tab7_rip['g_Mega'] - df_tab7_rip['g_r']  # r = g - (g-r)
df_tab7_rip['i_Mega'] = df_tab7_rip['g_Mega'] - df_tab7_rip['g_i']  # i = g - (g-i)
df_tab7_rip['z_Mega'] = df_tab7_rip['g_Mega'] - df_tab7_rip['g_z']  # z = g - (g-z)

# Step 2: Apply transformation formulas to convert MegaCam to SDSS
# These transformations are from the CFHT MegaCam filter system to SDSS
df_tab7_rip['u_SDSS'] = df_tab7_rip['u_Mega'] + 0.181 * (df_tab7_rip['u_Mega'] - df_tab7_rip['g_Mega'])
df_tab7_rip['g_SDSS'] = df_tab7_rip['g_Mega'] + 0.195 * (df_tab7_rip['g_Mega'] - df_tab7_rip['r_Mega'])
df_tab7_rip['r_SDSS'] = df_tab7_rip['r_Mega'] + 0.011 * (df_tab7_rip['g_Mega'] - df_tab7_rip['r_Mega'])
df_tab7_rip['i_SDSS'] = df_tab7_rip['i_Mega'] - 0.003 * (df_tab7_rip['g_Mega'] - df_tab7_rip['i_Mega'])
df_tab7_rip['z_SDSS'] = df_tab7_rip['z_Mega'] - 0.099 * (df_tab7_rip['i_Mega'] - df_tab7_rip['z_Mega'])

# Reorder columns for clarity
cols_order = [
    'NGVS', 'Class',
    'u_Mega', 'g_Mega', 'r_Mega', 'i_Mega', 'z_Mega',  # MegaCam magnitudes
    'u_SDSS', 'g_SDSS', 'r_SDSS', 'i_SDSS', 'z_SDSS'   # SDSS magnitudes
]
df_tab7_rip = df_tab7_rip[cols_order]

print(f"Converted magnitudes for {len(df_tab7_rip)} galaxies")
print("  MegaCam -> SDSS transformation applied to all 5 bands (ugriz)")

# ==============================================================================
# 9. Merge All Tables
# ==============================================================================
print("\n" + "="*80)
print("STEP 9: Merging Photometric and SDSS Data")
print("="*80)

# Merge photometric colors (Table 7) with SDSS matched data (Table 4)
df_main = pd.merge(df_tab7_rip, df_tab4_matched_rip, on='NGVS', how='inner')

print(f"Final merged catalog contains {len(df_main)} galaxies")
print(f"Total columns: {len(df_main.columns)}")

# ==============================================================================
# 10. Save Final Catalog
# ==============================================================================
print("\n" + "="*80)
print("STEP 10: Saving Final Photometric Catalog")
print("="*80)

output_file = '02.Virgo_core_photcat.csv'
df_main.to_csv(output_file, index=False)

print(f"✓ Successfully saved: {output_file}")
print(f"\nFinal catalog summary:")
print(f"  Number of galaxies: {len(df_main)}")
print(f"  Number of columns: {len(df_main.columns)}")
print(f"\nColumn list:")
for i, col in enumerate(df_main.columns, 1):
    print(f"  {i:2d}. {col}")

print("\n" + "="*80)
print("PROCESSING COMPLETE!")
print("="*80)
