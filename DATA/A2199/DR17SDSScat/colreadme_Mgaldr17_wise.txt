wid         STRING : unique WISE source designation.
wcc_flags   STRING : Contamination and confusion flag. Four character string, one character per band [W1/W2/W3/W4], that indicates that the photometry and/or position measurements of a source may be contaminated or biased due to proximity to an image artifact. Detailed information is at http://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec2_2a.html
wext_flg    STRING : Extended source flag (0: point source,>=1: extended source). This is an integer flag, the value of which indicates whether or not the morphology of a source is consistent with the WISE point spread function in any band, or whether the source is associated with or superimposed on a previously known extended object from the 2MASS Extended Source Catalog (XSC). 
xscprox     FLOAT : 2MASS Extended Source Catalog (XSC) proximity. Distance between the WISE source position and the position of a nearby 2MASS XSC source, if the separation is less than 1.1 times the Ks isophotal radius size of the XSC source. This identifies WISE sources that are identically the 2MASS XSC source as well as WISE sources that are fragments of large galaxies. This column is "null" if there is no 2MASS XSC source in proximity to the WISE source.
w1rsemi     FLOAT : Semi-major axis of the elliptical aperture used to measure source in W1 (arcsec). It seems that other WISE bands except for W4 have the same values of rsemi, ba and pa. 
w1ba        FLOAT : Axis ratio (b/a) of the elliptical aperture used to measure source in W1
w1pa        FLOAT : Position angle (degrees E of N) of the elliptical aperture major axis used to measure source in W1 (deg)
w4rsemi     FLOAT : Semi-major axis of the elliptical aperture used to measure source in W4 (arcsec). 
w4ba        FLOAT : Axis ratio (b/a) of the elliptical aperture used to measure source in W4
w4pa        FLOAT : Position angle (degrees E of N) of the elliptical aperture major axis used to measure source in W4 (deg)

wf3p4Jy      FLOAT : WISE 3.4um flux density (Jy) measured with profile-fitting photometry, or the magnitude of the 95% confidence brightness upper limit if the W1 flux measurement has SNR<2. This column is null if the source is nominally detected in W1, but no useful brightness estimate could be made.
wf3p4Jyerr   FLOAT : WISE 3.4um error 
wf3p4snr     FLOAT : WISE 3.4um S/N
w3p4rchi2    FLOAT : Reduced chi^2 of the WISE 3.4um profile-fit photometry measurement. This column is null if the W1 magnitude is a 95% confidence upper limit (i.e. the source is not detected).
w3p4gflux    FLOAT   : WISE 3.4um flux density (Jy) measured in the elliptical aperture described by w1rsemi, w1ba, and w1pa
w3p4gfluxsig FLOAT   : WISE 3.4um flux density error (Jy)
w3p4gflg     INTEGER : WISE 3.4um elliptical aperture measurement quality flag. This flag indicates if one or more image pixels in the measurement aperture for this band is confused with nearby objects, is contaminated by saturated or otherwise unusable pixels, or is an upper limit. The flag values are as described for the "standard" aperture photometry quality flag, w1flg.

wf4p6Jy      FLOAT : WISE 4.6um flux density in unit of Jy
wf4p6Jyerr   FLOAT : WISE 4.6um error 
wf4p6snr     FLOAT : WISE 4.6um S/N
w4p6rchi2    FLOAT : Reduced chi^2 of the WISE 4.6um profile-fit photometry measurement.
w4p6gflux    FLOAT   : WISE 4.6um flux density (Jy) measured in the elliptical aperture
w4p6gfluxsig FLOAT   : WISE 4.6um flux density error (Jy)
w4p6gflg     INTEGER : WISE 4.6um elliptical aperture measurement quality flag.

wf12Jy       FLOAT : WISE 12um flux density in unit of Jy
wf12Jyerr    FLOAT : WISE 12um error 
wf12snr      FLOAT : WISE 12um S/N
w12rchi2     FLOAT : Reduced chi^2 of the WISE 12um profile-fit photometry measurement.
w12gflux     FLOAT   : WISE 12um flux density (Jy) measured in the elliptical aperture
w12gfluxsig  FLOAT   : WISE 12um flux density error (Jy)
w12gflg      INTEGER : WISE 12um elliptical aperture measurement quality flag.

wf22Jy       FLOAT : WISE 22um flux density in unit of Jy
wf22Jyerr    FLOAT : WISE 22um error 
wf22snr      FLOAT : WISE 22um S/N
w22rchi2     FLOAT : Reduced chi^2 of the WISE 22um profile-fit photometry measurement.
w22gflux     FLOAT   : WISE 22um flux density (Jy) measured in the elliptical aperture
w22gfluxsig  FLOAT   : WISE 22um flux density error (Jy)
w22gflg      INTEGER : WISE 22um elliptical aperture measurement quality flag.
