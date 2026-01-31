s3_objid          STRING :     ObjId in SDSS DR16
s3_specobjid      STRING : SpecobjId in SDSS DR16
s3_dr7objid       STRING :     ObjId in SDSS DR7
s3_dr7specobjid   STRING : SpecobjId in SDSS DR7
s3_ra             DOUBLE : Right ascension, J2000, degrees
s3_dec            DOUBLE : Declination, J2000, degrees
s3_run            INT    :   RUN
s3_rerun          INT    : RERUN (there are some galaxies whose photometry was completely adopted from DR7; these galaxies have old rerun values (i.e. s3_rerun ne 301). You just need to use most updated rerun values if you would like to download their images)
s3_dr7run         INT    : RUN for DR7 data
s3_dr7rerun       INT    : RERUN for DR7 data
s3_dr7camcol      INT    : Camcol for DR7 data
s3_dr7field       INT    : Field for DR7 data
s3_obj            INT    : The object id within a field. Usually changes between reruns of the same field
s3_camcol         INT    : Camcol
s3_field          INT    : Field 
s3_ap             FLOAT  : Petrosian mag in r-band - Fiber mag in r-band (for aperture correction of emssion-line flux)
s3_z              DOUBLE : redshift
s3_zErr           DOUBLE : redshift error
s3_specClass      STRING : Spectroscopic class (GALAXY, QSO, STAR, or N (N will be probably galaxies))
s3_subclass       STRING : Spectroscopic subclass
s3_plate          STRING : plate  
s3_mjd            STRING : mjd
s3_fiberID        STRING : fiberID
s3_rmemabs70      FLOAT  : k-corrected, evolution-corrected petrosian absolute magnitude in r-band with H0=70km/s/Mpc
s3_rmemabs        FLOAT  : k-corrected, evolution-corrected petrosian absolute magnitude in r-band with H0=100km/s/Mpc
s3_bmemabs        FLOAT  : k-corrected, evolution-corrected petrosian absolute magnitude in B-band with H0=100km/s/Mpc
s3_urmod          FLOAT  : k-corrected, u-r model color
s3_urmode         FLOAT  : k-corrected, u-r model color error
s3_vdisp_cas      FLOAT  : velocity dispersion in DR9 pipeline
s3_errvdisp_cas   FLOAT  : velocity dispersion error in DR9 pipeline
s3_phtype         INT    : Morphology classification from KIAS-VAGC (DR7) + Galaxy Zoo 1 and 2 (both DR7!) + Hwang's eye (early: 1, late:2, point source (QSO like) : 3, difficult to classify: 8, unclassified: 9)
s3_phtype_source  STRING : Source for Morphology Information (GalaxyZoo1, GalaxyZoo2, KIASvagc, Hwang, N)
s3_sptype         STRING : Spectral types in DR7 MPA-JHU VAGCs (H-Starforming,C-Composite,S-AGN non-Liner,L-Low S/N Liner,U-undefined,N-Not Availble (from phot sample))  (h-Starforming, c-Composite, s-Seyfert; with small alphabet) from the literature 
s3_probpsf        INT    : Probability that the object is a star. Currently 0 if type == 3 (galaxy), 1 if type == 6 (star).
