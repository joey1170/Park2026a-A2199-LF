Galaxy catalogs in SDSS DR17 by Ho Seong Hwang
Last  updated: 09/Jul/2023
First updated: 08/Jul/2022

1. The spectroscopic sample of galaxies and QSOs - IDL save files only!

 * Column description for each save file is at colreadme_Mgaldr17_***.txt

 Mgaldr17_id.sav      : Identifications
sMgaldr17_id.sav      : Light version of Mgaldr17_id.sav (only contains very important columns!)
 Mgaldr17_flags.sav   : Several Flags including source of redshifts
 Mgaldr17_stars.sav   : Spectroscopically confirmed STARs in SDSS (not included in the galaxy catalog)
 Mgaldr17_starwise.sav : WISE data for Mgaldr17_stars.sav from http://wise2.ipac.caltech.edu/docs/release/allwise/
 Mgaldr17_garbage.sav : Problematic sources with spectra in SDSS (not included in the galaxy catalog)
 Mgaldr17_sdss.sav    : Photometric data
 Mgaldr17_spec.sav    : Spectroscopic data
 Mgaldr17_spcomp.sav  : Spectroscopic Completeness (meaningful only for the main galaxy sample)
 Mgaldr17_mpa.sav     : Spectroscopic data in the MPA-JHU VAGC (IN FACT, the actual data are only for galaxies in DR7) 
 Mgaldr17_galex.sav   : GALEX data
 Mgaldr17_2mass.sav   : 2MASS data    
 Mgaldr17_wise.sav    : WISE data for Mgaldr17_id.sav from http://wise2.ipac.caltech.edu/docs/release/allwise/
 Mgaldr17_wisecol.sav : AGN class using WISE data
 Mgaldr17_pscakari.sav : AKARI Point Source Catalog
 Mgaldr17_akari.sav    : AKARI Bright Source Catalog V2 from http://www.ir.isas.jaxa.jp/AKARI/Archive/Catalogues/FISBSCv2/  
 Mgaldr17_iras.sav     : IRAS data   
 Mgaldr17_herschel.sav : Herschel data   
 Mgaldr17_submm.sav    : Some ground-based Submillimeter data   
 Mgaldr17_tdust.sav    : Dust temperature/mass from 2-component MBB fit (NUMBER of galaxies is NOT the same as the one in Mgaldr17_id.sav!!!!)
 Mgaldr17_first.sav    : FIRST data   
 Mgaldr17_alfalfa.sav  : ALFALFA survey data (a.70 from http://egg.astro.cornell.edu/alfalfa/data/index.php)   
 Mgaldr17_clines.sav   : Extinction correction emission line data from the MPA-JHU VAGC 
 Mgaldr17_lir.sav      : Data form the SED fit with Chary & Elbaz (01)   
 Mgaldr17_jrm.sav      : Data from the SED fit with DECOMPIR (Number of galaxies in this file is different from those in  other files. You need to find the matches with IDs)
 Mgaldr17_s870.sav     : Predicted submillemter data from the SED fit
 Mgaldr17_cluster.sav  : CIRS, HeCS & HeCS-SZ cluster data
 Mgaldr17_memcluster.sav  : Some additional information on Cluster galaxies (including revised membership flag)
 Mgaldr17_listcluster.sav : Cluster list used for Mgaldr17_cluster.sav (number of entry is not the same as the number of galaxies in other save files!) 
 Mgaldr17_listcluster.txt : Same as Mgaldr17_listcluster.sav, but in txt format
 Mgaldr17_listclusterR.sav: Some additional information on Clusters (number of entry is not the same as the number of galaxies in other save files!) 
 Mgaldr17_listclusterR.txt : Same as Mgaldr17_listclusterR.sav, but in txt format
 Mgaldr17_mstarage.sav : Various Stellar Mass Estimates, Age & Metallicity
 Mgaldr17_drmanga.sav  : Flags for the MaNGA/SAMI galaxies included in DR16
 Mgaldr17_envmanga.sav : Environmental Parameters for the MaNGA/SAMI galaxies included in DR16
 Mgaldr17_envcoldgal.sav : Environmental Parameters for Very Cold Galaxies
 Mgaldr17_swift.sav    : Swift data from http://swift.gsfc.nasa.gov/results/bs70mon/
 Mgaldr17_gas.sav      : H2 gas data from the literature
 Mgaldr17_size.sav     : Some size information from SDSS
 Mgaldr17_morfit.sav   : Galaxy Serfit Fit information from SDSS
 Mgaldr17_spin.sav     : Galaxy Spin information from SDSS,SAMI,CALIFA & Literature
 Mgaldr17_ksg.sav      : KIAS Value-added Catalog data
 sdss_morph.txt        : Compilation of Visual Inspection from other surveys

rm -rf *sav
rm -rf col*txt
rm -rf *sdss_morph*txt
rm -rf *listclus*txt
cp -prf /Users/hhwang/Research/Work/LIRGs/galcat/*_Mgaldr17*txt .
cp -prf /Users/hhwang/Research/Work/LIRGs/galcat/Mgaldr17*sav .
cp -prf /Users/hhwang/Research/Work/LIRGs/galcat/sMgaldr17_id.sav .
cp -prf /Users/hhwang/Research/Work/LIRGs/galcat/sdss_morph.txt .
cp -prf /Users/hhwang/Research/Work/LIRGs/galcat/colreadme_sdss_morph.txt .
cp -prf /Users/hhwang/Research/Work/LIRGs/galcat/Mgaldr17_listcluster.txt .
cp -prf /Users/hhwang/Research/Work/LIRGs/galcat/Mgaldr17_listclusterR.txt .
rm -rf *envmanga_*
rm -rf *_manga*
rm -rf *_bar*
rm -rf *_magphys*
rm -rf *_sfh*
cd ..
tar czvf DR17sdsscat20230709.tar.gz DR17SDSScat
