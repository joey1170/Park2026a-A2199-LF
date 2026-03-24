#!/usr/bin/env python3
"""
NED Cross-Matching for Galaxy Catalog

This script cross-matches a photometric galaxy catalog with NED
(NASA/IPAC Extragalactic Database) to obtain spectroscopic redshifts:
1. Loads photometric catalog with RA/Dec coordinates
2. Queries NED for each object within a specified search radius
3. Collects matches with available redshift data (and uncertainty when available)
4. Deduplicates matches by keeping the closest match
5. Saves matched catalog to CSV

The NED database contains spectroscopic redshifts and multi-wavelength
data for millions of extragalactic objects.

Input file:
    - ./z_A2199_Hwang/z_DATA/z_a2199phot21_5DR9_hshwang_35arcmin_cut.csv

Output file:
    - NED_query.csv

Requirements:
    - astroquery
    - astropy
    - pandas
    - tqdm

Author: Jongin Park
Date: 2026
"""

import time
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy import units as u
from astroquery.utils.tap.core import Tap
from tqdm import tqdm


def load_catalog(catalog_path):
    """
    Load photometric catalog from CSV file.
    
    Parameters
    ----------
    catalog_path : str
        Path to the input CSV catalog file
    
    Returns
    -------
    df : pd.DataFrame
        Catalog DataFrame with RA and Dec columns
    """
    print(f"Loading catalog: {catalog_path}")
    df = pd.read_csv(catalog_path)
    print(f"  Loaded {len(df):,} objects")
    
    # Check for required columns
    required_cols = ['p_ra', 'p_dec']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    print(f"  Coordinate range:")
    print(f"    RA: {df['p_ra'].min():.6f} - {df['p_ra'].max():.6f} deg")
    print(f"    Dec: {df['p_dec'].min():.6f} - {df['p_dec'].max():.6f} deg")
    
    return df


def query_ned_for_catalog(df, search_radius_arcsec=1.5, sleep_time=0.0):
    """
    Query NED for each object in the catalog.
    
    For each object, this function:
    1. Creates a SkyCoord with RA/Dec
    2. Runs a NED TAP cone query within the specified radius
    3. Keeps only spectroscopic rows (zflag starts with 'S')
    4. Stores the closest spectroscopic match
    
    Parameters
    ----------
    df : pd.DataFrame
        Input catalog with 'p_ra' and 'p_dec' columns
    search_radius_arcsec : float, optional
        Search radius in arcseconds (default: 1.5)
    sleep_time : float, optional
        Sleep time between queries in seconds (default: 0.0)
        Use this to be polite to NED servers if needed
    
    Returns
    -------
    matched_df : pd.DataFrame
        DataFrame with matched NED objects and their properties
    """
    print(f"\nQuerying NED for {len(df):,} objects")
    print(f"  Search radius: {search_radius_arcsec} arcsec")
    print(f"  Sleep time between queries: {sleep_time} sec")
    print(f"  Include p_objid in output: {'p_objid' in df.columns}")
    print("-"*70)
    
    matched_rows = []
    search_radius_deg = search_radius_arcsec / 3600.0
    tap = Tap(url="https://ned.ipac.caltech.edu/tap")
    
    # Query each object with progress bar
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Querying NED"):
        try:
            # Keep original object id so the match can be traced back later.
            p_objid = row["p_objid"] if "p_objid" in df.columns else None
            if pd.isna(p_objid):
                p_objid = None

            # Create coordinate for this object
            coord = SkyCoord(
                ra=row['p_ra'] * u.deg,
                dec=row['p_dec'] * u.deg,
                frame='icrs'
            )
            
            # Query NED TAP within radius (cone search)
            query = (
                "SELECT prefname, ra, dec, z, zunc, zflag, zrefcode, pretype "
                "FROM NEDTAP.objdir "
                f"WHERE CONTAINS(POINT('J2000', ra, dec), "
                f"CIRCLE('J2000', {row['p_ra']}, {row['p_dec']}, {search_radius_deg})) = 1"
            )
            result = tap.launch_job(query).get_results()

            if len(result) > 0:
                best_match = None
                best_sep_arcsec = None

                for r in result:
                    zflag = str(r["zflag"]).strip().upper()
                    if not zflag.startswith("S"):
                        continue

                    # Skip rows without valid redshift value
                    try:
                        zval = float(r["z"])
                    except Exception:
                        continue

                    # Redshift uncertainty from NEDTAP.objdir.zunc (if available)
                    try:
                        zunc_val = float(r["zunc"])
                        if zunc_val <= 0:
                            zunc_val = None
                    except Exception:
                        zunc_val = None

                    candidate_coord = SkyCoord(
                        ra=float(r["ra"]) * u.deg,
                        dec=float(r["dec"]) * u.deg,
                        frame="icrs",
                    )
                    sep_arcsec = coord.separation(candidate_coord).arcsec

                    if best_sep_arcsec is None or sep_arcsec < best_sep_arcsec:
                        best_sep_arcsec = sep_arcsec
                        best_match = {
                            "p_objid": p_objid,
                            "p_ra": row["p_ra"],
                            "p_dec": row["p_dec"],
                            "ned_name": str(r["prefname"]).strip(),
                            "reference_code": str(r["zrefcode"]).strip(),
                            "redshift": zval,
                            "redshift_uncertainty": zunc_val,
                            "ned_ra": float(r["ra"]),
                            "ned_dec": float(r["dec"]),
                            "type": str(r["pretype"]).strip(),
                            "separation_arcsec": sep_arcsec,
                        }

                if best_match is not None:
                    matched_rows.append(best_match)
            
            # Optional sleep to avoid overloading NED servers
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        except Exception as e:
            # Log errors but continue processing
            tqdm.write(f"  ⚠️  Error at index {idx}: {e}")
            continue
    
    # Convert results to DataFrame
    matched_df = pd.DataFrame(matched_rows)
    
    print(f"\n✅ Matching complete:")
    print(f"  Objects with NED matches: {len(matched_df):,} / {len(df):,}")
    print(f"  Match rate: {len(matched_df)/len(df)*100:.1f}%")
    
    return matched_df


