#Alfalfa survey data
s3_af_id        STRING : Entry number in the AGC ("Arecibo General Catalog"), our internal database
s3_af_ra        FLOAT  : Right ascension (J2000) of the centroid of the ALFALFA HI signal, in degrees 
s3_af_dec       FLOAT  : Declination (J2000) of the centroid of the ALFALFA HI signal, in degrees
s3_af_z21       FLOAT  : Heliocentric redshift of the HI line emission
s3_af_w50       FLOAT  : Width of the HI line measured at 50% of the peak flux, in km/s
s3_af_werr      FLOAT  : Error on w50, in km/s
s3_af_flux      FLOAT  : HI line flux density, in Jy-km/s
s3_af_fluxerr   FLOAT  : Error on flux, in Jy-km/s
s3_af_snratio   FLOAT  : Signal-to-noise ratio of HI signal
s3_af_rms       FLOAT  : RMS noise at 10 km/s, in mJy
s3_af_dist      FLOAT  : Distance in Mpc as assigned 
s3_af_loghimass FLOAT  : Logarithm of the HI mass in solar units
s3_af_detcode   INTEGER: Code for HI line detection status (Code 1 = High signal to noise ratio, extragalactic source; Code 2 = Lower signal to noise ratio HI signal coincident with optical counterpart of unknown redshift; Code 9 = High signal to noise ratio source with no optical counterpart and likely Galactic high velocity cloud)
