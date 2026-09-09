#!/usr/bin/env python3
"""
Convert Coma Cluster Raw Data to CSV Format

This script converts raw Coma cluster catalog data files to CSV format:
1. Converts .npz master catalog to CSV (with proper byte order handling)
2. Reads and parses redshift text file to CSV

Input files:
    - coma_woody_master_catalog.npz (photometry catalog)
    - coma_woody_datafile2.txt (redshift catalog)

Output files:
    - coma_woody_master_catalog.csv
    - coma_datafile2.csv

Author: Jongin Park
Date: 2026
"""

import os
import numpy as np
import pandas as pd


def convert_npz_to_csv(npz_filename):
    """
    Convert .npz catalog file to CSV format with proper byte order handling.
    
    This function handles:
    - Big-endian to little-endian byte order conversion
    - Byte string to UTF-8 string conversion
    - Proper handling of mixed data types
    
    Parameters
    ----------
    npz_filename : str
        Path to the input .npz file
    
    Returns
    -------
    output_csv : str
        Path to the output CSV file
    """
    print(f"Loading .npz file: {npz_filename}")
    
    # Load the .npz file
    npz_data = np.load(npz_filename, allow_pickle=True)
    
    print(f"  Found {len(npz_data.files)} arrays in .npz file")
    
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
    
    # Build DataFrame and save to CSV
    df = pd.DataFrame(data_dict)
    csv_filename = os.path.splitext(npz_filename)[0] + '.csv'
    df.to_csv(csv_filename, index=False)
    
    print(f"  Saved CSV to: {csv_filename}")
    print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    return csv_filename


def convert_redshift_txt_to_csv(txt_filename, output_csv):
    """
    Read redshift catalog from text file and convert to CSV.
    
    The text file is space-delimited with 72 header lines to skip.
    Column definitions from the catalog documentation.
    
    Parameters
    ----------
    txt_filename : str
        Path to the input text file
    output_csv : str
        Path for the output CSV file
    
    Returns
    -------
    output_csv : str
        Path to the output CSV file
    """
    print(f"\nReading redshift catalog: {txt_filename}")
    
    # Define column names according to the catalog documentation
    colnames = [
        'Seq',          # Sequential number
        'ObjID',        # SDSS Object ID
        'RAdeg',        # Right Ascension (degrees)
        'DEdeg',        # Declination (degrees)
        'rmag',         # SDSS r-band magnitude
        'PointSource',  # Point source flag
        'z',            # Redshift
        'e_z',          # Redshift error
        'r_z',          # Redshift reference/source
        'Member'        # Cluster membership flag
    ]
    
    # Read the space-delimited file
    df = pd.read_csv(
        txt_filename,
        sep=r'\s+',          # Space-separated values (one or more spaces)
        names=colnames,      # Use the column names we defined
        skiprows=72,         # Skip the first 72 header/comment lines
        engine='python'      # Use Python engine for flexible parsing
    )
    
    # Save to CSV
    df.to_csv(output_csv, index=False)
    
    print(f"  Saved CSV to: {output_csv}")
    print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # Print some statistics
    print(f"\n  Redshift statistics:")
    print(f"    Entries with redshift: {(df['z'] > 0).sum():,}")
    print(f"    Redshift range: {df[df['z'] > 0]['z'].min():.4f} - {df[df['z'] > 0]['z'].max():.4f}")
    if 'Member' in df.columns:
        member_counts = df['Member'].value_counts()
        print(f"    Membership flags:")
        for flag, count in member_counts.items():
            print(f"      {flag}: {count:,}")
    
    return output_csv


def main():
    """
    Main function to convert all Coma cluster raw data to CSV format.
    """
    print("="*70)
    print("Coma Cluster Data Conversion: Raw Files → CSV")
    print("="*70)
    
    # Define input file paths
    npz_file = './coma_woody_master_catalog.npz'
    txt_file = './coma_woody_datafile2.txt'
    
    # Define output file paths
    output_redshift_csv = 'coma_datafile2.csv'
    
    # Step 1: Convert NPZ master catalog to CSV
    print("\nSTEP 1: Converting master photometry catalog")
    print("-"*70)
    
    if os.path.exists(npz_file):
        master_csv = convert_npz_to_csv(npz_file)
    else:
        print(f"  ERROR: File not found: {npz_file}")
        print(f"  Skipping master catalog conversion")
        master_csv = None
    
    # Step 2: Convert redshift text file to CSV
    print("\nSTEP 2: Converting redshift catalog")
    print("-"*70)
    
    if os.path.exists(txt_file):
        redshift_csv = convert_redshift_txt_to_csv(txt_file, output_redshift_csv)
    else:
        print(f"  ERROR: File not found: {txt_file}")
        print(f"  Skipping redshift catalog conversion")
        redshift_csv = None
    
    # Print summary
    print("\n" + "="*70)
    print("CONVERSION COMPLETE")
    print("="*70)
    
    print("\nOutput files created:")
    if master_csv and os.path.exists(master_csv):
        size_mb = os.path.getsize(master_csv) / (1024**2)
        print(f"  {master_csv} ({size_mb:.1f} MB)")
    
    if redshift_csv and os.path.exists(redshift_csv):
        size_mb = os.path.getsize(redshift_csv) / (1024**2)
        print(f"  {redshift_csv} ({size_mb:.1f} MB)")
    
    print("\nThese CSV files are ready for downstream analysis.")
    print("="*70)


if __name__ == "__main__":
    main()