def deduplicate_matches(matched_df):
    """
    Deduplicate matches by keeping the closest match for each NED object.
    
    If the same NED object is matched to multiple catalog objects,
    keep only the match with the smallest angular separation.
    
    Parameters
    ----------
    matched_df : pd.DataFrame
        DataFrame with matched NED objects
    
    Returns
    -------
    deduped_df : pd.DataFrame
        Deduplicated DataFrame
    """
    print("\nDeduplicating matches...")
    print(f"  Before deduplication: {len(matched_df):,} matches")
    
    # Convert separation to float if needed
    matched_df['separation_arcsec'] = matched_df['separation_arcsec'].astype(float)
    
    # Sort by separation and drop duplicates, keeping closest match
    deduped_df = (
        matched_df
        .sort_values(by='separation_arcsec')
        .drop_duplicates(subset='ned_name', keep='first')
        .reset_index(drop=True)
    )
    
    print(f"  After deduplication: {len(deduped_df):,} matches")
    print(f"  Removed {len(matched_df) - len(deduped_df)} duplicate NED objects")
    
    return deduped_df


def print_match_statistics(matched_df):
    """
    Print statistics about the matched catalog.
    
    Parameters
    ----------
    matched_df : pd.DataFrame
        Matched and deduplicated catalog
    """
    print("\n" + "="*70)
    print("MATCHING STATISTICS")
    print("="*70)
    
    print(f"\nTotal matched objects: {len(matched_df):,}")
    
    # Redshift statistics
    z_data = matched_df['redshift']
    print(f"\nRedshift statistics:")
    print(f"  Min: {z_data.min():.6f}")
    print(f"  Max: {z_data.max():.6f}")
    print(f"  Median: {z_data.median():.6f}")
    print(f"  Mean: {z_data.mean():.6f}")
    
    # Separation statistics
    sep_data = matched_df['separation_arcsec']
    print(f"\nSeparation statistics:")
    print(f"  Min: {sep_data.min():.4f} arcsec")
    print(f"  Max: {sep_data.max():.4f} arcsec")
    print(f"  Median: {sep_data.median():.4f} arcsec")
    print(f"  Mean: {sep_data.mean():.4f} arcsec")
    
    # Object types
    print(f"\nObject types:")
    type_counts = matched_df['type'].value_counts()
    for obj_type, count in type_counts.head(10).items():
        print(f"  {obj_type}: {count:,} ({count/len(matched_df)*100:.1f}%)")
    
    if len(type_counts) > 10:
        print(f"  ... and {len(type_counts) - 10} more types")


def main():
    """
    Main function to run NED cross-matching pipeline.
    """
    print("="*70)
    print("NED Cross-Matching for Galaxy Catalog")
    print("="*70)
    
    # Configuration
    catalog_path = './z_A2199_Hwang/z_DATA/z_a2199phot21_5DR9_hshwang_35arcmin_cut.csv'
    output_path = './NED/A2199_NED_query.csv'
    search_radius_arcsec = 1.5  # Search radius in arcseconds
    sleep_time = 0.0  # Sleep between queries (seconds)
    
    # Step 1: Load catalog
    print("\nSTEP 1: Loading photometric catalog")
    print("-"*70)
    df = load_catalog(catalog_path)

    # Step 2: Query NED for each object
    print("\nSTEP 2: Querying NED database")
    print("-"*70)
    matched_df = query_ned_for_catalog(
        df,
        search_radius_arcsec=search_radius_arcsec,
        sleep_time=sleep_time
    )
    
    # Check if any matches were found
    if len(matched_df) == 0:
        print("\n❌ No matches found in NED. Exiting.")
        return
    
    # Step 3: Deduplicate matches
    print("\nSTEP 3: Deduplicating matches")
    print("-"*70)
    deduped_df = deduplicate_matches(matched_df)
    
    # Step 4: Print statistics
    print_match_statistics(deduped_df)
    
    # Step 5: Save to CSV
    print("\n" + "="*70)
    print("SAVING RESULTS")
    print("="*70)
    deduped_df.to_csv(output_path, index=False)
    print(f"\n✅ Saved {len(deduped_df):,} matched objects to: {output_path}")
    
    # Show column info
    print(f"\nOutput columns:")
    for col in deduped_df.columns:
        print(f"  - {col}")
    
    print("\n" + "="*70)
    print("PROCESSING COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
