#!/usr/bin/env python3
"""
Merge Master Catalog for A2199 Cluster

This script merges spectroscopic redshift data from multiple sources
into a master photometric catalog for the A2199 galaxy cluster:
1. Loads base photometric catalog
2. Merges NED spectroscopic redshifts (coordinate matching)
3. Merges SDSS DR17 spectroscopic redshifts (object ID matching)
4. Merges DESI spectroscopic redshifts (coordinate matching)
5. Determines unified final redshift columns as in 03.Merge_mastercat.ipynb
6. Saves final merged catalog

Input files:
    - ./z_A2199_Hwang/z_DATA/z_a2199phot21_5DR9_hshwang_35arcmin_cut.csv
    - ./NED/A2199_NED_query.csv
    - ./DR17SDSScat/Mgaldr17_id.csv
    - ./DESI/A2199_DESI_specz_within35arcmin.csv

Output file:
    - A2199_mastercat_intermediate_file0.csv

Author: Jongin Park
Date: 2026 (revised 2024-06 for final z columns)
"""

import os
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy import units as u

def load_catalogs():
    print("="*70)
    print("LOADING INPUT CATALOGS")
    print("="*70)
    print("\n1. Loading base photometric catalog...")
    df_main = pd.read_csv('./z_A2199_Hwang/z_DATA/z_a2199phot21_5DR9_hshwang_35arcmin_cut.csv')
    print(f"   → {len(df_main):,} objects")
    print("\n2. Loading NED redshift catalog...")
    df_ned = pd.read_csv('./NED/A2199_NED_query.csv')
    print(f"   → {len(df_ned):,} objects with NED redshifts")
    print("\n3. Loading SDSS DR17 spectroscopic catalog...")
    df_sdss = pd.read_csv('./DR17SDSScat/Mgaldr17_id.csv', low_memory=False)
    print(f"   → {len(df_sdss):,} SDSS spectra")
    print("\n4. Loading DESI spectroscopic catalog...")
    df_desi = pd.read_csv('./DESI/A2199_DESI_specz_within35arcmin.csv')
    print(f"   → {len(df_desi):,} DESI spectra")
    return df_main, df_ned, df_sdss, df_desi

def prepare_ned_catalog(df_ned):
    print("\nPreparing NED catalog...")
    df_ned_clean = df_ned.copy()
    df_ned_clean['z_ned_z'] = df_ned_clean['redshift'].astype(float)

    # Use uncertainty from NED query output when available.
    # Rule: NaN or negative uncertainty -> -9.
    if 'redshift_uncertainty' in df_ned_clean.columns:
        zerr = pd.to_numeric(df_ned_clean['redshift_uncertainty'], errors='coerce')
        df_ned_clean['z_ned_zerr'] = zerr.where((~zerr.isna()) & (zerr >= 0), -9.0)
    else:
        df_ned_clean['z_ned_zerr'] = -9.0

    df_ned_clean['z_ned_name'] = df_ned_clean['ned_name']
    df_ned_clean = df_ned_clean[['p_ra', 'p_dec', 'z_ned_name', 'z_ned_z', 'z_ned_zerr']]
    print(f"   → Prepared {len(df_ned_clean):,} NED entries")
    return df_ned_clean

def merge_ned_redshifts(df_main, df_ned_clean):
    print("\n" + "="*70)
    print("STEP 1: MERGING NED REDSHIFTS")
    print("="*70)
    df_merged = pd.merge(
        df_main,
        df_ned_clean,
        on=['p_ra', 'p_dec'],
        how='outer'
    )
    df_merged['z_ned_z'] = df_merged['z_ned_z'].fillna(-9)
    df_merged['z_ned_zerr'] = df_merged['z_ned_zerr'].fillna(-9)
    df_merged['z_ned_name'] = df_merged['z_ned_name'].fillna('NN')
    n_matched = (df_merged['z_ned_z'] != -9).sum()
    print(f"\n✅ NED merge complete:")
    print(f"   Total objects: {len(df_merged):,}")
    print(f"   Objects with NED z: {n_matched:,}")
    print(f"   Match rate: {n_matched/len(df_merged)*100:.1f}%")
    return df_merged

