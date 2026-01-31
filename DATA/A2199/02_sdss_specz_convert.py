#!/usr/bin/env python3
"""
Convert SDSS DR17 Spectroscopic Catalog from IDL to CSV

This script converts SDSS DR17 spectroscopic redshift catalog from
IDL .sav format to CSV format for easy use with Python/pandas:
1. Reads IDL .sav file using scipy
2. Converts to .npz intermediate format
3. Handles byte order and string encoding
4. Exports to CSV format

The SDSS DR17 spectroscopic catalog contains redshifts, coordinates,
and spectroscopic information for galaxies observed by SDSS.

Input file:
    - ./DR17SDSScat/Mgaldr17_id.sav (IDL format)

Output files:
    - ./DR17SDSScat/Mgaldr17_id.npz (intermediate)
    - ./DR17SDSScat/Mgaldr17_id.csv (final)

Requirements:
    - scipy (for reading .sav files)
    - numpy
    - pandas

Author: Jongin Park
Date: 2026
"""

import os
import numpy as np
import pandas as pd
from scipy.io import readsav


def convert_sav_to_npz(sav_filepath):
    """
    Convert IDL .sav file to numpy .npz format.
    
    IDL .sav files are a binary format used by IDL (Interactive Data Language).
    This function reads the .sav file and converts it to a more Python-friendly
    .npz format.
    
    Parameters
    ----------
    sav_filepath : str
        Path to the input .sav file
    
    Returns
    -------
    npz_filepath : str
        Path to the output .npz file
    """
    print(f"Reading IDL .sav file: {sav_filepath}")
    
    # Read the .sav file
    sav_data = readsav(sav_filepath)
    
    # Convert AttrDict to regular dictionary
    sav_dict = dict(sav_data)
    
    print(f"  Found {len(sav_dict)} arrays in .sav file")
    print(f"  Arrays: {', '.join(sav_dict.keys())}")
    
    # Create output path
    npz_filepath = sav_filepath.replace('.sav', '.npz')
    
    # Save to .npz format
    np.savez(npz_filepath, **sav_dict)
    
    print(f"  Saved to: {npz_filepath}")
    
    return npz_filepath


def convert_npz_to_csv(npz_filepath):
    """
    Convert .npz file to CSV with proper data type handling.
    
    This function:
    - Loads the .npz file
    - Handles big-endian to little-endian byte order conversion
    - Converts byte strings to UTF-8 strings
    - Exports to CSV format
    
    Parameters
    ----------
    npz_filepath : str
        Path to the input .npz file
    
    Returns
    -------
    csv_filepath : str
        Path to the output CSV file
    """
    print(f"\nConverting .npz to CSV: {npz_filepath}")
    
    # Load the .npz file
    npz_data = np.load(npz_filepath, allow_pickle=True)
    
    print(f"  Processing {len(npz_data.files)} arrays...")
    
    # Convert to native byte order and handle byte strings
    data_dict = {}
    for key in npz_data.files:
        arr = npz_data[key]
        
        # Handle byte order (convert big-endian to native/little-endian)
        if arr.dtype.byteorder == '>' or (arr.dtype.byteorder == '=' and not np.little_endian):
            arr = arr.byteswap().newbyteorder()
        
        # Convert byte strings to regular UTF-8 strings
        if arr.dtype.kind in {'S', 'O'}:  # S = bytes, O = object (might contain bytes)
            arr = np.array([x.decode('utf-8') if isinstance(x, bytes) else x for x in arr])
        
        data_dict[key] = arr
    
    # Build DataFrame
    df = pd.DataFrame(data_dict)
    
    # Create output path
    csv_filepath = os.path.splitext(npz_filepath)[0] + '.csv'
    
    # Save to CSV
    df.to_csv(csv_filepath, index=False)
    
    print(f"  Saved to: {csv_filepath}")
    print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    return csv_filepath, df


def print_catalog_info(df):
    """
    Print summary information about the catalog.
    
    Parameters
    ----------
    df : pd.DataFrame
        The catalog DataFrame
    """
    print("\n" + "="*70)
    print("CATALOG INFORMATION")
    print("="*70)
    
    print(f"\nTotal objects: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")
    
    # Show column names
    print(f"\nColumns ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # Show coordinate range if available
    if 's3_ra' in df.columns and 's3_dec' in df.columns:
        print(f"\nCoordinate range:")
        print(f"  RA:  {df['s3_ra'].min():.6f} - {df['s3_ra'].max():.6f} deg")
        print(f"  Dec: {df['s3_dec'].min():.6f} - {df['s3_dec'].max():.6f} deg")
    
    # Show redshift range if available
    if 's3_z' in df.columns:
        z_valid = df['s3_z'][df['s3_z'] > -999]  # Filter invalid values
        if len(z_valid) > 0:
            print(f"\nRedshift statistics:")
            print(f"  Valid redshifts: {len(z_valid):,} / {len(df):,}")
            print(f"  Range: {z_valid.min():.6f} - {z_valid.max():.6f}")
            print(f"  Median: {z_valid.median():.6f}")
    
    # Show data types
    print(f"\nData types:")
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        print(f"  {dtype}: {count} columns")


def main():
    """
    Main function to convert SDSS DR17 catalog from .sav to CSV.
    """
    print("="*70)
    print("SDSS DR17 Spectroscopic Catalog Conversion")
    print("IDL .sav → .npz → CSV")
    print("="*70)
    
    # Define input file path
    sav_file = './DR17SDSScat/Mgaldr17_id.sav'
    
    # Check if input file exists
    if not os.path.exists(sav_file):
        print(f"\n❌ Error: Input file not found: {sav_file}")
        print(f"   Please ensure the SDSS DR17 catalog file is in the correct location.")
        return
    
    # Step 1: Convert .sav to .npz
    print("\nSTEP 1: Converting IDL .sav to .npz")
    print("-"*70)
    npz_file = convert_sav_to_npz(sav_file)
    
    # Step 2: Convert .npz to CSV
    print("\nSTEP 2: Converting .npz to CSV")
    print("-"*70)
    csv_file, df = convert_npz_to_csv(npz_file)
    
    # Step 3: Print catalog information
    print_catalog_info(df)
    
    # Final summary
    print("\n" + "="*70)
    print("CONVERSION COMPLETE")
    print("="*70)
    
    print(f"\nOutput files:")
    
    # Check file sizes
    for filepath in [npz_file, csv_file]:
        if os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024**2)
            print(f"  ✓ {filepath} ({size_mb:.1f} MB)")
    
    print(f"\nThe CSV file is ready for use:")
    print(f"  → {csv_file}")
    print(f"\nThis file contains SDSS DR17 spectroscopic redshifts")
    print(f"and can be used in downstream analysis (e.g., 03.Merge_mastercat.ipynb)")
    
    print("="*70)


if __name__ == "__main__":
    main()
