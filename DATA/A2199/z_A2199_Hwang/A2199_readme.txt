# data for A2199  at CfA 2012/Sep/17
1. DATA
1) Photometric sample of galaxies
; DR7
SELECT p.objid,p.ra,p.dec,p.petroMag_u,p.petroMagerr_u,p.petroMag_g,p.petroMagerr_g,p.petroMag_r,p.petroMagerr_r,p.petroMag_i,p.petroMagerr_i,p.petroMag_z,p.petroMagerr_z,p.modelMag_u,p.modelMagerr_u,p.modelMag_g,p.modelMagerr_g,p.modelMag_r,p.modelMagerr_r,p.modelMag_i,p.modelMagerr_i,p.modelMag_z,p.modelMagerr_z,p.extinction_u,p.extinction_g,p.extinction_r,p.extinction_i,p.extinction_z,p.petroRad_r,p.petroRadErr_r,p.run,p.rerun,p.camCol,p.field,p.petroMag_r-p.fiberMag_r,p.probPSF,p.fiberMag_u,p.fiberMagerr_u,p.fiberMag_g,p.fiberMagerr_g,p.fiberMag_r,p.fiberMagerr_r,p.fiberMag_i,p.fiberMagerr_i,p.fiberMag_z,p.fiberMagerr_z into mydb.TAGMLNa2199phot
FROM dbo.fGetNearbyObjEq(247.15933, 39.55127, 400) as b, PhotoObj as p
WHERE b.objID = p.objID and p.petroMag_r-p.extinction_r <= 20.11
; => TAGMLNa2199phot_hshwang.csv

; DR9 # Because there are some galaxies with spec z in DR9
SELECT p.objid,p.ra,p.dec,p.petroMag_u,p.petroMagerr_u,p.petroMag_g,p.petroMagerr_g,p.petroMag_r,p.petroMagerr_r,p.petroMag_i,p.petroMagerr_i,p.petroMag_z,p.petroMagerr_z,p.modelMag_u,p.modelMagerr_u,p.modelMag_g,p.modelMagerr_g,p.modelMag_r,p.modelMagerr_r,p.modelMag_i,p.modelMagerr_i,p.modelMag_z,p.modelMagerr_z,p.extinction_u,p.extinction_g,p.extinction_r,p.extinction_i,p.extinction_z,p.petroRad_r,p.petroRadErr_r,p.run,p.rerun,p.camCol,p.field,p.petroMag_r-p.fiberMag_r,p.probPSF,p.fiberMag_u,p.fiberMagerr_u,p.fiberMag_g,p.fiberMagerr_g,p.fiberMag_r,p.fiberMagerr_r,p.fiberMag_i,p.fiberMagerr_i,p.fiberMag_z,p.fiberMagerr_z,p.fracDeV_r,p.deVRad_i,p.deVAB_i into mydb.a2199phot21_5DR9_hshwang
FROM dbo.fGetNearbyObjEq(247.15933, 39.55127, 400) as b, PhotoObj as p
WHERE b.objID = p.objID and (p.petroMag_r-p.extinction_r <= 21.5 or p.fiberMag_r<20.975)
; => a2199phot21_5DR9_hshwang.csv

; MMT z data From Rines & Geller 08
A) Catalog : aj262373_mrt1.txt
; cp aj262373_mrt1.txt aj262373_mrt1ed.txt
; vi aj262373_mrt1ed.txt ; Comment two overlapped galaxies
B) Spectra from Susan (email at Nov. 17 2011) 
  /Users/hhwang/Research/Work/WISEcfa/IndivCluster/A2199/z_SPECTRA/2007.0716 
  /Users/hhwang/Research/Work/WISEcfa/IndivCluster/A2199/z_SPECTRA/2007.0717 
.comp zoutmake
zoutmake
; => zout_* at each directory


;2) New MMT z data and Match the photometric sample of galaxies with Spectroscopic data 
.comp photmat.pro   ; (badphot.txt)
photmat

; Numbers for Rines & Geller 08
; In the catalog, there are 479 redshifts 
; 2 appear twice (also 2 close to bright stars, but decide to add) 
; Initially, there are 7 objects not matched with DR12 phot
104.a2199new_1_9.ms.fits 247.222452  39.561722   8820.0  1 - PofG
236.a2199new_1_7.ms.fits 247.106810  39.567444  10451.0  2 - no phot ; 587733604804395254
038.a2199b_1_219.ms.fits 246.681604  39.418251   8917.0  3 - 23.26286, 20.77138
042.a2199b_1_22.ms.fits 246.884336  39.506527  80497.0  4 - 24.81801, 19.01572
167.a2199b_1_329.ms.fits 247.194414  39.568943  80173.0  5 - no phot ; 587733604804461124
202.a2199b_1_327.ms.fits 247.157965  39.532501 153099.0  6 - no phot ; 587733604804460611
242.a2199b_1_86.ms.fits 247.127037  39.471222   9161.0  7 - 23.09724, 20.97412
; => After revision, there are 477 redshifts in my save files!!!

