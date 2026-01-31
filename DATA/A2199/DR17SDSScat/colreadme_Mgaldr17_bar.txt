#Bar data from Park & Lee
b_id       STRING: Index of Galaxies in KIAS VAGC
b_ra       FLOAT: Right ascension (J2000)
b_dec      FLOAT: Declination (J2000)
b_z        FLOAT: Redshift
b_rabsmag  FLOAT: Petrosian absolute magnitude at r-band normalized to the z=0.1 epoch. [Note] This is calculated from extinction corrected AB fluxes and the evolution correction of E(z)=1.6(z-0.1) is made (Tegmark et al. 2004)
b_ur       FLOAT: u-r color [Note] We use model magnitudes that are extinction and K-corrected to the z=0.1
b_morph    INTEGER: Galaxy morphology type in KIAS VAGC (1 if Elliptical and lenticular, 2 if Spiral or irregular)
b_cdi      FLOAT: The difference in g-i color of the region with R<0.5Rp form that of the annulus with 0.5Rp<R<Rp, where Rp is the Petrosian radius at i-band. A negative color difference means bluer outside.
b_conx     FLOAT: The inverse concentration index at i-band with seeing correnction, c_{in} = R_{50}/R_{90} where R_{50} and R_{90} are the radii from the center of a galaxy containing 50%, and 90% of the Petrosian flux.
b_abtrue   FLOAT: Seeing corrected isophotal b/a axis ratio at i-band
b_vdisp    FLOAT:  Velocity dispersion. [Note] spectral with median per-pixel S/N >10 and 70 < vdisp < 420 km s^{-1} are recommended to be used
b_vdisperr FLOAT: Error in velocity dispersion
b_snmedian FLOAT: Median per-pixel signal-to-noise
b_bartype  INTEGER: 0 if Early-type galaxies with BARS, 1 if Late-type galaxies with STRONG BARS, 2 if Late-type galaxies with WEAK BARS, 3 if Late-type galaxies with AMBIGUOUS BARS, 9 if Early/Late-type galaxies with NO BARS, -9 NOT CLASSIFIED
