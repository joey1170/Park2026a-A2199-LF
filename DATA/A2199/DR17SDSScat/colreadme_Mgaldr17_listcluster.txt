# There are several nonHeCS clusters (A383, A611, A1126, A2415, A2457, IIZW108) included in this catalog.
# The MMT redshifts for these clusters ARE included in Mgaldr16_id.sav
#  even though their member galaxies are NOT identified in Mgaldr16_cluster.sav!!!
cl_id      STRING : Cluster ID 
cl_ra      FLOAT  : R.A. of cluster (J2000, deg)
cl_dec     FLOAT  : Decl. of cluster (J2000, deg)
cl_z       FLOAT  : Cluster redshift
cl_sig     FLOAT  : Velocity dispersion of cluster (km/s)
cl_usig    FLOAT  : Upper uncertainty limit in cl_sig
cl_lsig    FLOAT  : Lower uncertainty limit in cl_sig
cl_m200c   FLOAT  : Caustic mass (Msun/h)
cl_em200c  FLOAT  : Uncertainty in M200c
cl_survey  STRING : Source of Survey (CIRS, HeCS, HeCS-SZ, nonHeCS)
cl_r200    FLOAT  : R_200 (Mpc/h)