; Numbers for our MMT
We observed 1025 targets, and obtained 776 reliable redshifts.
However, one galaxy turns out to be part of galaxy 1237659326029431079 at 247.294111773, 39.348420700
; => We therefore report as we observed 1024 targets, and obtained 775 redshifts!

;3) Match with NED spec and SDSS data
.comp nedmatch.pro 
nedmatch
; => nz_a2199phot21_5DR9_hshwang.sav
;DR12
INDMMT          LONG      = Array[1555]
INDMMTRG        LONG      = Array[477]
INDMMTR13       LONG      = Array[502]
INDR02          LONG      = Array[17]
INDSDSS         LONG      = Array[43521]
INDNED          LONG      = Array[320]
INDSDSSNED      LONG      = Array[718]
INDN            LONG      =           -1
INDU            LONG      =           -1
2MRS B02 C90 HO98 MMT MMT_R13 MMT_RG08 NED NFPS P99 R02 SDSS SDSS_NED U W05 Z90
INDMMTKIAS14    LONG      = Array[324]
INDMMTKIAS15    LONG      = Array[450]
INDMMTKIAS19    LONG      = Array[781]


;DR12 with old NED
INDMMT          LONG      = Array[775]
INDMMTRG        LONG      = Array[477]
INDMMTR13       LONG      = Array[502]
INDR02          LONG      = Array[42]
INDSDSS         LONG      = Array[43637]
INDNED          LONG      = Array[465]

;DR10 with zWarning cut
;IND             LONG      = Array[45416]
INDMMT          LONG      = Array[1295]
INDMMTKIAS      LONG      = Array[325]
INDSDSS         LONG      = Array[43514]
INDD11          LONG      = Array[120]
INDNED          LONG      = Array[487]

; R02
158 243.256674  39.236973  0.032  1 ; hard to identify, but sdss covered
269 244.575949  41.578804  0.060  2 ; hard to identify, but sdss covered
608 246.918354  40.921612  0.032  3 ; hard to identify, but sdss covered
845 248.589020  43.378887  0.071  4 ; appear twice
914 249.422665  42.527390  0.078  5 ; appear twice


; WISE data
.comp pmatchwise.pro
pmatchwise
; => W_a2199phot21_5DR9_hshwang.sav

; AGN class
.comp agnclass
agnclass
; => AGN_a2199phot21_5DR9_hshwang.sav


;7) Color - magntidue Diagram
.comp cmr
cmr, /col
; => Ccmr_a2199.eps
; => cmr_a2199phot21_5DR9_hshwang.sav
aa =       1.2520572
bb =    -0.030092999
rms =     0.079206757
; two members with very red colors are checked, and good to go
;    1237659330852159915 247.252412  39.613588 3  18.75   1.00  0.038 MMT_RG0   2
;     1237659326029366034 247.056882  39.495417 3  19.60   0.99  0.031    MMT   3
; => redshifts with g-r<-0.2 are checked: most of them are stars! 


.comp kcorrgal
kcorrgal
; => kcorr_a2199phot21_5DR9_hshwang.sav


; ; data for R<33arcmin
.comp savcat
savcat
; => zr33_a2199phot21_5DR9_hshwang.sav
; Redshift sources at R<30'
INDMMT          LONG      = Array[1555]
INDR02          LONG      = Array[1]
INDMMTRG        LONG      = Array[477]
INDSDSS         LONG      = Array[363]
IND2MRS         LONG      = Array[1]
INDC90          LONG      =           -1
INDNFPS         LONG      = Array[2]
INDP99          LONG      =           -1
INDW05          LONG      =           -1
INDZ90          LONG      =           -1
INDB02          LONG      = Array[1]
INDHO98         LONG      = Array[4]
INDNED          LONG      =           -1
INDU            LONG      =           -1
INDMMTR13       LONG      =           -1
        2404

; Redshift sources at R<65'
INDMMT          LONG      = Array[1555]
INDR02          LONG      = Array[8]
INDMMTRG        LONG      = Array[477]
INDSDSS         LONG      = Array[1282]
IND2MRS         LONG      = Array[2]
INDC90          LONG      = Array[1]
INDNFPS         LONG      = Array[2]
INDP99          LONG      = Array[1]
INDW05          LONG      = Array[1]
INDZ90          LONG      = Array[2]
INDB02          LONG      = Array[1]
INDHO98         LONG      = Array[4]
INDNED          LONG      =           -1
INDU            LONG      =           -1
INDN            LONG      =           -1
INDMMTR13       LONG      =           -1

