# IFS data
# MaNGA data : v1_2_12 from MaNGA_targets_extNSA_tiled.fit => v1_2_27 from MaNGA_targets_extNSA_tiled.fit (from DR17)
# SAMI data : Public data from https://datacentral.org.au/services/query/#sami.dr2.catalogues.other.DR2Sample, but actually from Haeun Chung (sami_dr2_cat.fits)
s3_nsaid          INTEGER: The unique NSA identifier. This is unique and consistent over all versions of the NSA (http://www.nsatlas.org/)
s3_obsflag        DOUBLE : Set to 1 if the target has already been included on a plate set to be observed at the time the allocation was done, otherwise 0
s3_badphotflag    DOUBLE : Set to 1 if target has been visually inspected to have bad photometry and should not be observed
s3_ranflag        DOUBLE : Set to 1 if target is to be included after random sampling to get correct proportions of each sample, otherwise 0 
s3_samicatid      STRING: The SAMI catalog ID
s3_samiobsflag   INTEGER: Set to 1 if the target was included in the data release, or -9
