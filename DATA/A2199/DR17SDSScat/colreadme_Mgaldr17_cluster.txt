cirsflag     INT    : Flag for CIRS (1 - member galaxy in CIRS clusters (see http://adsabs.harvard.edu/abs/2006AJ....132.1275R ; data are not public, so do not use yet, 0 - not in CIRS clusters))
cirsname     STRING : Name of CIRS cluster
cirsdist     FLOAT  : Projected clustercentric distance to nearby CIRS cluster (degree) 
hecsflag     INT    : Flag for HeCS (>=1 - member galaxy in HeCS clusters (see http://adsabs.harvard.edu/abs/2013ApJ...767...15R, 0 - not in HeCS clusters)). Strictly, it indicates the number of clusters for which this galaxy is classified as a member.
hecsname     STRING : Name of HeCS cluster
hecsdist     FLOAT  : Projected clustercentric distance to nearby HeCS cluster (degree)
hecsszflag   INT    : Flag for HeCS-SZ (>=1 - member galaxy in HeCS-SZ clusters (see http://adsabs.harvard.edu/abs/2016ApJ...819...63R, 0 - not in HeCS-SZ clusters)). Strictly, it indicates the number of clusters for which this galaxy is classified as a member.
hecsszname   STRING : Name of HeCS-SZ cluster
hecsszdist   FLOAT  : Projected clustercentric distance to nearby HeCS-SZ cluster (degree)
nonhecsflag  INT    : Flag for nonHeCS (>=1 - member galaxy in nonHeCS clusters (A383 - http://adsabs.harvard.edu/abs/2014ApJ...783...52G, A611 - http://adsabs.harvard.edu/abs/2014ApJ...783...52G) 
nonhecsname  STRING : Name of nonHeCS cluster
nonhecsdist  FLOAT  : Projected clustercentric distance to nearby nonHeCS cluster (degree)
cl_zsource   STRING : redshift source (MMT, SDSS, NED, FLWO, B04(Boschin+04))
