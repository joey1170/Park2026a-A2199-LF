ss3_objid          STRING :     ObjId in SDSS DR16
ss3_dr7objid       STRING :     ObjId in SDSS DR7
ss3_specobjid      STRING : SpecobjId in SDSS DR16
ss3_ra             DOUBLE : Right ascension, J2000, degrees
ss3_dec            DOUBLE : Declination, J2000, degrees
ss3_petroMag_r     FLOAT  : r-band Petrosian magnitude (not AB)
ss3_extinction_r   FLOAT  : Galactic extinction in r-band
ss3_z              DOUBLE : redshift
ss3_zErr           DOUBLE : redshift error
ss3_clean          INTEGER: Clean photometry flag (1=clean, 0=unclean)
ss3_survey         STRING : Survey  name (e.g. sdss, boss, segue1, segue2, NN). NN means that redshift information comes from the literature (i.e. NED). 
ss3_programname    STRING : Program name (e.g. boss, lowz_lrg, southern, segpointed, NN)  
ss3_sourceType     STRING : For Legacy, SEGUE-2 and BOSS science targets, type of object targeted as (e.g. NONLEGACY, LRG, QSO, STAR, GALAXY, NN)
ss3_zWarning       INTEGER: Bitmask of warning values; 0 means all is well
ss3_instrument     STRING : Instrument that this spectrum was observed with (SDSS or BOSS)