def prepare_sdss_catalog(df_sdss):
    print("\nPreparing SDSS catalog...")
    df_sdss_clean = df_sdss.copy()
    df_sdss_clean['z_sdss_z'] = df_sdss_clean['s3_z'].astype(float)
    df_sdss_clean['z_sdss_zerr'] = df_sdss_clean['s3_zerr'].astype(float)
    df_sdss_clean['s3_objid'] = df_sdss_clean['s3_objid'].astype('Int64')
    df_sdss_clean = df_sdss_clean[['s3_objid', 'z_sdss_z', 'z_sdss_zerr']]
    print(f"   → Prepared {len(df_sdss_clean):,} SDSS entries")
    return df_sdss_clean

def merge_sdss_redshifts(df_main, df_sdss_clean):
    print("\n" + "="*70)
    print("STEP 2: MERGING SDSS DR17 REDSHIFTS")
    print("="*70)
    df_merged = pd.merge(
        df_main,
        df_sdss_clean,
        left_on='p_objid',
        right_on='s3_objid',
        how='left'
    )
    if 's3_objid' in df_merged.columns:
        df_merged = df_merged.drop(columns=['s3_objid'])
    df_merged['z_sdss_z'] = df_merged['z_sdss_z'].fillna(-9)
    df_merged['z_sdss_zerr'] = df_merged['z_sdss_zerr'].fillna(-9)
    n_matched = (df_merged['z_sdss_z'] != -9).sum()
    print(f"\n✅ SDSS merge complete:")
    print(f"   Total objects: {len(df_merged):,}")
    print(f"   Objects with SDSS z: {n_matched:,}")
    print(f"   Match rate: {n_matched/len(df_merged)*100:.1f}%")
    return df_merged

def prepare_desi_catalog(df_desi):
    print("\nPreparing DESI catalog...")
    desi_columns = ['TARGETID', 'SURVEY', 'Z', 'ZERR', 'TARGET_RA', 'TARGET_DEC',
                    'FLUX_R', 'FLUX_IVAR_R']
    available_cols = [col for col in desi_columns if col in df_desi.columns]
    df_desi_clean = df_desi[available_cols].copy()
    df_desi_clean = df_desi_clean.rename(columns={
        'Z': 'z_desi_z',
        'ZERR': 'z_desi_zerr',
        'TARGETID': 'z_desi_id'
    })
    print(f"   → Prepared {len(df_desi_clean):,} DESI entries")
    return df_desi_clean

def merge_desi_redshifts(df_main, df_desi_clean, match_radius_arcsec=1.5):
    print("\n" + "="*70)
    print("STEP 3: MERGING DESI REDSHIFTS")
    print("="*70)
    print(f"   Match radius: {match_radius_arcsec} arcsec")
    print("\n   Creating coordinate objects...")
    coords_main = SkyCoord(
        ra=df_main['p_ra'].values * u.deg,
        dec=df_main['p_dec'].values * u.deg,
        frame='icrs'
    )
    coords_desi = SkyCoord(
        ra=df_desi_clean['TARGET_RA'].values * u.deg,
        dec=df_desi_clean['TARGET_DEC'].values * u.deg,
        frame='icrs'
    )
    print("   Matching coordinates...")
    idx, d2d, _ = coords_desi.match_to_catalog_sky(coords_main)
    match_radius = match_radius_arcsec * u.arcsec
    match_mask = d2d <= match_radius
    print(f"   → Found {match_mask.sum():,} matches within {match_radius_arcsec} arcsec")
    matched_desi_rows = df_desi_clean[match_mask].reset_index(drop=True)
    matched_idx_in_main = idx[match_mask]
    desi_columns = [col for col in df_desi_clean.columns 
                    if col not in ['TARGET_RA', 'TARGET_DEC']]
    df_desi_matched = pd.DataFrame(index=df_main.index, columns=desi_columns)
    df_desi_matched.loc[matched_idx_in_main] = matched_desi_rows[desi_columns].values
    df_merged = pd.concat([df_main.reset_index(drop=True), 
                          df_desi_matched.reset_index(drop=True)], axis=1)
    df_merged['z_desi_z'] = df_merged['z_desi_z'].fillna(-9)
    df_merged['z_desi_zerr'] = df_merged['z_desi_zerr'].fillna(-9)
    df_merged['z_desi_id'] = df_merged['z_desi_id'].fillna('NN')
    n_matched = (df_merged['z_desi_z'] != -9).sum()
    print(f"\n✅ DESI merge complete:")
    print(f"   Total objects: {len(df_merged):,}")
    print(f"   Objects with DESI z: {n_matched:,}")
    print(f"   Match rate: {n_matched/len(df_merged)*100:.1f}%")
    return df_merged

