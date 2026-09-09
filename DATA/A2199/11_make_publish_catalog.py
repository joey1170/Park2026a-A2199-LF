#!/usr/bin/env python3
"""
Build the machine-readable redshift table of A2199 (Table 2 of the paper)

Selects the objects with a redshift within 35 arcmin of the cluster centre from
the final master catalog, maps the redshift source (and, for NED redshifts, the
literature reference) to an integer code, rounds redshifts to 0.0001, and writes
a fixed-width table with a byte-by-byte header.

Input files:
    - ./A2199_mastercat_within35arcmin.csv (from 10_membership.py)
    - ./NED/A2199_NED_query.csv (from 01_ned_matching.py; NED reference codes)

Output file:
    - A2199_Machine_Readable_Table2.txt

Author: Jongin Park
Date: 2026
"""

import pandas as pd


def build_df_mrt(master_path="./A2199_mastercat_within35arcmin.csv",
                 ned_query_path="./NED/A2199_NED_query.csv"):
    """
    Build the table of NED redshifts with their reference codes:
      1) load master catalog
      2) select rows with z_tot_zsource == 'NED'
      3) merge NED reference_code from NED query table by (p_ra, p_dec)
    """
    df = pd.read_csv(master_path)
    df_ned = df[df["z_tot_zsource"] == "NED"].copy()
    ned_query_df = pd.read_csv(ned_query_path)

    df_mrt = df_ned[
        [
            "p_objid",
            "p_ra",
            "p_dec",
            "p_petromag_r_0",
            "extended_source_flag",
            "photflag",
            "z_tot_z",
            "z_tot_zerr",
            "z_tot_zsource",
            "member",
        ]
    ].copy()

    # (p_ra, p_dec) are identical in both tables
    df_mrt = df_mrt.merge(
        ned_query_df[["p_ra", "p_dec", "reference_code"]],
        on=["p_ra", "p_dec"],
        how="left",
    )

    return df, df_mrt


