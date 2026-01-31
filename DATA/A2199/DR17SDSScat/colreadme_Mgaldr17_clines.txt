snflag               INTEGER: 1 - Those with signal-to-noise ratio (S/N) >= 3 in the strong emission-lines Hbeta, [OIII] 5007, Halpha, [NII] 6584, and [SII]6717, 6731; select these galaxies if you want have a sample of galaxies with reliable measurements below; 0 - any galaxies 
hsptype              STRING : Spectral type for DR7 galaxies (H-Starforming,C-Composite,S-Seyfert,L-LINER,A-Amorphous,U-undefined,N-Not Availble(from phot sample)) according to Kewley et al. 2006, MNRAS, 372, 961; (c-Composite, s-Seyfert; with small alphabet) from the literature
ebv_int              FLOAT  : E(b-v) (Not Galactic extinction, But Internal extinction) derived from Balmer decrement (H_alpha/H_beta). This value is determined for only the galaxies with SPTYPE, so you had better use ALL_EBV at Mgaldr7_sup1.sav if you want to have more galaxies (Halpha>0 & Hbeta>0)
cOIII_Hb             FLOAT  : Extinction corrected flux ratio between OIII5007 and Hbeta
cNII_Ha              FLOAT  : Extinction corrected flux ratio between  NII6584 and Halpha
cSII_Ha              FLOAT  : Extinction corrected flux ratio between SII6717+SII6731 and Halpha    
cOI_Ha               FLOAT  : Extinction corrected flux ratio between OI6300 and Halpha
cfha                 FLOAT  : Extinction-corrected H_alpha_flux (1E-17 erg/s/cm^2) -  different from raw data in MPA catalog because of extinction-correction
cfha_err             FLOAT  : Extinction-corrected H_alpha_flux_err
cfhb                 FLOAT  : Extinction-corrected H_beta_flux (1E-17 erg/s/cm^2)
cfhb_err             FLOAT  : Extinction-corrected H_beta_flux_err
coiii_5007_flux      FLOAT  : Extinction-corrected OIII5007_flux (1E-17 erg/s/cm^2)
coiii_5007_flux_err  FLOAT  : Extinction-corrected OIII5007_flux_err
coi_6300_flux        FLOAT  : Extinction-corrected OI6300_flux (1E-17 erg/s/cm^2)
coi_6300_flux_err    FLOAT  : Extinction-corrected OI6300_flux_err
cnii_6584_flux       FLOAT  : Extinction-corrected NII6584_flux (1E-17 erg/s/cm^2)
cnii_6584_flux_err   FLOAT  : Extinction-corrected NII6584_flux_err
csii_6717_flux       FLOAT  : Extinction-corrected SII6717_flux (1E-17 erg/s/cm^2)
csii_6717_flux_err   FLOAT  : Extinction-corrected SII6717_flux_err
csii_6731_flux       FLOAT  : Extinction-corrected SII6731_flux (1E-17 erg/s/cm^2)
csii_6731_flux_err   FLOAT  : Extinction-corrected SII6731_flux_err
coii_3726_flux       FLOAT  : Extinction-corrected OII3726_flux (1E-17 erg/s/cm^2)
coii_3726_flux_err   FLOAT  : Extinction-corrected OII3726_flux_err
coii_3729_flux       FLOAT  : Extinction-corrected OII3729_flux (1E-17 erg/s/cm^2) 
coii_3729_flux_err   FLOAT  : Extinction-corrected OII3729_flux_err
