# See http://skyserver.sdss.org/dr16/en/help/docs/tabledesc.aspx for the details of different models and the name of TABLES
# It seems that s3_stellarMassPCAWiscBC03_mstellar_median is the best to use; see http://arxiv.org/abs/1607.04678
s3_stellarMassFSPSGranEarlyDust_logMass_median    FLOAT : Median stellar mass of galaxy. It corresponds to the value of PDF at which 50% of the stellar mass probability is accumulated (log base 10 in solar masses). (changed from Kroupa IMF to Salpeter IMF with mstar / 0.7; Granada group originally provides the mass with Kroupa/Salpeter IMFs (see http://www.sdss.org/dr16/spectro/galaxy_granada/), but the Kroupa one is included in the SDSS database for CasJobs. Therefore, I downloaded the Kroupa one from the Casjobs, and convert it to Salpeter one by dividing with 0.7 to be consistent with other estimate. Note that the comparion between Kroupa and Salpeter ones for this version suggests that the factor to divide is 0.614724 rather 0.7, but I decided to use 0.7 for consistency.) (Granada group provides Mstar for both MGS and BOSS galaxies!)
s3_stellarMassFSPSGranEarlyDust_logMass_err       FLOAT : 1-sigma error associated with LogMass_Median
s3_stellarMassFSPSGranEarlyNoDust_logMass_median  FLOAT : Median stellar mass of galaxy. It corresponds to the value of PDF at which 50% of the stellar mass probability is accumulated (log base 10 in solar masses). (changed from Kroupa IMF to Salpeter IMF with mstar / 0.7)
s3_stellarMassFSPSGranEarlyNoDust_logMass_err     FLOAT : 1-sigma error associated with LogMass_Median 
s3_stellarMassFSPSGranWideDust_logMass_median     FLOAT : Median stellar mass of galaxy. It corresponds to the value of PDF at which 50% of the stellar mass probability is accumulated (log base 10 in solar masses). (changed from Kroupa IMF to Salpeter IMF with mstar / 0.7)
s3_stellarMassFSPSGranWideDust_logMass_err        FLOAT : 1-sigma error associated with LogMass_Median 
s3_stellarMassFSPSGranWideNoDust_logMass_median   FLOAT : Median stellar mass of galaxy. It corresponds to the value of PDF at which 50% of the stellar mass probability is accumulated (log base 10 in solar masses). (changed from Kroupa IMF to Salpeter IMF with mstar / 0.7)
s3_stellarMassFSPSGranWideNoDust_logMass_err      FLOAT : 1-sigma error associated with LogMass_Median 
s3_stellarMassPassivePort_logMass                 FLOAT : Best-fit stellar mass of galaxy (changed from Kroupa IMF to Salpeter IMF with mstar / 0.7)
s3_stellarMassPassivePort_minlogMass              FLOAT : 1-sigma minimum stellar mass (where chi-squared is within minimum + 1)
s3_stellarMassPassivePort_maxlogMass              FLOAT : 1-sigma maximum stellar mass (where chi-squared is within minimum + 1)
s3_stellarMassPCAWiscBC03_mstellar_median         FLOAT : median (50th percentile of PDF) of log stellar mass (best estimator) (changed from Kroupa IMF to Salpeter IMF with mstar / 0.7)
s3_stellarMassPCAWiscBC03_mstellar_err            FLOAT : 1-sigma error in log stellar mass (84th minus 16th percential)
s3_stellarMassPCAWiscM11_mstellar_median          FLOAT : median (50th percentile of PDF) of log stellar mass (best estimator) (changed from Kroupa IMF to Salpeter IMF with mstar / 0.7)
s3_stellarMassPCAWiscM11_mstellar_err             FLOAT : 1-sigma error in log stellar mass (84th minus 16th percential)
s3_stellarMassStarformingPort_logMass             FLOAT : Best-fit stellar mass of galaxy (changed from Kroupa IMF to Salpeter IMF with mstar / 0.7)
s3_stellarMassStarformingPort_minlogMass          FLOAT : 1-sigma minimum stellar mass (where chi-squared is within minimum + 1)
s3_stellarMassStarformingPort_maxlogMass          FLOAT : 1-sigma maximum stellar mass (where chi-squared is within minimum + 1)
s3_stellarMassPassivePort_age                     FLOAT : Age of best fit based on Portsmouth method, passive model and Kroupa IMF
s3_stellarMassPassivePort_minage                  FLOAT : 1-sigma minimum age (where chi-squared is within minimum + 1)
s3_stellarMassPassivePort_maxage                  FLOAT : 1-sigma maximum age (where chi-squared is within minimum + 1)
s3_stellarMassStarformingPort_age                 FLOAT : Age of best fit based on Portsmouth method, star-forming model and Kroupa IMF
s3_stellarMassStarformingPort_minage              FLOAT : 1-sigma minimum age (where chi-squared is within minimum + 1)
s3_stellarMassStarformingPort_maxage              FLOAT : 1-sigma maximum age (where chi-squared is within minimum + 1)
s3_stellarMassFSPSGranEarlyDust_metallicity       FLOAT : Best-fit metallicity, where Z_sun=0.019
s3_stellarMassFSPSGranEarlyDust_metallicity_err   FLOAT : 1-sigma error for metallicity
s3_stellarMassFSPSGranEarlyNoDust_metallicity     FLOAT : Best-fit metallicity, where Z_sun=0.019
s3_stellarMassFSPSGranEarlyNoDust_metallicity_err FLOAT : 1-sigma error for metallicity
s3_stellarMassFSPSGranWideDust_metallicity        FLOAT : Best-fit metallicity, where Z_sun=0.019
s3_stellarMassFSPSGranWideDust_metallicity_err    FLOAT : 1-sigma error for metallicity
s3_stellarMassFSPSGranWideNoDust_metallicity      FLOAT : Best-fit metallicity, where Z_sun=0.019
s3_stellarMassFSPSGranWideNoDust_metallicity_err  FLOAT : 1-sigma error for metallicity
s3_stellarMassStarformingPort_metallicity         FLOAT : Metallicity of best fit template (0.004, 0.01, 0.02, 0.04, or "composite")
lmass                                             FLOAT : stellar mass (Salpeter IMF) derived using Le Phare code with SDSS 5-band photometry
lmasserr                                          FLOAT : Le Phare stellar mass error
logmass_rabs                                      FLOAT : log(stellar mass) (Salpeter IMF) converted from s3_rmemabs 
FSPSGranEarlyDust_cModelAbsMag_u                  FLOAT : u-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranEarlyDust_cModelAbsMag_g                  FLOAT : g-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranEarlyDust_cModelAbsMag_r                  FLOAT : r-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranEarlyDust_cModelAbsMag_i                  FLOAT : i-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranEarlyDust_cModelAbsMag_z                  FLOAT : z-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranEarlyNoDust_cModelAbsMag_u                FLOAT : u-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranEarlyNoDust_cModelAbsMag_g                FLOAT : g-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranEarlyNoDust_cModelAbsMag_r                FLOAT : r-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranEarlyNoDust_cModelAbsMag_i                FLOAT : i-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranEarlyNoDust_cModelAbsMag_z                FLOAT : z-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranWideDust_cModelAbsMag_u                   FLOAT : u-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranWideDust_cModelAbsMag_g                   FLOAT : g-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranWideDust_cModelAbsMag_r                   FLOAT : r-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranWideDust_cModelAbsMag_i                   FLOAT : i-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranWideDust_cModelAbsMag_z                   FLOAT : z-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranWideNoDust_cModelAbsMag_u                 FLOAT : u-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranWideNoDust_cModelAbsMag_g                 FLOAT : g-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranWideNoDust_cModelAbsMag_r                 FLOAT : r-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranWideNoDust_cModelAbsMag_i                 FLOAT : i-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
FSPSGranWideNoDust_cModelAbsMag_z                 FLOAT : z-band Cmodel absolute magnitudes, K+E corrected at z_0=0.55
