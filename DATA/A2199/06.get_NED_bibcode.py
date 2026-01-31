import pandas as pd
from astroquery.ned import Ned
from astropy.coordinates import SkyCoord
import astropy.units as u
import time

def get_ned_info(ra, dec):
    """
    Query NED for object at given RA, Dec. Returns (ned_name, redshift, redshift_error, reference_code).
    """
    try:
        coord = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, frame='icrs')
        results = Ned.query_region(coord, radius=1.5 * u.arcsec)
        if len(results) == 0:
            return None, None, None, None

        ned_name = results['Object Name'][0]
        ztab = Ned.get_table(ned_name, table='redshifts')
        if len(ztab) == 0:
            return ned_name, None, None, None

        redshift = ztab['Redshift'][0] if 'Redshift' in ztab.colnames else None

        if 'Error' in ztab.colnames:
            redshift_err = ztab['Error'][0]
        elif 'Uncertainty' in ztab.colnames:
            redshift_err = ztab['Uncertainty'][0]
        else:
            redshift_err = None

        refcode = ztab['Refcode'][0] if 'Refcode' in ztab.colnames else None

        try:
            redshift = float(redshift) if redshift is not None else None
        except Exception:
            redshift = None

        try:
            redshift_err = float(redshift_err) if redshift_err is not None else None
        except Exception:
            redshift_err = None

        return ned_name, redshift, redshift_err, refcode

    except Exception:
        return None, None, None, None

tempdf = pd.read_csv('./A2199_mastercat_within35arcmin.csv')
tempdf = tempdf[tempdf['p_radgal']<=35]
# Assume tempdf is defined elsewhere
df_ned = tempdf[tempdf['z_tot_zsource'] == 'ned'].copy()

ned_names, redshifts, redshift_errs, refcodes = [], [], [], []

from tqdm import tqdm
for _, row in tqdm(df_ned.iterrows(), total=df_ned.shape[0]):
    ra, dec = row['p_ra'], row['p_dec']
    ned_name, z, zerr, ref = get_ned_info(ra, dec)
    ned_names.append(ned_name)
    redshifts.append(z)
    redshift_errs.append(zerr)
    refcodes.append(ref)
    time.sleep(1)

df_ned['ned_name'] = ned_names
df_ned['redshift'] = redshifts
df_ned['redshift_error'] = redshift_errs
df_ned['reference_code'] = refcodes

# Assign specific reference codes for certain objects by ned_name
df_ned.loc[df_ned['ned_name'] == 'WHL J162620.3+392343', 'reference_code'] = "2016SDSSD.C...0000:"
df_ned.loc[df_ned['ned_name'] == 'NFP J162735.4+391458', 'reference_code'] = "2004AJ....128.1558S"

df_ned.to_csv('./NED/A2199_NED_redshift_reference_code.csv', index=False)
