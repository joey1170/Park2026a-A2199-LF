eadr6                STRING : Name of E+A (DR6) used in Choi et al. 2009, MNRAS, 395, 637
galexid              STRING : Galex ID 
nuv_mag              FLOAT  : Galactic Extinction CORRECTED Galex NUV magnitude (mag_auto) from http://galex.stsci.edu/doc/CASJobsXTutorial.htm (see  http://galex.stsci.edu/GR6/?page=userfaq and http://www.galex.caltech.edu/researcher/faq.html#ANSWER130 for the description of Galex magnitude, also AB mag - https://asd.gsfc.nasa.gov/archive/galex/FAQ/))
nuv_magerr           FLOAT  : Galex NUV magnitude error 
fuv_mag              FLOAT  : Galactic Extinction CORRECTED Galex FUV magnitude (mag_auto) from http://galex.stsci.edu/doc/CASJobsXTutorial.htm (see  http://galex.stsci.edu/GR6/?page=userfaq and http://www.galex.caltech.edu/researcher/faq.html#ANSWER130 for the description of Galex magnitude, also AB mag - https://asd.gsfc.nasa.gov/archive/galex/FAQ/))
fuv_magerr           FLOAT  : Galex FUV magnitude error 
mpstype              STRING : Survey type - AIS, MIS, DIS and so on..
nuv_exptime          FLOAT  : Exposure time for NUV in unit of seconds
fuv_exptime          FLOAT  : Exposure time for FUV in unit of seconds
distance             FLOAT  : angular separation between SDSS and GALEX sources in arc seconds, the radius used for matching is 5"
reverseDistanceRank  INT    : 1 indicates that for a given SDSS object with a GALEX match, that match is the closest, value of 2 indicates the next closest, etc.
nuv_flag             INT    : 1 if NUV data come from the closest match, 2 if it comes from the next closest match
fuv_flag             INT    : 1 if FUV data come from the closest match, 2 if it comes from the next closest match
nuv_galexid          STRING : Galex ID for NUV data. If it is different from GALEXID, then it means that the NUV data come from the next closest
fuv_galexid          STRING : Galex ID for FUV data. If it is different from GALEXID, then it means that the NUV data come from the next closest
e_bv_MW              FLOAT  : Milky Way E(B-V)  
