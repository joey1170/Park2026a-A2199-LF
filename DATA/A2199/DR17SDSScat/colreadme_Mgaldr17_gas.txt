# Master CO/H2 data
s3_tot_cosource    STRING: CO data reference (GaoSolomon04, Kenney89, Chung09, Mok16, French15, HRS, ALLSMOG, ATLAS3D, xCOLDGASS, VALES, Oteo17, Koyama17, N - no data)
s3_tot_coflag      STRING: 'Y' if CO detected, 'N' for no detection
s3_tot_logmh2       FLOAT: log(H2 mass/Msun)
s3_tot_logmh2err    FLOAT: error of log(H2 mass/Msun)
# Data from VALES (https://ui.adsabs.harvard.edu/abs/2017MNRAS.470.3775V/abstract)
s3_v17_id           STRING: VALES ID
s3_v17_logmh2       FLOAT: log(H2 mass/Msun)
s3_v17_logmh2_err   FLOAT: error of log(H2 mass/Msun)
# Data from Oteo17 (https://arxiv.org/pdf/1707.05329.pdf)
s3_o17_id           STRING: Source ID
s3_o17_logmh2       FLOAT: log(H2 mass/Msun)
# Data from Koyama17 (https://ui.adsabs.harvard.edu/abs/2017ApJ...847..137K/abstract)
s3_k17_id           STRING: Source ID
s3_k17_logmh2       FLOAT: log(H2 mass/Msun)
s3_k17_logmh2_err   FLOAT: error of log(H2 mass/Msun)
# Data from xCOLDGASS (https://ui.adsabs.harvard.edu/abs/2017ApJS..233...22S/abstract)
s3_cg_id            STRING: GASS ID
s3_cg_logmstar       FLOAT: Stellar mass [log Msun]
s3_cg_sn             FLOAT: S/N of the CO(1-0) line
s3_cg_logmh2         FLOAT: Total molecular gas mass [log Msun]
s3_cg_logmh2_err     FLOAT: Error on LOGMH2
s3_cg_coflag       INTEGER: flagCO [1: detection, 2: non-detection] 
# Data from ALTAS3D (https://ui.adsabs.harvard.edu/abs/2011MNRAS.414..940Y/abstract)
s3_at_id           STRING: ATLAS3D ID
s3_at_i10           FLOAT: Intregrated intensity at CO(1-0), quoted as main beam brightness temperature Tmb 
s3_at_i10err        FLOAT: rms uncertainty on I(1-0) 
s3_at_logmh2flag   STRING: H2 mass flag (=: detection, <:upper limit)
s3_at_logmh2        FLOAT: log H2 mass (Msun)
s3_at_logmh2err     FLOAT: rms uncertainty on logMH2 
# Data from ALLSMOG (https://ui.adsabs.harvard.edu/abs/2017A%26A...604A..53C/abstract)
s3_as_id           STRING: Source name from NED.   
s3_as_lco21         FLOAT: Luminosity of the CO(2-1) emission line, in units of 10^8 K km/s pc^2
s3_as_lco21err      FLOAT: Error in s3_as_lco21
s3_as_logmh2_flag  STRING: H2 mass flag (=: detection, <:upper limit) 
s3_as_logmh2_cxo    FLOAT: Log molecular hydrogen mass, calculated assuming a constant X_co appropriate for the Milky-Way.  
s3_as_logmh2_cxoerr FLOAT: Error in s3_as_logmh2_cxo
s3_as_logmh2_mxo    FLOAT: Log molecular hydrogen mass, calculated assuming a metallicity-dependent X_co, as described in the text. 
s3_as_logmh2_mxoerr FLOAT: Error in s3_as_logmh2_mxo 
s3_as_logmh1        FLOAT: Log atomic hydrogen mass. 
s3_as_logmstar      FLOAT: Log stellar mass, calculated from SDSS. 
# Data from HRS (https://ui.adsabs.harvard.edu/abs/2014A%26A...564A..65B/abstract): Herschel Reference Survey
s3_hrs_id          STRING: Source ID
s3_hrs_sco          FLOAT: Total CO flux (Jy.km/s)
s3_hrs_scoerr       FLOAT: Error on the total CO flux
s3_hrs_logmh2_cxo   FLOAT: Logarithm of the molecular gas mass (assuming the standard galactic X_CO_) in unit of Msun
s3_hrs_logmh2_lxo   FLOAT: Logarithm of the molecular gas mass (assuming a luminosity dependent X_CO_) in unit of Msun
# Data from French15 (https://ui.adsabs.harvard.edu/abs/2015ApJ...801....1F/abstract); E+A survey
s3_ea_id           STRING: Galaxy ID
s3_ea_ico           FLOAT: I_CO (K km/s)
s3_ea_icoerr        FLOAT: Error in I_CO
s3_ea_lco           FLOAT: L_CO (10^7 K km/s pc^2)
s3_ea_lcoerr        FLOAT: Error in L_CO
s3_ea_mh2_flag     STRING: H2 mass flag (' ':detection, '<':upper limit)   
s3_ea_mh2           FLOAT: H2 mass in unit of Msun (not LOG!)
s3_ea_mh2err        FLOAT: Error in H2 mass
# Data from GaoSolomon04 (https://ui.adsabs.harvard.edu/abs/2004ApJS..152...63G/abstract)
s3_gao_id          STRING: Galaxy ID
s3_gao_logmh2       FLOAT: log (H2 mass/Msun)
# Data from Kenney89 (https://ui.adsabs.harvard.edu/#abs/1989ApJ...344..171K/abstract)
s3_kenney_id         STRING: Galaxy ID
s3_kenney_scojykms    FLOAT: Total CO flux (Jy km/s)
s3_kenney_scojykmserr FLOAT: Error on the total CO flux
s3_kenney_logmh2      FLOAT: log (H2 mass/Msun)
s3_kenney_logmh2err   FLOAT: error in log (H2 mass/Msun)
# Data from Chung09 (https://ui.adsabs.harvard.edu/abs/2009ApJS..184..199C/abstract)
s3_chung_id         STRING: Galaxy ID
s3_chung_scojykms    FLOAT: Total CO flux (Jy km/s)
s3_chung_scojykmserr FLOAT: Error on the total CO flux
s3_chung_logmh2      FLOAT: log (H2 mass/Msun)
s3_chung_logmh2err   FLOAT: error in log (H2 mass/Msun)
# Data from Mok16 JCMT NGLS (https://ui.adsabs.harvard.edu/abs/2016MNRAS.456.4384M/abstract)
s3_ngls_id          STRING: Galaxy ID
s3_ngls_logmh2      FLOAT: log (H2 mass/Msun)
s3_ngls_logmh2err   FLOAT: error in log (H2 mass/Msun)
