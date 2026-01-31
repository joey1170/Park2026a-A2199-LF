import pandas as pd

# 1. Load the master catalog and filter to galaxies within 35 arcmin radius
tempdf = pd.read_csv('./A2199_mastercat_within35arcmin.csv')
tempdf = tempdf[tempdf['p_radgal'] <= 35]  # keep only those within 35 arcmin

# 2. Remove entries with missing redshift (-9) and compute extinction-corrected Petrosian magnitude
tempdf = tempdf[tempdf['z_tot_z'] != -9]
tempdf['p_petromag_r_0'] = tempdf['p_petromag_r'] - tempdf['p_extinction_r']

# 3. Select and order columns for the publication catalog
pubcat = tempdf[['p_objid', 'p_ra', 'p_dec', 'p_petromag_r_0', 
                 'galaxyflag', 'photflag', 'z_tot_z', 'z_tot_zerr', 
                 'z_tot_zsource', 'member']].reset_index(drop=True)

# 4. Load NED reference code mapping table
#    Only need p_objid, ned_name, and reference_code columns
df_ned = pd.read_csv('./NED/A2199_NED_redshift_reference_code.csv')[['p_objid', 'ned_name', 'reference_code']]

# 5. Create mapping from reference code string to source integer value, for output in column 9 of table
ned_ref_map = {
    "2016SDSSD.C...0000:": 4,
    "2017ApJ...842...88S": 5,
    "2009ApJS..180...67R": 6,
    "2004AJ....128.1558S": 7,
    "2023ApJS..268...17K": 8,
    "2023ApJS..267...27Z": 9
}
# Map NED reference codes to their integer flag
df_ned['ref_num'] = df_ned['reference_code'].map(ned_ref_map).fillna(-1).astype(int)

# 6. Map member flag from string to int: 'N'→0, 'Y'→1
pubcat['member'] = pubcat['member'].map({'N': 0, 'Y': 1})

# 7. Map z_tot_zsource string values to integer codes. Default to -9 if unknown.
zsource_map = {'mmt': 1, 'sdss': 2, 'desi': 3}
pubcat['z_tot_zsource_flag'] = pubcat['z_tot_zsource'].str.lower().map(zsource_map).fillna(-9).astype(int)

# 8. For rows with a corresponding p_objid in NED table, use NED reference code as zsource flag
ned_ref_lookup = df_ned.set_index('p_objid')['ref_num']
mask = pubcat['p_objid'].isin(ned_ref_lookup.index)
pubcat.loc[mask, 'z_tot_zsource_flag'] = pubcat.loc[mask, 'p_objid'].map(ned_ref_lookup)

# 9. Rearrange and finalize columns for output. Ensure p_objid is string.
pubcat = pubcat[['p_objid', 'p_ra', 'p_dec', 'p_petromag_r_0', 
                 'galaxyflag', 'photflag', 'z_tot_z', 'z_tot_zerr', 
                 'z_tot_zsource_flag', 'member']]
pubcat['p_objid'] = pubcat['p_objid'].astype(str)

# 10. Set missing z error code (-9) to 0.0001 per publication conventions
pubcat.loc[pubcat['z_tot_zerr'] == -9, 'z_tot_zerr'] = 0.0001

# 11. Prepare master output copy, reset index and assign new sequential ID starting at 1
pubcat_master = pubcat.copy()
pubcat_master = pubcat_master.reset_index(drop=True)
pubcat_master['ID'] = pubcat_master.index + 1  # ID: 1, 2, 3, ...

# 12. Define multi-line header for output file (matches published table notes)
header_txt = """
Title: A redshift survey of the nearby galaxy cluster Abell 2199 : No
upturn of the faint-end slope of galaxy luminosity function

Authors: Park J., Song H., Hwang H.S.
Table: Redshifts in the field of A2199 within 35 arcmins from the cluster center
================================================================================
Byte-by-byte Description of file: v57n2p249_Table1.txt
--------------------------------------------------------------------------------
  Bytes  Format Units  Label    Explanations
--------------------------------------------------------------------------------
   1-  4 I4     ---    ID       Object identification
   6- 24 A19    ---    SDSS     SDSS DR17 Object identification
  26- 35 F10.6  deg    RAdeg    Right Ascension in decimal degrees (J2000)
  37- 45 F9.6   deg    DEdeg    Declination in decimal degrees (J2000)
  47- 52 F6.3   mag    rmag     Extinction corrected r-band Petrosian magnitude
  54- 54 I1     ---    Extended Source Flag     Extended source flag (1)
  54- 54 I1     ---    Photometric Flag     Photomemtric magnidutde flag (2)
  56- 62 F8.6   ---    z        Redshift
  64- 70 F8.6   ---    e_z      Uncertainty in z (3)
  72- 73 I1     ---    r_z      Reference for z (4)
      75 I1     ---    Member   Membership flag (5)
--------------------------------------------------------------------------------
Note (1):
   0 = Point source;
   1 = Extended source.
Note (2):
   0 = Petrosian magnitude;
   1 = Fiber magnitude.
Note (3):
   If redshift errors of galaxies from NED are not available,
   we set them to 0.0001.
Note (4):
   1 = MMT2019 (This study);
   2 = SDSS DR17;
   3 = DESI DR1 [Abdul-Karim et al. (2025)];
   4 = Albareti et al. (2017) [2016SDSSD.C...0000:];
   5 = Song et al. (2017) [2017ApJ...842...88S];
   6 = Richard et al. (2009) [2009ApJS..180...67R];
   7 = Smith et al. (2004) [2004AJ....128.1558S];
   8 = Kim et al. (2023) [2023ApJS..268...17K];
   9 = Zaritsky et al. (2023) [2023ApJS..267...27Z].
Note (5):
   0 = A2199 non-member;
   1 = A2199 member.
--------------------------------------------------------------------------------
"""

# 13. Write output table, with header and columns properly formatted to match publication sample
output_file = "A2199_Machine_Readable_Table2.txt"
with open(output_file, "w") as f:
    f.write(header_txt)
    for _, row in pubcat_master.iterrows():
        # Print each row in formatted fixed-width, match published sample
        f.write(
            f"{int(row['ID']):4d} {row['p_objid']:s} {row['p_ra']:.6f} {row['p_dec']:.6f} "
            f"{row['p_petromag_r_0']:.3f} {int(row['galaxyflag'])} {int(row['photflag'])} "
            f"{row['z_tot_z']:.6f} {row['z_tot_zerr']:.6f} "
            f"{int(row['z_tot_zsource_flag'])} {int(row['member'])}\n"
        )

print(f"Written table to {output_file}")