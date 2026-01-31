# There are several nonHeCS clusters (A383, A611, A1126, A2415, A2457, IIZW108) included in this catalog.
# The MMT redshifts for these clusters ARE included in Mgaldr16_id.sav
#  even though their member galaxies are NOT identified in Mgaldr16_cluster.sav!!!
cl_id  STRING : Cluster ID (This column does not appear in the save file, because the order is the same as Mgaldr16_listcluster.sav)
compcl FLOAT  : Overall Spectroscopic Completeness for a given r-band mag limit (maglcl)
maglcl FLOAT  : r-band mag limit used for calculating the overall Spectroscopic Completeness
Xcl    FLOAT  : Cluster Position in Cartesian Coordinate X (Mpc/h with Om=0.3 and OL=0.7)
Ycl    FLOAT  : Cluster Position in Cartesian Coordinate Y (Mpc/h with Om=0.3 and OL=0.7)
Zcl    FLOAT  : Cluster Position in Cartesian Coordinate Z (Mpc/h with Om=0.3 and OL=0.7)
scale  FLOAT  : arcmin/(Mpc/h) at a cluster redshift