def main():
    # 1) NED reference codes
    df_master, df_mrt = build_df_mrt()

    # 2) Keep only objects within 35 arcmin and with valid z
    tempdf = df_master[df_master["p_radgal"] <= 35].copy()
    tempdf = tempdf[tempdf["z_tot_z"] != -9].copy()

    # 3) Publication columns
    pubcat = tempdf[
        [
            "p_objid",
            "p_ra",
            "p_dec",
            "p_petromag_r_0",
            "extended_source_flag",
            "photflag",
            "z_tot_z",
            "z_tot_zerr",
            "z_tot_zsource",
            "member",
        ]
    ].reset_index(drop=True)

    # 4) Map member flag from string to int
    pubcat["member"] = pubcat["member"].map({"N": 0, "Y": 1})

    # 5) Base z source flags for non-NED rows
    zsource_map = {"mmt": 1, "sdss": 2, "desi": 3}
    pubcat["z_tot_zsource_flag"] = (
        pubcat["z_tot_zsource"].str.lower().map(zsource_map).fillna(-9).astype(int)
    )

    # 6) NED reference map (only currently used reference codes)
    #    array(['2016SDSSD.C...0000:', '2017ApJ...842...88S', '2023ApJS..267...27Z'])
    ned_ref_map = {
        "2016SDSSD.C...0000:": 4,
        "2017ApJ...842...88S": 5,
        "2023ApJS..267...27Z": 6,
    }

    # 7) Override NED rows using df_mrt reference_code by p_objid
    df_mrt = df_mrt[["p_objid", "reference_code"]].copy()
    df_mrt["ref_num"] = df_mrt["reference_code"].map(ned_ref_map).fillna(-1).astype(int)
    ned_ref_lookup = df_mrt.set_index("p_objid")["ref_num"]
    mask = pubcat["p_objid"].isin(ned_ref_lookup.index)
    pubcat.loc[mask, "z_tot_zsource_flag"] = pubcat.loc[mask, "p_objid"].map(ned_ref_lookup)

    # 8) Final formatting
    pubcat = pubcat[
        [
            "p_objid",
            "p_ra",
            "p_dec",
            "p_petromag_r_0",
            "extended_source_flag",
            "photflag",
            "z_tot_z",
            "z_tot_zerr",
            "z_tot_zsource_flag",
            "member",
        ]
    ].copy()
    pubcat["p_objid"] = pubcat["p_objid"].astype(str)
    pubcat["z_tot_z"] = pubcat["z_tot_z"].astype(float)
    pubcat["z_tot_zerr"] = pubcat["z_tot_zerr"].astype(float)

    # Apply 0.0001 precision to z and e_z.
    # Keep sign for z in output by using fixed-width numeric format later.
    pubcat["z_tot_z"] = pubcat["z_tot_z"].round(4)
    pubcat.loc[pubcat["z_tot_zerr"] == -9, "z_tot_zerr"] = 0.0001
    pubcat["z_tot_zerr"] = pubcat["z_tot_zerr"].round(4)
    small_err_mask = (pubcat["z_tot_zerr"] > 0) & (pubcat["z_tot_zerr"] < 0.0001)
    pubcat.loc[small_err_mask, "z_tot_zerr"] = 0.0001

    pubcat_master = pubcat.reset_index(drop=True).copy()
    pubcat_master["ID"] = pubcat_master.index + 1

    header_txt = """
Title: A redshift survey of the nearby galaxy cluster Abell 2199 : No
upturn of the faint-end slope of galaxy luminosity function

Authors: Park J-I., Song H., Hwang H.S.
Table: Redshifts in the field of A2199 within 35 arcmin from the cluster center
================================================================================
Byte-by-byte Description of file: v57n2p249_Table2.txt
--------------------------------------------------------------------------------
  Bytes  Format Units  Label    Explanations
--------------------------------------------------------------------------------
   1-  4 I4     ---    ID       Object identification
   6- 24 A19    ---    SDSS     SDSS DR17 Object identification
  26- 35 F10.6  deg    RAdeg    Right Ascension in decimal degrees (J2000)
  37- 45 F9.6   deg    DEdeg    Declination in decimal degrees (J2000)
  47- 52 F6.3   mag    rmag     Extinction corrected r-band magnitude
  54- 54 I1     ---    ExtFlag  Extended source flag (1)
  56- 56 I1     ---    PhotFlag Photometric magnitude flag (2)
  58- 64 F7.4   ---    z        Redshift
  66- 71 F6.4   ---    e_z      Uncertainty in z (3)
      73 I1     ---    r_z      Reference for z (4)
      75 I1     ---    Member   Membership flag (5)
--------------------------------------------------------------------------------
Note (1):
   0 = Point source;
   1 = Extended source.
Note (2):
   0 = Petrosian magnitude;
   1 = Fiber magnitude.
Note (3):
   If redshift errors of galaxies from NED are not available or smaller than 0.0001, we set them to 0.0001. Redshifts and uncertainties are reported to 0.0001 precision.
Note (4):
   1 = This study;
   2 = SDSS DR17;
   3 = DESI DR1;
   4 = Albareti et al. (2017) [2016SDSSD.C...0000:];
   5 = Song et al. (2017) [2017ApJ...842...88S];
   6 = Zaritsky et al. (2023) [2023ApJS..267...27Z].
Note (5):
   0 = A2199 non-member;
   1 = A2199 member.
--------------------------------------------------------------------------------
"""

    output_file = "A2199_Machine_Readable_Table2.txt"
    with open(output_file, "w") as f:
        f.write(header_txt)
        for _, row in pubcat_master.iterrows():
            # Fixed-width machine-readable line that matches byte-by-byte description.
            line = (
                f"{int(row['ID']):4d} "
                f"{str(row['p_objid']):<19.19s} "
                f"{row['p_ra']:10.6f} "
                f"{row['p_dec']:9.6f} "
                f"{row['p_petromag_r_0']:6.3f} "
                f"{int(row['extended_source_flag']):1d} "
                f"{int(row['photflag']):1d} "
                f"{row['z_tot_z']:7.4f} "
                f"{row['z_tot_zerr']:6.4f} "
                f"{int(row['z_tot_zsource_flag']):1d} "
                f"{int(row['member']):1d}\n"
            )
            if len(line.rstrip("\n")) != 75:
                raise ValueError(f"Formatted line length is {len(line.rstrip())}, expected 75: {line!r}")
            f.write(line)

    print("Built the NED reference table.")
    print(f"Unique NED reference_code in df_mrt: {df_mrt['reference_code'].dropna().unique()}")
    print(f"Written table to {output_file}")


if __name__ == "__main__":
    main()
