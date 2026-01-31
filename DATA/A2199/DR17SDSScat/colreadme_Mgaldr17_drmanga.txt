# IFS data
# MaNGA data : drpall-v2_4_3.fits from DR16 public data (Same as DR15) => drpall-v3_1_1.fits from DR17 public data (I have changed these data in DR16)
# SAMI data : Public data from https://datacentral.org.au/services/query/#sami.dr2.catalogues.other.DR2Sample, but actually from Haeun Chung (sami_dr2_cat.fits)
s3_drnsaid     INTEGER: The unique NSA identifier. This is unique and consistent over all versions of the NSA (http://www.nsatlas.org/)
s3_drobsflag   INTEGER: Set to 1 if the target was included in the data release, or -9
s3_plateifu     STRING: Composed of the plate ID (PLATE) and the IFU design ID (IFUDSGN) in the format of "PLATE-IFUDSGN". It uniquely identifies an observation of a target. 
s3_samicatid    STRING: The SAMI catalog ID
s3_samiobsflag INTEGER: Set to 1 if the target was included in the data release, or -9