def determine_final_redshift_columns(df):
    """
    Set the unified/final redshift columns on the catalog, as in 03.Merge_mastercat.ipynb.
    
    Follows:
        - z_tot_z: first available (good) z from MMT, DESI, SDSS, NED
          (priority: MMT > DESI > SDSS > NED)
        - z_tot_zsource: which catalog the z_tot_z comes from
          ("MMT", "DESI", "SDSS", "NED", "none")
        - z_tot_zerr: corresponding z uncertainty
    
    Columns added:
        - z_tot_z, z_tot_zsource, z_tot_zerr
    """
    print("\n" + "="*70)
    print("STEP 4: DETERMINING FINAL REDSHIFT COLUMNS (z_tot_z, etc)")
    print("="*70)
    # Use -9 as missing value
    z_mmt_z = df['z_mmt_z'].values
    z_desi_z = df['z_desi_z'].values
    z_sdss_z = df['z_sdss_z'].values
    z_ned_z = df['z_ned_z'].values

    z_mmt_zerr = df['z_mmt_zerr'].values
    z_desi_zerr = df['z_desi_zerr'].values
    z_sdss_zerr = df['z_sdss_zerr'].values
    z_ned_zerr = df['z_ned_zerr'].values

    # Boolean masks for valid z
    has_mmt  = z_mmt_z > -9
    has_desi = (~has_mmt) & (z_desi_z > -9)
    has_sdss = (~has_mmt) & (~has_desi) & (z_sdss_z > -9)
    has_ned  = (~has_mmt) & (~has_desi) & (~has_sdss) & (z_ned_z > -9)

    # Final redshift value
    z_tot_z = np.where(has_mmt, z_mmt_z,
                  np.where(has_desi, z_desi_z,
                  np.where(has_sdss, z_sdss_z,
                    np.where(has_ned, z_ned_z, -9)
                  )))

    # Final redshift source
    z_tot_zsource = np.where(has_mmt, 'MMT',
                     np.where(has_desi, 'DESI',
                     np.where(has_sdss, 'SDSS',
                       np.where(has_ned, 'NED', 'none'))))

    z_tot_zerr   = np.where(has_mmt, z_mmt_zerr,
                     np.where(has_desi, z_desi_zerr,
                     np.where(has_sdss, z_sdss_zerr,
                       np.where(has_ned, z_ned_zerr, -9)
                     )))

    df['z_tot_z']      = z_tot_z
    df['z_tot_zsource'] = z_tot_zsource
    df['z_tot_zerr']   = z_tot_zerr

    # For summary
    n_tot_z = (z_tot_z > -9).sum()
    print(f"   Objects with z_tot_z > -9: {n_tot_z:,} ({n_tot_z/len(df)*100:.1f}%)")
    print("   Redshift source counts:")
    for _src in ['MMT', 'DESI', 'SDSS', 'NED', 'none']:
        print(f"      {_src:4s}: {(z_tot_zsource==_src).sum():,}")

    return df