; Redshift sources at R<65' - When publishing a paper 
INDMMT          LONG      = Array[775]
INDR02          LONG      = Array[11]
INDMMTRG        LONG      = Array[477]
INDSDSS         LONG      = Array[1285]
IND2MRS         LONG      = Array[2]
INDC90          LONG      = Array[1]
INDNFPS         LONG      = Array[2]
INDP99          LONG      = Array[1]
INDW05          LONG      = Array[1]
6.0650000
INDZ90          LONG      = Array[2]
INDB02          LONG      = Array[1]
INDHO98         LONG      = Array[4]
INDNED          LONG      =           -1
INDU            LONG      =           -1
INDMMTR13       LONG      =           -1
; =OK!

; list of fiberid =000 with zsource=SDSS
1237659330315681928 247.596366  38.783539 ; SDSS qso
1237655373036257686 247.076809  40.490219 ; SDSS but from different fiber
1237659324955820509 246.728966  38.633820 ; SDSS qso


.comp pcmr
pcmr
; => pcmr_a2199.eps
1237659330315419891 247.119005  39.152331 1 9  16.67   0.88  766.9   NED   1
1237659330315288687 246.929210  39.381253 1 9  19.13   0.82 -511.0   MMT   2


; Completeness
.comp complete
;complete, /sav
; => p2014_01_08_a2199.txt ; Send it to Matt!
; => comp_a2199phot21_5DR9_hshwang.sav
complete 
; => completeness.eps
; => A2199mor1ed.txt


;Central region
.comp Scomplete
Scomplete
; => Scomplete.eps

; For Galaxy Number Density Profile
.comp Acomplete.pro
Acomplete
; => Acomplete.eps ; 2D completeness
; => rmcomp_MLNa2107phot21_3DR10_hshwang.sav


.comp enva2199  ; (cmr_a2199phot21_5DR9_hshwang.sav, comp_a2199phot21_5DR9_hshwang.sav)
enva2199, /logx, /mag, /col
; => Clog_enva2199.eps
; => D2013_12_05_a2199.txt; Sent it to Matt (https://www.cfa.harvard.edu/~hhwang/WISEcfa/A2199/D2013_12_05_a2199.txt)
enva2199, /mag, /col
; => Cenva2199.eps


.comp zhist.pro
zhist
; => zhist.eps
mv zhist.eps zhistMMTraw.eps


;6) Large-scale view of Spatial distribution of galaxies
.comp large
large
; => large_a2199.eps
large, /phot
;=> ph_large.eps ; Just phot sample without z

START - send the master catalog to Hyunmin sometime in June!


;MMT observation for 2014A (CBP)
.comp target2014a.pro
target2014a
; => go for Xfitfibs

.comp propcmr
propcmr
; => propcmr.eps ; FOR MMT proposal
; => 0tarmor.txt
; => DONE


;MMT observation for 2014C (CBP)
.comp target2014c.pro
target2014c ; Ready submit 2014/Aug/6
; => go for Xfitfibs

.comp cpropcmr
cpropcmr
; => cpropcmr.eps ; FOR MMT proposal
; => 0tarmor.txt
; => DONE


;MMT observation for 2015b (CBP)
.comp target2015b.pro
target2015b
; => go for Xfitfibs ; Submitted 2015/May/11


;MMT observation for 2019a (HMSONG)
.comp target2019a.pro
target2019a
; => go for Xfitfibs ; To submit ; START

.comp propcmr
propcmr
; => propcmr.eps ; FOR MMT proposal
; => 0tarmor.txt
; => DONE



; Master catalogs
.comp catalog
catalog
; => Siden_A2199_20150130.txt
; => Sspec_A2199_20140130.txt
; => Ssdss_A2199_20140130.txt
; => Sphot_A2199_20140130.txt

.comp catalog
catalog, /one
; D1deg_A2199_20141201.txt ; To Tamura


;2.5 Flux Calibration of Spectra
;;.comp Ifluxspec ;
;;Ifluxspec
;;Hfluxspec,/new

.comp fluxapercal.pro
fluxapercal
;fluxapercal, /new


; Images & Spectra
.comp dr12querysp.pro ;
dr12querysp
dr12querysp, /boss
dr12querysp, /sv1
;->   sdssquery.sh
dir: /Users/hhwang/Research/Work/LIRGs/allimages/source sdssquery.sh


; Finding Chart with Spectra
.comp Ichart
Ichart, /arb, /spec, /obs, /flam;, /imsk
; => arb_sp_Imapchart.ps
;Ichart, /arb
; => arb_Hmapchart.ps

; Suzaku X-ray image from Tamura March 31, 2016
=> add1_lc1_pi192_548_subn_rate.xy

