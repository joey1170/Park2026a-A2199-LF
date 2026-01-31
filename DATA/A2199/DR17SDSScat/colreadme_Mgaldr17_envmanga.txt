# Environmental Parameters for MaNGA/SAMI galaxies
# MaNGA data : drpall-v2_4_3.fits from DR16 public data (Same as DR15) => drpall-v3_1_1.fits from DR17 public data (I have changed these data in DR16)
# SAMI data : Public data from https://datacentral.org.au/services/query/#sami.dr2.catalogues.other.DR2Sample, but actually from Haeun Chung (sami_dr2_cat.fits)
# rho20, nsig1nvol & nsig2nvol are defined using the galaxies with 0.01<=z<=0.15 and M_{r,k/E with H0=100km/s}>=-20.598217 (see top right panel in https://astro.kias.re.kr/~hshwang/doc/sample.eps for sample definition)
# dv<=1500 km/s is additionally used for selecting neighbors to calculate nsig1nvol & nsig2nvol
# see https://astro.kias.re.kr/~hshwang/doc/compenv.eps for the comparisons of these parameters
manga_rho20      FLOAT: rho_20/rho_mean that is the background density using the closest 20 galaxies (see eq. 1 of Park & Choi 2009, 691, 1828) 
manga_idsign1vol STRING: SDSS ObjID for the 3rd nearest neighbor
manga_nsign1vol  FLOAT: Sigma_3 (galaxies h^2/Mpc^2) = 3/(!pi*D_p,3^2) where D_p,3 is the projected distance to the 3th-nearest neighbor
manga_idsign2vol STRING: SDSS ObjID for the 5th nearest neighbor
manga_nsign2vol  FLOAT: Sigma_5 (galaxies h^2/Mpc^2) = 5/(!pi*D_p,5^2) where D_p,5 is the projected distance to the 3th-nearest neighbor
manga_distn_id   STRING: SDSS ObjID for the nearest neighbor (Here neighbors should have Mr = Mr,target + 0.5 and have relative velocities less than dv <= 600 km/s for early-type target galaxies and less than dv <= 400 km s−1 for late-type target galaxies)
manga_distn_sec  FLOAT: Distance to the nearest neighbor (in unit of arcsec)
manga_distn_phy  FLOAT: Distance to the nearest neighbor (in unit of Mpc/h)
manga_distn_vir  FLOAT: Distance to the nearest neighbor (in unit of virial radius of the NEIGHBOR)
manga_distn_tvir  FLOAT: Distance to the nearest neighbor (in unit of virial radius of the NEIGHBOR + virial radius of the TARGET)
manga_distn_type INTEGER: Morphological type of the nearest neighbor (1-ETG, 2-LTGs)
manga_disp_neib  FLOAT: Velocity dispersion of neighboring galaxies (HERE neighgbor conditions here: dv<=1500 km/s and R_p<=1 cMpc/h)