def print_merge_summary(df_final, extra_final_columns=True):
    print("\n" + "="*70)
    print("MERGE SUMMARY")
    print("="*70)
    print(f"\nTotal objects in final catalog: {len(df_final):,}")
    n_mmt = (df_final['z_mmt_z'] > -9).sum()
    n_ned = (df_final['z_ned_z'] > -9).sum()
    n_sdss = (df_final['z_sdss_z'] > -9).sum()
    n_desi = (df_final['z_desi_z'] > -9).sum()
    has_any_z = ((df_final['z_mmt_z'] > -9) |
                 (df_final['z_ned_z'] > -9) | 
                 (df_final['z_sdss_z'] > -9) | 
                 (df_final['z_desi_z'] > -9))
    n_any_z = has_any_z.sum()
    print(f"\nRedshift source statistics:")
    print(f"   MMT:  {n_mmt:,} ({n_mmt/len(df_final)*100:.1f}%)")
    print(f"   NED:  {n_ned:,} ({n_ned/len(df_final)*100:.1f}%)")
    print(f"   SDSS: {n_sdss:,} ({n_sdss/len(df_final)*100:.1f}%)")
    print(f"   DESI: {n_desi:,} ({n_desi/len(df_final)*100:.1f}%)")
    print(f"   Any:  {n_any_z:,} ({n_any_z/len(df_final)*100:.1f}%)")
    n_multiple = ((df_final['z_mmt_z'] > -9).astype(int) +
                 (df_final['z_ned_z'] > -9).astype(int) +
                  (df_final['z_sdss_z'] > -9).astype(int) +
                  (df_final['z_desi_z'] > -9).astype(int)) > 1
    print(f"   Multiple sources: {n_multiple.sum():,} ({n_multiple.sum()/len(df_final)*100:.1f}%)")
    if extra_final_columns and "z_tot_z" in df_final.columns:
        n_tot = (df_final["z_tot_z"] > -9).sum()
        print(f"   z_tot_z  set for: {n_tot:,} ({n_tot/len(df_final)*100:.1f}%)")
        for _src in ["MMT", "DESI", "SDSS", "NED", "none"]:
            print(f"      z_tot_zsource={_src:4s}: {(df_final['z_tot_zsource']==_src).sum():,}")
    print(f"\nFinal catalog columns: {len(df_final.columns)}")

def main():
    print("="*70)
    print("A2199 MASTER CATALOG MERGER")
    print("="*70)
    print("\nMerging spectroscopic redshifts from NED, SDSS DR17, and DESI")
    print("into photometric master catalog")
    # Step 0: Load all catalogs
    df_main, df_ned, df_sdss, df_desi = load_catalogs()
    # Step 1: Merge NED redshifts
    df_ned_clean = prepare_ned_catalog(df_ned)
    df_main = merge_ned_redshifts(df_main, df_ned_clean)
    # Step 2: Merge SDSS redshifts
    df_sdss_clean = prepare_sdss_catalog(df_sdss)
    df_main = merge_sdss_redshifts(df_main, df_sdss_clean)
    # Step 3: Merge DESI redshifts
    df_desi_clean = prepare_desi_catalog(df_desi)
    df_main = merge_desi_redshifts(df_main, df_desi_clean, match_radius_arcsec=1.5)
    # Step 4: Determine unified final redshift columns as 03.Merge_mastercat.ipynb
    df_main = determine_final_redshift_columns(df_main)
    # Print summary (include info on z_tot_z etc)
    print_merge_summary(df_main, extra_final_columns=True)
    print("\n" + "="*70)
    print("SAVING MERGED CATALOG")
    print("="*70)
    output_file = 'A2199_mastercat_intermediate_file0.csv'
    df_main.to_csv(output_file, index=False)
    file_size_mb = os.path.getsize(output_file) / (1024**2)
    print(f"\n✅ Saved merged catalog to: {output_file}")
    print(f"   File size: {file_size_mb:.1f} MB")
    print(f"   Objects: {len(df_main):,}")
    print(f"   Columns: {len(df_main.columns)}")
    print("\n" + "="*70)
    print("MERGING COMPLETE")
    print("="*70)
    print("\nThe merged catalog is ready for downstream analysis")
    print("(e.g., membership determination, k-corrections)")

if __name__ == "__main__":
    main()
