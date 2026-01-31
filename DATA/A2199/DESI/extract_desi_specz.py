#!/usr/bin/env python3
"""
Extract DESI Spectroscopic Redshifts for A2199 Cluster Only

This script extracts DESI spectroscopic redshifts for galaxies within a
specified radius of the A2199 cluster only:
1. Loads cluster catalog (AllHeCS VAC)
2. Selects only CLID='A2199'
3. Reads DESI spectroscopic catalog from FITS file
4. Finds all DESI sources within radius of A2199
5. Saves matched sources to a CSV file

Input files:
    - ../../AllHeCS_VAC_updated.csv (cluster catalog)
    - ../../../DATA/DESI_redshift/zall-pix-iron.fits (DESI spectroscopy)

Output file:
    - A2199_DESI_specz_within{radius}arcmin.csv

Author: Jongin Park
Date: 2026
"""

import os
import numpy as np
import pandas as pd
import fitsio
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy import units as u

def load_a2199_row(catalog_path):
    """
    Load only the row for CLID='A2199' from the cluster catalog.
    """
    print(f"Loading cluster catalog: {catalog_path}")
    allhecs = pd.read_csv(catalog_path)
    thisrow = allhecs[allhecs['CLID'] == 'A2199']
    if thisrow.empty:
        raise ValueError("A2199 not found in cluster catalog")
    print("  Found CLID='A2199'")
    return thisrow.iloc[0]  # as Series

def load_desi_catalog(fits_path, columns=None):
    """
    Load DESI spectroscopic redshift catalog from FITS file.
    """
    print(f"\nLoading DESI spectroscopic catalog: {fits_path}")
    if columns is None:
        columns = [
            'TARGETID',
            'SURVEY',
            'Z',
            'ZERR',
            'TARGET_RA',
            'TARGET_DEC',
            'FLUX_R',
            'FLUX_IVAR_R'
        ]
    print(f"  Reading {len(columns)} columns from FITS file...")
    f = fitsio.FITS(fits_path)
    subset = f[1].read(columns=columns)
    desi_table = Table(subset)
    print(f"  Loaded {len(desi_table):,} DESI sources")
    print(f"  Columns: {', '.join(desi_table.colnames)}")
    return desi_table

def extract_sources_for_a2199(desi_table, cluster_row, radius_arcmin=35):
    """
    Extract DESI sources within specified radius of A2199 only.
    """
    print(f"\nExtracting DESI sources within {radius_arcmin} arcmin of A2199")
    print("-"*70)
    desi_coords = SkyCoord(
        ra=desi_table['TARGET_RA'] * u.deg,
        dec=desi_table['TARGET_DEC'] * u.deg,
        frame='icrs'
    )
    clid = cluster_row['CLID']
    ra = cluster_row['RA']
    dec = cluster_row['DEC']
    cluster_center = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')
    search_radius = radius_arcmin * u.arcmin
    separations = desi_coords.separation(cluster_center)
    within_radius = separations <= search_radius
    matched_sources = desi_table[within_radius]
    output_filename = f"{clid}_DESI_specz_within{radius_arcmin:.0f}arcmin.csv"
    matched_sources.write(output_filename, format="csv", overwrite=True)
    print(f"  ✅ {clid}: {len(matched_sources):,} sources → {output_filename}")
    return {clid: len(matched_sources)}

def print_summary(results, radius_arcmin):
    """
    Print summary statistics of extraction results.
    """
    print("\n" + "="*70)
    print("EXTRACTION COMPLETE")
    print("="*70)
    print(f"\nSummary:")
    print(f"  Search radius: {radius_arcmin} arcmin")
    print(f"  Cluster: A2199")
    print(f"  Number of DESI sources extracted: {results['A2199']:,}")
    filename = f"A2199_DESI_specz_within{radius_arcmin:.0f}arcmin.csv"
    if os.path.exists(filename):
        size_mb = os.path.getsize(filename) / (1024**2)
        print(f"\nOutput file created:")
        print(f"  ✓ {filename} ({size_mb:.2f} MB)")
    print("="*70)

def main():
    """
    Main function to extract DESI spectroscopic redshifts for A2199 cluster only.
    """
    print("="*70)
    print("DESI Spectroscopic Redshift Extraction for A2199 Only")
    print("="*70)
    # Configuration
    cluster_catalog_path = '../../AllHeCS_VAC_updated.csv'
    desi_fits_path = '../../../DATA/DESI_redshift/zall-pix-iron.fits'
    search_radius_arcmin = 35
    # Step 1: Load only the A2199 row
    print("\nSTEP 1: Loading cluster catalog and selecting A2199")
    print("-"*70)
    cluster_row = load_a2199_row(cluster_catalog_path)
    # Step 2: Load DESI spectroscopic catalog
    print("\nSTEP 2: Loading DESI catalog")
    print("-"*70)
    desi_table = load_desi_catalog(desi_fits_path)
    # Step 3: Extract sources for A2199
    print("\nSTEP 3: Matching DESI sources to A2199")
    print("-"*70)
    results = extract_sources_for_a2199(
        desi_table,
        cluster_row,
        radius_arcmin=search_radius_arcmin
    )
    # Step 4: Print summary
    print_summary(results, search_radius_arcmin)

if __name__ == "__main__":
    main()
