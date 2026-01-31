PRO photmat;, ext = ext

xcut = 4.
;rcut = 22.75
rcut = 30.
c=2.99792458d5 ;km/s

dirg   = '/Users/hhwang/Research/Work/LIRGs/galcat/'
dircl  = '/Users/hhwang/Research/Work/WISEcfa/IndivCluster/A2199/z_DATA/'
;dirclo = '/Users/hhwang/Research/Work/WISEcfa/IndivCluster/A2199_DR7/data/'
dirclw = '/Users/hhwang/Research/Work/WISEcfa/IndivCluster/A2199/'
;dird0  = '/Users/hhwang/Research/Work/MMTraw/SPEC.2014A-UAO-G19.RAW.140219T1435/reduction/0100/'
;dird0  = '/Users/hhwang/Research/Work/MMTraw/2014.0219/reduction/0100/'
dird11  = '/Users/hhwang/Research/Work/WISEcfa/IndivCluster/A2199/z_SPECTRA/2007.0716/skysub_a2199new_1/'
dird12  = '/Users/hhwang/Research/Work/WISEcfa/IndivCluster/A2199/z_SPECTRA/2007.0717/skysub_a2199b_1/'
dird0  = '/Users/hhwang/Research/Work/MMTraw/'
dird2  = dird0 + '2014.0219/reduction/0100/skysub_a2199a_1/'
dird3  = dird0 + '2014.0219/reduction/0100/skysub_a2199a_2/'
dird4  = dird0 + '2015.0524/reduction/0100/skysub_a2199b15_1/'
dird5  = dird0 + '2015.0524/reduction/0100/skysub_a2199b15_2/'
;dird6  = dird0 + '2019.0309/reduction/0102/skysub_a2199a19_2cfaraw/'
dird6  = dird0 + '2019.0309/reduction/0102/skysub_a2199a19_2/'
dird7  = dird0 + '2019.0428/reduction/0100/skysub_a2199a19_3/'
dird8  = dird0 + '2019.0429/reduction/0100/skysub_a2199a19_1/'
dird9  = dird0 + '2019.0501/reduction/0100/skysub_a2199a19_4/'
;dird   = '/Users/hhwang/Research/Work/MMTraw/SPEC.2014A-UAO-G19.RAW.140219T1435/reduction/0100/'
;dirsp  = '/Users/hhwang/Research/Work/WISEcfa/IndivCluster/A2199/z_SPECTRA/'

;BCG
;racen = 247.15933d
;decen =  39.55127d

;X-ray
racen = 247.15820d
decen =  39.54870d


; KIAS MMT data - 2019a - 1
readcol, dird9 + 'zout_a2199a19_4', $
  ofilename, sra, sdec, ocz, oczerr, oczxcr, ovelqual, $
  f ='a,a,a,d,d, f,a', skiplin = 2

  ra = ocz * 0. - 99.
  de = ocz * 0. - 99.
  for j = 0, n_elements(sra) - 1 do begin
     STRINGAD, sra[j] + ' ' + sdec[j], tomk2_ra, tomk2_dec
     ra[j] = tomk2_ra
     de[j] = tomk2_dec
  endfor

ind = where(oczxcr ge xcut and ovelqual eq '_', cnt)
if cnt ge 1 then ovelqual[ind] = 'N'
ind = where(ovelqual eq 'Q' or ovelqual eq 'N', cnt)
 ofilename9 = ofilename[ind]
        ra9 = ra[ind]
        de9 = de[ind]
       ocz9 = ocz[ind]
    oczerr9 = oczerr[ind]
    oczxcr9 = oczxcr[ind]
  ovelqual9 = ovelqual[ind]
odfilename9 = strarr(n_elements(ofilename9)) + 'skysub_a2199a19_4'

; KIAS MMT data - 2019a - 1
readcol, dird8 + 'zout_a2199a19_1', $
  ofilename, sra, sdec, ocz, oczerr, oczxcr, ovelqual, $
  f ='a,a,a,d,d, f,a', skiplin = 2

  ra = ocz * 0. - 99.
  de = ocz * 0. - 99.
  for j = 0, n_elements(sra) - 1 do begin
     STRINGAD, sra[j] + ' ' + sdec[j], tomk2_ra, tomk2_dec
     ra[j] = tomk2_ra
     de[j] = tomk2_dec
  endfor

ind = where(oczxcr ge xcut and ovelqual eq '_', cnt)
if cnt ge 1 then ovelqual[ind] = 'N'
ind = where(ovelqual eq 'Q' or ovelqual eq 'N', cnt)
 ofilename8 = ofilename[ind]
        ra8 = ra[ind]
        de8 = de[ind]
       ocz8 = ocz[ind]
    oczerr8 = oczerr[ind]
    oczxcr8 = oczxcr[ind]
  ovelqual8 = ovelqual[ind]
odfilename8 = strarr(n_elements(ofilename8)) + 'skysub_a2199a19_1'

help, ovelqual8

; KIAS MMT data - 2019a - 3
readcol, dird7 + 'zout_a2199a19_3', $
  ofilename, sra, sdec, ocz, oczerr, oczxcr, ovelqual, $
  f ='a,a,a,d,d, f,a', skiplin = 2

  ra = ocz * 0. - 99.
  de = ocz * 0. - 99.
  for j = 0, n_elements(sra) - 1 do begin
     STRINGAD, sra[j] + ' ' + sdec[j], tomk2_ra, tomk2_dec
     ra[j] = tomk2_ra
     de[j] = tomk2_dec
  endfor

ind = where(oczxcr ge xcut and ovelqual eq '_', cnt)
if cnt ge 1 then ovelqual[ind] = 'N'
ind = where(ovelqual eq 'Q' or ovelqual eq 'N', cnt)
 ofilename7 = ofilename[ind]
        ra7 = ra[ind]
        de7 = de[ind]
       ocz7 = ocz[ind]
    oczerr7 = oczerr[ind]
    oczxcr7 = oczxcr[ind]
  ovelqual7 = ovelqual[ind]
odfilename7 = strarr(n_elements(ofilename7)) + 'skysub_a2199a19_3'


; KIAS MMT data - 2019a - 2
readcol, dird6 + 'zout_a2199a19_2', $
  ofilename, sra, sdec, ocz, oczerr, oczxcr, ovelqual, $
  f ='a,a,a,d,d, f,a', skiplin = 2

  ra = ocz * 0. - 99.
  de = ocz * 0. - 99.
  for j = 0, n_elements(sra) - 1 do begin
     STRINGAD, sra[j] + ' ' + sdec[j], tomk2_ra, tomk2_dec
     ra[j] = tomk2_ra
     de[j] = tomk2_dec
  endfor

ind = where(oczxcr ge xcut and ovelqual eq '_', cnt)
if cnt ge 1 then ovelqual[ind] = 'N'
ind = where(ovelqual eq 'Q' or ovelqual eq 'N', cnt)
ind = where((ovelqual eq 'Q' or ovelqual eq 'N') and $
             ocz/c lt 0.6, cnt) ; just for this config...
;ind = where((ovelqual eq 'Q' or ovelqual eq 'N') and $
;	ofilename ne '006.a2199a19_2_1344.ms.fits' and $
;	ofilename ne '138.a2199a19_2_1001.ms.fits' and $
;	ofilename ne '259.a2199a19_2_1927.ms.fits' and $
;	ofilename ne '255.a2199a19_2_2626.ms.fits' and $
;	ofilename ne '129.a2199a19_2_1327.ms.fits' and $
;	ofilename ne '111.a2199a19_2_695.ms.fits' and $
;	ofilename ne '017.a2199a19_2_826.ms.fits', cnt)
 ofilename6 = ofilename[ind]
        ra6 = ra[ind]
        de6 = de[ind]
       ocz6 = ocz[ind]
    oczerr6 = oczerr[ind]
    oczxcr6 = oczxcr[ind]
  ovelqual6 = ovelqual[ind]
odfilename6 = strarr(n_elements(ofilename6)) + 'skysub_a2199a19_2'


; KIAS MMT data - 2015b - 2
readcol, dird5 + 'zout_a2199b15_2', $
  ofilename, sra, sdec, ocz, oczerr, oczxcr, ovelqual, $
  f ='a,a,a,d,d, f,a', skiplin = 2

  ra = ocz * 0. - 99.
  de = ocz * 0. - 99.
  for j = 0, n_elements(sra) - 1 do begin
     STRINGAD, sra[j] + ' ' + sdec[j], tomk2_ra, tomk2_dec
     ra[j] = tomk2_ra
     de[j] = tomk2_dec
  endfor

ind = where(oczxcr ge xcut and ovelqual eq '_', cnt)
if cnt ge 1 then ovelqual[ind] = 'N'
ind = where(ovelqual eq 'Q' or ovelqual eq 'N', cnt)
 ofilename5 = ofilename[ind]
        ra5 = ra[ind]
        de5 = de[ind]
       ocz5 = ocz[ind]
    oczerr5 = oczerr[ind]
    oczxcr5 = oczxcr[ind]
  ovelqual5 = ovelqual[ind]
odfilename5 = strarr(n_elements(ofilename5)) + 'skysub_a2199b15_2'


; KIAS MMT data - 2015b - 1
readcol, dird4 + 'zout_a2199b15_1', $
  ofilename, sra, sdec, ocz, oczerr, oczxcr, ovelqual, $
  f ='a,a,a,d,d, f,a', skiplin = 2

  ra = ocz * 0. - 99.
  de = ocz * 0. - 99.
  for j = 0, n_elements(sra) - 1 do begin
     STRINGAD, sra[j] + ' ' + sdec[j], tomk2_ra, tomk2_dec
     ra[j] = tomk2_ra
     de[j] = tomk2_dec
  endfor

ind = where(oczxcr ge xcut and ovelqual eq '_', cnt)
if cnt ge 1 then ovelqual[ind] = 'N'
ind = where(ovelqual eq 'Q' or ovelqual eq 'N', cnt)
 ofilename4 = ofilename[ind]
        ra4 = ra[ind]
        de4 = de[ind]
       ocz4 = ocz[ind]
    oczerr4 = oczerr[ind]
    oczxcr4 = oczxcr[ind]
  ovelqual4 = ovelqual[ind]
odfilename4 = strarr(n_elements(ofilename4)) + 'skysub_a2199b15_1'


; KIAS MMT data - 2014a
readcol, dird3 + 'zout_a2199a_2', $
  ofilename, sra, sdec, ocz, oczerr, oczxcr, ovelqual, $
  f ='a,a,a,d,d, f,a', skiplin = 2

  ra = ocz * 0. - 99.
  de = ocz * 0. - 99.
  for j = 0, n_elements(sra) - 1 do begin
     STRINGAD, sra[j] + ' ' + sdec[j], tomk2_ra, tomk2_dec
     ra[j] = tomk2_ra
     de[j] = tomk2_dec
  endfor

;ind = where(ovelqual eq 'Q')
ind = where(oczxcr ge xcut and ovelqual eq '_', cnt)
if cnt ge 1 then ovelqual[ind] = 'N'
;ind = where(ovelqual eq 'Q' or (oczxcr ge xcut and ovelqual eq '_'), cnt)
ind = where(ovelqual eq 'Q' or ovelqual eq 'N', cnt)
ofilename3 = ofilename[ind]
ra3 = ra[ind]
de3 = de[ind]
ocz3 = ocz[ind]
oczerr3 = oczerr[ind]
oczxcr3 = oczxcr[ind]
ovelqual3 = ovelqual[ind]
;ovelqual3 = replicate('Q', cnt)
odfilename3 = strarr(n_elements(ofilename3)) + 'skysub_a2199a_2'


; KIAS MMT data 
readcol, dird2 + 'zout_a2199a_1', $
  ofilename, sra, sdec, ocz, oczerr, oczxcr, ovelqual, $
  f ='a,a,a,d,d, f,a', skiplin = 2

  ra = ocz * 0. - 99.
  de = ocz * 0. - 99.
  for j = 0, n_elements(sra) - 1 do begin
     STRINGAD, sra[j] + ' ' + sdec[j], tomk2_ra, tomk2_dec
     ra[j] = tomk2_ra
     de[j] = tomk2_dec
  endfor

ind = where(oczxcr ge xcut and ovelqual eq '_', cnt)
if cnt ge 1 then ovelqual[ind] = 'N'
;ind = where(ovelqual eq 'Q' or (oczxcr ge xcut and ovelqual eq '_'), cnt)
ind = where(ovelqual eq 'Q' or ovelqual eq 'N', cnt)
ofilename2 = ofilename[ind]
ra2 = ra[ind]
de2 = de[ind]
ocz2 = ocz[ind]
oczerr2 = oczerr[ind]
oczxcr2 = oczxcr[ind]
ovelqual2 = ovelqual[ind]
;ovelqual2 = replicate('Q', cnt)
odfilename2 = strarr(n_elements(ofilename2)) + 'skysub_a2199a_1'

help, ovelqual2
help, ovelqual3
help, ovelqual4
help, ovelqual5


; Rines MMT data - 1
readcol, dird11 + 'zout_a2199new_1', $
  ofilename, sra, sdec, ocz, oczerr, oczxcr, ovelqual, $
  f ='a,a,a,d,d, f,a', skiplin = 2

  ra = ocz * 0. - 99.
  de = ocz * 0. - 99.
  for j = 0, n_elements(sra) - 1 do begin
     STRINGAD, sra[j] + ' ' + sdec[j], tomk2_ra, tomk2_dec
     ra[j] = tomk2_ra
     de[j] = tomk2_dec
  endfor

;ind = where(ovelqual eq 'Q' or ovelqual eq '?', cnt)
ind = where(ovelqual ne 'XXX', cnt)
 ofilename11 = ofilename[ind]
        ra11 = ra[ind]
        de11 = de[ind]
       ocz11 = ocz[ind]
    oczerr11 = oczerr[ind]
    oczxcr11 = oczxcr[ind]
  ovelqual11 = ovelqual[ind]
odfilename11 = strarr(n_elements(ofilename11)) + 'skysub_a2199new_1'


; Rines MMT data - 2
readcol, dird12 + 'zout_a2199b_1', $
  ofilename, sra, sdec, ocz, oczerr, oczxcr, ovelqual, $
  f ='a,a,a,d,d, f,a', skiplin = 2

  ra = ocz * 0. - 99.
  de = ocz * 0. - 99.
  for j = 0, n_elements(sra) - 1 do begin
     STRINGAD, sra[j] + ' ' + sdec[j], tomk2_ra, tomk2_dec
     ra[j] = tomk2_ra
     de[j] = tomk2_dec
  endfor

;ind = where(ovelqual eq 'Q' or ovelqual eq '?', cnt)
ind = where(ovelqual ne 'XXX', cnt)
 ofilename12 = ofilename[ind]
        ra12 = ra[ind]
        de12 = de[ind]
       ocz12 = ocz[ind]
    oczerr12 = oczerr[ind]
    oczxcr12 = oczxcr[ind]
  ovelqual12 = ovelqual[ind]
odfilename12 = strarr(n_elements(ofilename12)) + 'skysub_a2199b_1'


 odfilename1 = [odfilename11, odfilename12]
 ofilename1 = [ofilename11, ofilename12]
 ra1 = [ra11, ra12]
 de1 = [de11, de12]
 ocz1    = [ocz11, ocz12]
 oczerr1 = [oczerr11, oczerr12]
 oczxcr1 = [oczxcr11, oczxcr12]
 ovelqual1 = [ovelqual11, ovelqual12]

ind = where(ovelqual1 ne 'Q', cnt)
if cnt ge 1 then ovelqual1[ind] = 'N' ; Just for A2199 because Rines+08 published some ?/X redshifts as well.

readcol, dircl + 'aj262373_mrt1ed.txt', $
  rah, ram, ras, ded, dem, des, oocz, ooczerr, ooczxcr, $
  f ='i,i,f, i,i,f, f,f', skipl = 19

ra = 15d0 * (rah + ram/60. + ras/3600.)
de =  1d0 * (ded + dem/60. + des/3600.)
ngal = n_elements(ra)
 ofilename = strarr(ngal) + 'nn.fits'
odfilename = strarr(ngal) + 'NN'
  ovelqual = strarr(ngal) + 'Q'

;-----------------------
tolerance= 0.5
hs_radecmatch,tolerance, ra, de, ra1, de1, $
 indxfile1call,indxfile2call,nonindxfile1call,nonindxfile2call, $
 dra12,ddec12,dist12,pa12,kindx12,matchednum12
par = 'Rines'
hs_match, dra12, ddec12, tolerance, oocz, ofilename1, $
 indxfile1call, indxfile2call, kindx12, dist12, $
 dir = dirclw, par = par

 ofilename[indxfile1call] =  ofilename1[indxfile2call]
odfilename[indxfile1call] = odfilename1[indxfile2call]
  ovelqual[indxfile1call] =   ovelqual1[indxfile2call]

ind = where(ofilename eq '104.a2199new_1_9.ms.fits', cnt)
if cnt ge 1 then begin
  ra[ind] = 247.221734954d
  de[ind] = 39.560005372d
endif

 tmp_ofilename = [ofilename2, ofilename3, ofilename4, ofilename5, $
   ofilename6, ofilename7, ofilename8, ofilename9]
 tmp_ra = [ra2, ra3, ra4, ra5, $
   ra6, ra7, ra8, ra9]
 tmp_de = [de2, de3, de4, de5, $
   de6, de7, de8, de9]

 odfilename = [odfilename, odfilename2, odfilename3, odfilename4, odfilename5, $
   odfilename6, odfilename7, odfilename8, odfilename9]
 ofilename = [ofilename, ofilename2, ofilename3, ofilename4, ofilename5, $
   ofilename6, ofilename7, ofilename8, ofilename9]
 ra = [ra, ra2, ra3, ra4, ra5, $
   ra6, ra7, ra8, ra9]
 de = [de, de2, de3, de4, de5, $
   de6, de7, de8, de9]
 ocz    = [oocz, ocz2, ocz3, ocz4, ocz5, $
   ocz6, ocz7, ocz8, ocz9]
 oczerr = [ooczerr, oczerr2, oczerr3, oczerr4, oczerr5, $
   oczerr6, oczerr7, oczerr8, oczerr9]
 oczxcr = [ooczxcr, oczxcr2, oczxcr3, oczxcr4, oczxcr5, $
   oczxcr6, oczxcr7, oczxcr8, oczxcr9]
 ovelqual = [ovelqual, ovelqual2, ovelqual3, ovelqual4, ovelqual5, $
   ovelqual6, ovelqual7, ovelqual8, ovelqual9]

; cf_ocz    = [oocz, cf_ocz2, cf_ocz3]
; cf_oczerr = [ooczerr, cf_oczerr2, cf_oczerr3]
; cf_oczxcr = [ooczxcr, cf_oczxcr2, cf_oczxcr3]


;ind = where(cz gt 0)
;ra = ra[ind]
;de = de[ind]
;cz = cz[ind]

;dr7file = 'MLNa383phot21_32_hshwang.'
dr7file = 'TAGMLNa2199phot_hshwang.' ; p.petroMag_r-p.extinction_r <= 20.11
goto, jump2
readcol, dircl + dr7file +'csv' , $
  dr7_objid, dr7_ra, dr7_dec, $
  dr7_petroMag_u,dr7_petroMagerr_u,dr7_petroMag_g,dr7_petroMagerr_g,dr7_petroMag_r,dr7_petroMagerr_r,$
  dr7_petroMag_i,dr7_petroMagerr_i,dr7_petroMag_z,dr7_petroMagerr_z,$
  dr7_modelMag_u,dr7_modelMagerr_u,dr7_modelMag_g,dr7_modelMagerr_g,dr7_modelMag_r,dr7_modelMagerr_r, $
  dr7_modelMag_i,dr7_modelMagerr_i,dr7_modelMag_z,dr7_modelMagerr_z,$
  f = 'a,d,d, f,f,f,f,f, f,f,f,f,f, f,f,f,f,f, f,f,f,f,f'
readcol, dircl + dr7file + 'csv', $
  dr7_extinction_u,dr7_extinction_g,dr7_extinction_r,dr7_extinction_i,dr7_extinction_z,$
  dr7_petroRad_r,dr7_petroRadErr_r, $
  dr7_run,dr7_rerun,dr7_camCol,dr7_field,dr7_efac,dr7_probPSF, $
  dr7_fiberMag_u,dr7_fiberMagerr_u, $
  dr7_fiberMag_g,dr7_fiberMagerr_g, $
  dr7_fiberMag_r,dr7_fiberMagerr_r, $
  dr7_fiberMag_i,dr7_fiberMagerr_i, $
  dr7_fiberMag_z,dr7_fiberMagerr_z, $
  f = 'x,x,x, x,x,x,x,x, x,x,x,x,x, x,x,x,x,x, x,x,x,x,x,' + $
   'f,f,f,f,f, f,f, a,a,a,a,f, i, f,f,f,f,f,f,f,f,f,f'

save, FILENAME= dircl + dr7file + 'sav', /compress, $
  dr7_objid, dr7_ra, dr7_dec, $
  dr7_petroMag_u,dr7_petroMagerr_u,dr7_petroMag_g,dr7_petroMagerr_g,dr7_petroMag_r,dr7_petroMagerr_r,$
  dr7_petroMag_i,dr7_petroMagerr_i,dr7_petroMag_z,dr7_petroMagerr_z,$
  dr7_modelMag_u,dr7_modelMagerr_u,dr7_modelMag_g,dr7_modelMagerr_g,dr7_modelMag_r,dr7_modelMagerr_r, $
  dr7_modelMag_i,dr7_modelMagerr_i,dr7_modelMag_z,dr7_modelMagerr_z,$
  dr7_extinction_u,dr7_extinction_g,dr7_extinction_r,dr7_extinction_i,dr7_extinction_z,$
  dr7_petroRad_r,dr7_petroRadErr_r, $
  dr7_run,dr7_rerun,dr7_camCol,dr7_field,dr7_efac,dr7_probPSF, $
  dr7_fiberMag_u,dr7_fiberMagerr_u, $
  dr7_fiberMag_g,dr7_fiberMagerr_g, $
  dr7_fiberMag_r,dr7_fiberMagerr_r, $
  dr7_fiberMag_i,dr7_fiberMagerr_i, $
  dr7_fiberMag_z,dr7_fiberMagerr_z
jump2:
restore, dircl + dr7file + 'sav'



file = 'a2199phot21_5DR9_hshwang.'
goto, jump3
readcol, dircl + file +'csv' , $
  p_objid, p_ra, p_dec, $
  p_petroMag_u,p_petroMagerr_u,p_petroMag_g,p_petroMagerr_g,p_petroMag_r,p_petroMagerr_r,$
  p_petroMag_i,p_petroMagerr_i,p_petroMag_z,p_petroMagerr_z,$
  p_modelMag_u,p_modelMagerr_u,p_modelMag_g,p_modelMagerr_g,p_modelMag_r,p_modelMagerr_r, $
  p_modelMag_i,p_modelMagerr_i,p_modelMag_z,p_modelMagerr_z,$
  f = 'a,d,d, f,f,f,f,f, f,f,f,f,f, f,f,f,f,f, f,f,f,f,f'
;if keyword_set(ext) then $
readcol, dircl + file + 'csv', $
  p_extinction_u,p_extinction_g,p_extinction_r,p_extinction_i,p_extinction_z,$
  p_petroRad_r,p_petroRadErr_r, $
  p_run,p_rerun,p_camCol,p_field,p_efac,p_probPSF, $
  p_fiberMag_u,p_fiberMagerr_u, $
  p_fiberMag_g,p_fiberMagerr_g, $
  p_fiberMag_r,p_fiberMagerr_r, $
  p_fiberMag_i,p_fiberMagerr_i, $
  p_fiberMag_z,p_fiberMagerr_z, $
  p_deVRad_i, p_deVAB_i, $
  f = 'x,x,x, x,x,x,x,x, x,x,x,x,x, x,x,x,x,x, x,x,x,x,x,' + $
      'f,f,f,f,f, f,f, a,a,a,a,f, i, f,f,f,f,f,f,f,f,f,f, x,f,f'

;goto, jump3
save, FILENAME= dircl + file + 'sav', /compress, $
  p_objid, p_ra, p_dec, $
  p_petroMag_u,p_petroMagerr_u,p_petroMag_g,p_petroMagerr_g,p_petroMag_r,p_petroMagerr_r,$
  p_petroMag_i,p_petroMagerr_i,p_petroMag_z,p_petroMagerr_z,$
  p_modelMag_u,p_modelMagerr_u,p_modelMag_g,p_modelMagerr_g,p_modelMag_r,p_modelMagerr_r, $
  p_modelMag_i,p_modelMagerr_i,p_modelMag_z,p_modelMagerr_z,$
  p_extinction_u,p_extinction_g,p_extinction_r,p_extinction_i,p_extinction_z,$
  p_petroRad_r,p_petroRadErr_r, $
  p_run,p_rerun,p_camCol,p_field,p_efac,p_probPSF, $
  p_fiberMag_u,p_fiberMagerr_u, $
  p_fiberMag_g,p_fiberMagerr_g, $
  p_fiberMag_r,p_fiberMagerr_r, $
  p_fiberMag_i,p_fiberMagerr_i, $
  p_fiberMag_z,p_fiberMagerr_z, $
  p_deVRad_i, p_deVAB_i

jump3:
restore, dircl + file + 'sav'

ind = where(p_objid eq '1237659326029366507', cnt)
if cnt ge 1 then begin
   p_ra[ind] = 247.02156d
  p_dec[ind] =  39.49932d
endif

inddr9 = where(p_petroMag_r-p_extinction_r le 21.5 or $
	       p_objid eq '1237655373036519580' or $ ; Rines & Geller
	       p_objid eq '1237659330315223132' or $ ; Rines & Geller
	       p_objid eq '1237659330315288582' or $ ; Rines & Geller
	       p_objid eq '1237659326029365403', cnt9) ; Rines & Geller
nondr7 = where(dr7_objid eq '587733604804395254' or $
               dr7_objid eq '587733604804461124' or $
               dr7_objid eq '587729651810697226' or $
               dr7_objid eq '587729651810697225' or $
               dr7_objid eq '587729653423276237' or $
               dr7_objid eq '587733604804460611', cnt) & help, nondr7
if cnt ge 1 then begin 
p_objid = [p_objid[inddr9], dr7_objid[nondr7]]
p_ra = [p_ra[inddr9], dr7_ra[nondr7]]
p_dec= [p_dec[inddr9], dr7_dec[nondr7]]

p_petroMag_u = [   p_petroMag_u[inddr9],    dr7_petroMag_u[nondr7]]
p_petroMagerr_u = [p_petroMagerr_u[inddr9], dr7_petroMagerr_u[nondr7]]
p_petroMag_g = [   p_petroMag_g[inddr9],    dr7_petroMag_g[nondr7]]
p_petroMagerr_g = [p_petroMagerr_g[inddr9], dr7_petroMagerr_g[nondr7]]
p_petroMag_r = [   p_petroMag_r[inddr9],    dr7_petroMag_r[nondr7]]
p_petroMagerr_r = [p_petroMagerr_r[inddr9], dr7_petroMagerr_r[nondr7]]
p_petroMag_i = [   p_petroMag_i[inddr9],    dr7_petroMag_i[nondr7]]
p_petroMagerr_i = [p_petroMagerr_i[inddr9], dr7_petroMagerr_i[nondr7]]
p_petroMag_z = [   p_petroMag_z[inddr9],    dr7_petroMag_z[nondr7]]
p_petroMagerr_z = [p_petroMagerr_z[inddr9], dr7_petroMagerr_z[nondr7]]

p_modelMag_u = [   p_modelMag_u[inddr9],    dr7_modelMag_u[nondr7]]
p_modelMagerr_u = [p_modelMagerr_u[inddr9], dr7_modelMagerr_u[nondr7]]
p_modelMag_g = [   p_modelMag_g[inddr9],    dr7_modelMag_g[nondr7]]
p_modelMagerr_g = [p_modelMagerr_g[inddr9], dr7_modelMagerr_g[nondr7]]
p_modelMag_r = [   p_modelMag_r[inddr9],    dr7_modelMag_r[nondr7]]
p_modelMagerr_r = [p_modelMagerr_r[inddr9], dr7_modelMagerr_r[nondr7]]
p_modelMag_i = [   p_modelMag_i[inddr9],    dr7_modelMag_i[nondr7]]
p_modelMagerr_i = [p_modelMagerr_i[inddr9], dr7_modelMagerr_i[nondr7]]
p_modelMag_z = [   p_modelMag_z[inddr9],    dr7_modelMag_z[nondr7]]
p_modelMagerr_z = [p_modelMagerr_z[inddr9], dr7_modelMagerr_z[nondr7]]

p_fiberMag_u = [   p_fiberMag_u[inddr9],    dr7_fiberMag_u[nondr7]]
p_fiberMagerr_u = [p_fiberMagerr_u[inddr9], dr7_fiberMagerr_u[nondr7]]
p_fiberMag_g = [   p_fiberMag_g[inddr9],    dr7_fiberMag_g[nondr7]]
p_fiberMagerr_g = [p_fiberMagerr_g[inddr9], dr7_fiberMagerr_g[nondr7]]
p_fiberMag_r = [   p_fiberMag_r[inddr9],    dr7_fiberMag_r[nondr7]]
p_fiberMagerr_r = [p_fiberMagerr_r[inddr9], dr7_fiberMagerr_r[nondr7]]
p_fiberMag_i = [   p_fiberMag_i[inddr9],    dr7_fiberMag_i[nondr7]]
p_fiberMagerr_i = [p_fiberMagerr_i[inddr9], dr7_fiberMagerr_i[nondr7]]
p_fiberMag_z = [   p_fiberMag_z[inddr9],    dr7_fiberMag_z[nondr7]]
p_fiberMagerr_z = [p_fiberMagerr_z[inddr9], dr7_fiberMagerr_z[nondr7]]

p_extinction_u = [p_extinction_u[inddr9], dr7_extinction_u[nondr7]]
p_extinction_g = [p_extinction_g[inddr9], dr7_extinction_g[nondr7]]
p_extinction_r = [p_extinction_r[inddr9], dr7_extinction_r[nondr7]]
p_extinction_i = [p_extinction_i[inddr9], dr7_extinction_i[nondr7]]
p_extinction_z = [p_extinction_z[inddr9], dr7_extinction_z[nondr7]]

p_petroRad_r = [p_petroRad_r[inddr9], dr7_petroRad_r[nondr7]]
p_petroRaderr_r = [p_petroRaderr_r[inddr9], dr7_petroRaderr_r[nondr7]]

p_run= [p_run[inddr9], dr7_run[nondr7]]
p_rerun= [p_rerun[inddr9], dr7_rerun[nondr7]]
p_camcol= [p_camcol[inddr9], dr7_camcol[nondr7]]
p_field = [p_field[inddr9],  dr7_field[nondr7]]
p_efac = [p_efac[inddr9],  dr7_efac[nondr7]]
p_probpsf = [p_probpsf[inddr9],  dr7_probpsf[nondr7]]

p_deVRad_i = [p_deVRad_i[inddr9], fltarr(cnt) - 9.]
p_deVAB_i = [p_deVAB_i[inddr9], fltarr(cnt) - 9.]
endif

p_phtype0 = intarr(n_elements(p_objid)) + 9

restore, dirg + 'Mgaldr12_garbage.sav'
match, p_objid, gs3_objid, suba, subb, count = cnt
help,  p_objid, gs3_objid, suba, subb, cnt
if cnt gt 0 then $
  p_phtype0[suba] = 4


readcol, dircl + 'A2199mor1ed.txt', id1, mor1, f ='a, x,x, i'
match, p_objid, id1, suba, subb
p_phtype0[suba] = mor1[subb]
help,  p_objid, id1, suba, subb

ind = where(p_phtype0 eq 3, cnt)
if cnt ge 1 then $
  p_probpsf[ind] = 1 ; point sources

ind = where(p_phtype0 eq 4, cnt)
if cnt ge 1 then $
  p_probpsf[ind] = 4 ; point sources

;tmp = where(p_objid eq '1237654652560867404') & help, tmp
ind = where(p_petroMag_r ge 0 and $
 p_probpsf ne 4, comp=nind) & help, nind
; p_objid ne '1237676672859373592', comp=nind) & help, nind

  p_phtype0 = p_phtype0[ind]
  p_objid = p_objid[ind]
  p_ra = p_ra[ind]
  p_dec = p_dec[ind]
  p_petroMag_u = p_petroMag_u[ind]
  p_petroMagerr_u = p_petroMagerr_u[ind]
  p_petroMag_g = p_petroMag_g[ind]
  p_petroMagerr_g = p_petroMagerr_g[ind]
  p_petroMag_r = p_petroMag_r[ind]
  p_petroMagerr_r = p_petroMagerr_r[ind]
  p_petroMag_i = p_petroMag_i[ind]
  p_petroMagerr_i = p_petroMagerr_i[ind]
  p_petroMag_z = p_petroMag_z[ind]
  p_petroMagerr_z = p_petroMagerr_z[ind]
  p_modelMag_u = p_modelMag_u[ind]
  p_modelMagerr_u = p_modelMagerr_u[ind]
  p_modelMag_g = p_modelMag_g[ind]
  p_modelMagerr_g = p_modelMagerr_g[ind]
  p_modelMag_r = p_modelMag_r[ind]
  p_modelMagerr_r = p_modelMagerr_r[ind]
  p_modelMag_i = p_modelMag_i[ind]
  p_modelMagerr_i = p_modelMagerr_i[ind]
  p_modelMag_z = p_modelMag_z[ind]
  p_modelMagerr_z = p_modelMagerr_z[ind]

  p_fiberMag_u = p_fiberMag_u[ind]
  p_fiberMagerr_u = p_fiberMagerr_u[ind]
  p_fiberMag_g = p_fiberMag_g[ind]
  p_fiberMagerr_g = p_fiberMagerr_g[ind]
  p_fiberMag_r = p_fiberMag_r[ind]
  p_fiberMagerr_r = p_fiberMagerr_r[ind]
  p_fiberMag_i = p_fiberMag_i[ind]
  p_fiberMagerr_i = p_fiberMagerr_i[ind]
  p_fiberMag_z = p_fiberMag_z[ind]
  p_fiberMagerr_z = p_fiberMagerr_z[ind]

  p_extinction_u = p_extinction_u[ind]
  p_extinction_g = p_extinction_g[ind]
  p_extinction_r = p_extinction_r[ind]
  p_extinction_i = p_extinction_i[ind]
  p_extinction_z = p_extinction_z[ind]
  p_petroRad_r = p_petroRad_r[ind]
  p_petroRadErr_r = p_petroRadErr_r[ind]
  p_deVRad_i= p_deVRad_i[ind]
  p_deVAB_i= p_deVAB_i[ind]
  p_run = p_run[ind]
  p_rerun = p_rerun[ind]
  p_camCol = p_camCol[ind]
  p_field = p_field[ind]
  p_efac = p_efac[ind]
  p_probpsf = p_probpsf[ind]




help, ra, de, ocz, ofilename
;tolerance = 1.
tolerance = 2.5
for i = 0l, n_elements(ra) -1l do begin
  gcirc, 2, ra[i], de[i], p_ra, p_dec, distg
  ind = where(distg le tolerance, cnt)
  if cnt le 0 then $
    print, i, ra[i], de[i], ocz[i], ofilename[i], $
      f='(i5, 2d11.6, d9.1, a30)'
endfor


help, ra, p_ra
hs_radecmatch,tolerance, ra, de, p_ra, p_dec, $
  indxfile1call,indxfile2call,nonindxfile1call,nonindxfile2call,$
  dra12,ddec12,dist12,pa12,kindx12,matchednum12
par = 'photmat'
hs_match, dra12, ddec12, tolerance, ofilename, p_objid, $
   indxfile1call, indxfile2call, kindx12, dist12, $
   dir = dirclw, par = par

toto = where(odfilename[indxfile1call] eq 'skysub_a2199a_1' or $
             odfilename[indxfile1call] eq 'skysub_a2199a_2' or $
             odfilename[indxfile1call] eq 'skysub_a2199b15_1' or $
             odfilename[indxfile1call] eq 'skysub_a2199b15_2', cnt)
help, toto
toto = where(odfilename[nonindxfile1call] eq 'skysub_a2199a_1' or $
             odfilename[nonindxfile1call] eq 'skysub_a2199a_2' or $
             odfilename[nonindxfile1call] eq 'skysub_a2199b15_1' or $
             odfilename[nonindxfile1call] eq 'skysub_a2199b15_2', cnt)
help, toto
toto = where(odfilename[indxfile1call] eq 'skysub_a2199new_1' or $
             odfilename[indxfile1call] eq 'skysub_a2199b_1', cnt)
help, toto
;stop
toto = where(odfilename[nonindxfile1call] eq 'skysub_a2199new_1' or $
             odfilename[nonindxfile1call] eq 'skysub_a2199b_1', cnt)
if cnt ge 1 then begin
tmp = nonindxfile1call[toto]
for i = 0, cnt -1 do $
   print, ofilename[tmp[i]], $
    ra[tmp[i]], de[tmp[i]], $
    ocz[tmp[i]], $
    i + 1, $
    f = '(a30, 2d11.6, f9.1, i3)'
;for i = 0, n_elements(nonindxfile1call)-1 do $
;   print, ofilename[nonindxfile1call[i]], $
;    ra[nonindxfile1call[i]], de[nonindxfile1call[i]], $
;    ocz[nonindxfile1call[i]], $
;    i + 1, $
;    f = '(a30, 2d11.6, f9.1, i3)'
endif
help, toto
;stop

;stop
hs_stat, p_petroMag_r[indxfile2call]

ind = where(dist12 gt 0.5, cnt)
help, ind
;cnt = 10
if cnt ge 1 then $
 for i = 0, cnt-1 do $
   print, p_objid[indxfile2call[ind[i]]], $
    p_ra[indxfile2call[ind[i]]], p_dec[indxfile2call[ind[i]]], $
    ofilename[indxfile1call[ind[i]]], $
    ra[indxfile1call[ind[i]]], de[indxfile1call[ind[i]]], $
    i + 1, $
    f = '(2(a30, 2d11.6), i3)'

;stop
tmp = reverse(sort(p_petroMag_r[indxfile2call]))
ind = tmp[0]
print, p_objid[indxfile2call[ind]], p_petroMag_r[indxfile2call[ind]], ocz[indxfile1call[ind]], ovelqual[indxfile1call[ind]]
ind = tmp[1]
print, p_objid[indxfile2call[ind]], p_petroMag_r[indxfile2call[ind]]

;if keyword_set(ext) then begin
  tmp = reverse(sort(p_petroMag_r[indxfile2call]-p_extinction_r[indxfile2call]))
  ind = tmp[0]
  print, p_objid[indxfile2call[ind]], $
    p_petroMag_r[indxfile2call[ind]]-p_extinction_r[indxfile2call[ind]]
  ind = tmp[1]
  print, p_objid[indxfile2call[ind]], $
    p_petroMag_r[indxfile2call[ind]]-p_extinction_r[indxfile2call[ind]]
  ind = tmp[2]
  print, p_objid[indxfile2call[ind]], $
    p_petroMag_r[indxfile2call[ind]]-p_extinction_r[indxfile2call[ind]]
  ind = tmp[3]
  print, p_objid[indxfile2call[ind]], $
    p_petroMag_r[indxfile2call[ind]]-p_extinction_r[indxfile2call[ind]]


ngal = n_elements(p_ra)
 z_filename = strarr(ngal) + 'nn.fits'
z_dfilename = strarr(ngal) + 'NN'
z_mmt_z    = dblarr(ngal) - 9d0 
z_mmt_zerr = dblarr(ngal) - 9d0 
z_mmt_xcr  = fltarr(ngal) - 9.
z_mmt_velqual  = strarr(ngal) + 'N'
;      cf_z_mmt_z = dblarr(ngal) - 9d0 
;   cf_z_mmt_zerr = dblarr(ngal) - 9d0 
;  cf_z_mmt_czxcr = dblarr(ngal) - 9d0 

  z_dfilename[indxfile2call] = odfilename[indxfile1call]
   z_filename[indxfile2call] = ofilename[indxfile1call]
      z_mmt_z[indxfile2call] =    ocz[indxfile1call] / c
   z_mmt_zerr[indxfile2call] = oczerr[indxfile1call] / c
z_mmt_velqual[indxfile2call] = ovelqual[indxfile1call]
  z_mmt_xcr[indxfile2call] = oczxcr[indxfile1call]

;      cf_z_mmt_z[indxfile2call] =    cf_ocz[indxfile1call] / c
;   cf_z_mmt_zerr[indxfile2call] = cf_oczerr[indxfile1call] / c
;  cf_z_mmt_czxcr[indxfile2call] = cf_oczxcr[indxfile1call]


ind = where(p_petroMag_r - p_extinction_r lt rcut)

  z_dfilename = z_dfilename[ind]
   z_filename = z_filename[ind]
     z_mmt_z  = z_mmt_z[ind]
  z_mmt_zerr  = z_mmt_zerr[ind]
z_mmt_velqual = z_mmt_velqual[ind]
  z_mmt_xcr = z_mmt_xcr[ind]

;      cf_z_mmt_z = cf_z_mmt_z[ind]
;   cf_z_mmt_zerr = cf_z_mmt_zerr[ind]
;  cf_z_mmt_czxcr = cf_z_mmt_czxcr[ind]

;ind = where(p_objid ne '1237678858477502625') ; PoG
  p_phtype0 = p_phtype0[ind]
  p_objid = p_objid[ind]
  p_ra = p_ra[ind]
  p_dec = p_dec[ind]
  p_petroMag_u = p_petroMag_u[ind]
  p_petroMagerr_u = p_petroMagerr_u[ind]
  p_petroMag_g = p_petroMag_g[ind]
  p_petroMagerr_g = p_petroMagerr_g[ind]
  p_petroMag_r = p_petroMag_r[ind]
  p_petroMagerr_r = p_petroMagerr_r[ind]
  p_petroMag_i = p_petroMag_i[ind]
  p_petroMagerr_i = p_petroMagerr_i[ind]
  p_petroMag_z = p_petroMag_z[ind]
  p_petroMagerr_z = p_petroMagerr_z[ind]
  p_modelMag_u = p_modelMag_u[ind]
  p_modelMagerr_u = p_modelMagerr_u[ind]
  p_modelMag_g = p_modelMag_g[ind]
  p_modelMagerr_g = p_modelMagerr_g[ind]
  p_modelMag_r = p_modelMag_r[ind]
  p_modelMagerr_r = p_modelMagerr_r[ind]
  p_modelMag_i = p_modelMag_i[ind]
  p_modelMagerr_i = p_modelMagerr_i[ind]
  p_modelMag_z = p_modelMag_z[ind]
  p_modelMagerr_z = p_modelMagerr_z[ind]

  p_fiberMag_u = p_fiberMag_u[ind]
  p_fiberMagerr_u = p_fiberMagerr_u[ind]
  p_fiberMag_g = p_fiberMag_g[ind]
  p_fiberMagerr_g = p_fiberMagerr_g[ind]
  p_fiberMag_r = p_fiberMag_r[ind]
  p_fiberMagerr_r = p_fiberMagerr_r[ind]
  p_fiberMag_i = p_fiberMag_i[ind]
  p_fiberMagerr_i = p_fiberMagerr_i[ind]
  p_fiberMag_z = p_fiberMag_z[ind]
  p_fiberMagerr_z = p_fiberMagerr_z[ind]

  p_extinction_u = p_extinction_u[ind]
  p_extinction_g = p_extinction_g[ind]
  p_extinction_r = p_extinction_r[ind]
  p_extinction_i = p_extinction_i[ind]
  p_extinction_z = p_extinction_z[ind]
  p_petroRad_r = p_petroRad_r[ind]
  p_petroRadErr_r = p_petroRadErr_r[ind]
  p_deVRad_i= p_deVRad_i[ind]
  p_deVAB_i= p_deVAB_i[ind]
  p_run = p_run[ind]
  p_rerun = p_rerun[ind]
  p_camCol = p_camCol[ind]
  p_field = p_field[ind]
  p_efac = p_efac[ind]
  p_probpsf = p_probpsf[ind]

ind = where(p_petroRadErr_r lt 0, cnt)
if cnt ge 1 then p_petroRadErr_r[ind] = -9.

hs_stat, p_petroMag_r-p_extinction_r
hs_stat, p_petroMag_r

hs_stat, p_deVRad_i
hs_stat, p_deVAB_i

gcirc, 2, p_ra, p_dec, racen, decen, distg
p_radgal = distg/60.



phot_source = strarr(n_elements(p_objid)) + 'DR9'

ind = where(p_objid eq '1237659326029496400' or $
            p_objid eq '1237659326566237358' or $
            p_objid eq '1237659330315223777' or $
            p_objid eq '1237659326566368623' or $
            p_objid eq '1237659330315224202' or $
            p_objid eq '1237659330315289909' or $
            p_objid eq '1237659330315355256' or $
            p_objid eq '1237659330852225974' or $
            p_objid eq '1237659330315223957' or $
            p_objid eq '1237659330315223611' or $
            p_objid eq '1237659326566237105' or $
            p_objid eq '1237659330315486155' or $
            p_objid eq '1237659330315355266' or $
            p_objid eq '1237659325492430611' or $
            p_objid eq '1237659330315158365' or $
            p_objid eq '1237659330315158743' or $
            p_objid eq '1237659326029563310' or $
            p_objid eq '1237659326029431082' or $
            p_objid eq '1237659326029497054' or $
            p_objid eq '1237659326029169568' or $
            p_objid eq '1237659326029431551' or $
            p_objid eq '1237659326566302977' or $
            p_objid eq '1237659326029431838' or $
            p_objid eq '1237659330852291441' or $
            p_objid eq '1237659326029366619' or $
            p_objid eq '1237659330851964051' or $
            p_objid eq '1237659326566237714' or $
            p_objid eq '1237659330315158619' or $
            p_objid eq '1237659330852095021' or $
            p_objid eq '1237659326029104264' or $
            p_objid eq '1237659326566237110' or $
            p_objid eq '1237659326029430857' or $
            p_objid eq '1237659330852159878' or $
            p_objid eq '1237659326566301886', cnt)
if cnt ge 1 then begin
 p_petroMag_u[ind] = p_modelMag_u[ind]
 p_petroMag_g[ind] = p_modelMag_g[ind]
 p_petroMag_r[ind] = p_modelMag_r[ind]
 p_petroMag_i[ind] = p_modelMag_i[ind]
 p_petroMag_z[ind] = p_modelMag_z[ind]

 p_petroMagerr_u[ind] = p_modelMagerr_u[ind]
 p_petroMagerr_g[ind] = p_modelMagerr_g[ind]
 p_petroMagerr_r[ind] = p_modelMagerr_r[ind]
 p_petroMagerr_i[ind] = p_modelMagerr_i[ind]
 p_petroMagerr_z[ind] = p_modelMagerr_z[ind]
endif


ind = where(p_objid eq '1237659326029234779' or $
            p_objid eq '1237659326029497448' or $ 
            p_objid eq '1237659326029366842' or $
            p_objid eq '1237659326029562522' or $
            p_objid eq '1237659326029168745' or $
            p_objid eq '1237659330315486330' or $
            p_objid eq '1237659326029170123' or $
            p_objid eq '1237659326566303189' or $
            p_objid eq '1237659330852225089' or $
            p_objid eq '1237655373036519580' or $
            p_objid eq '1237659326029497648' or $
            p_objid eq '1237659326029365322' or $
            p_objid eq '1237655471820833889' or $
            p_objid eq '1237659326029365776' or $
            p_objid eq '1237659326029430811' or $
            p_objid eq '1237655471820703123' or $
            p_objid eq '1237659330315158899' or $
            p_objid eq '1237659326029366843' or $
            p_objid eq '1237659326029234789' or $
            p_objid eq '1237659330852028516' or $
            p_objid eq '1237655471821030647' or $
            p_objid eq '1237655471820964932' or $
            p_objid eq '1237659326566171518' or $
            p_objid eq '1237659330852291187' or $
            p_objid eq '1237659326029300982' or $
            p_objid eq '1237659326029366649' or $
            p_objid eq '1237659326029301207' or $
            p_objid eq '1237659326029365340' or $
            p_objid eq '1237655471820702829' or $
            p_objid eq '1237659326566041178' or $
            p_objid eq '1237659326029366522' or $
            p_objid eq '1237659326029169535' or $
            p_objid eq '1237659330852029383' or $
            p_objid eq '1237659326029234787' or $
            p_objid eq '1237655471820768763' or $
            p_objid eq '1237659330852095186' or $
            p_objid eq '1237659330315224382' or $
            p_objid eq '1237659330315224308' or $
            p_objid eq '1237659326029301231' or $
            p_objid eq '1237659325492495519', cnt)
if cnt ge 1 then begin
 p_petroMag_u[ind] = p_fiberMag_u[ind]
 p_petroMag_g[ind] = p_fiberMag_g[ind]
 p_petroMag_r[ind] = p_fiberMag_r[ind]
 p_petroMag_i[ind] = p_fiberMag_i[ind]
 p_petroMag_z[ind] = p_fiberMag_z[ind]

 p_petroMagerr_u[ind] = p_fiberMagerr_u[ind]
 p_petroMagerr_g[ind] = p_fiberMagerr_g[ind]
 p_petroMagerr_r[ind] = p_fiberMagerr_r[ind]
 p_petroMagerr_i[ind] = p_fiberMagerr_i[ind]
 p_petroMagerr_z[ind] = p_fiberMagerr_z[ind]

 p_modelMag_u[ind] = p_fiberMag_u[ind]
 p_modelMag_g[ind] = p_fiberMag_g[ind]
 p_modelMag_r[ind] = p_fiberMag_r[ind]
 p_modelMag_i[ind] = p_fiberMag_i[ind]
 p_modelMag_z[ind] = p_fiberMag_z[ind]

 p_modelMagerr_u[ind] = p_fiberMagerr_u[ind]
 p_modelMagerr_g[ind] = p_fiberMagerr_g[ind]
 p_modelMagerr_r[ind] = p_fiberMagerr_r[ind]
 p_modelMagerr_i[ind] = p_fiberMagerr_i[ind]
 p_modelMagerr_z[ind] = p_fiberMagerr_z[ind]
endif

;goto, jump1
dr9l = ['1237659325492494473', $
        '1237659162815103001', $
        '1237655472360325176', $
        '1237662499470049385', $
        '1237655473433084004', $
        '1237659326029365777', $
        '1237659330315288879', $
        '1237659325492429421', $
        '1237659330852094076', $
        '1237659326029430896', $
        '1237659326029365434', $
        '1237659326029365780', $
        '1237655473433083999']
dr7l = ['587733604267589957', $
        '587733441590198292', $
        '587729751135420466', $
        '588018253221855461', $
        '587729752208179285', $
        '587733604804461078', $
        '587733609090384559', $
        '587733604267524497', $
        '587733609627189900', $
        '587733604804526198', $
        '587733604804460733', $
        '587733604804461080', $
        '587729752208179308']
for k = 0, n_elements(dr9l)- 1 do begin
  ind  = where(  p_objid eq dr9l[k], cnt9)
  ind7 = where(dr7_objid eq dr7l[k], cnt7)
  if cnt9 le 0 or cnt7 le 0 then stop

;  print, k, cnt9, cnt7
  p_petroMag_u[ind] =    dr7_petroMag_u[ind7]
  p_petroMag_g[ind] =    dr7_petroMag_g[ind7]
  p_petroMag_r[ind] =    dr7_petroMag_r[ind7]
  p_petroMag_i[ind] =    dr7_petroMag_i[ind7]
  p_petroMag_z[ind] =    dr7_petroMag_z[ind7]
  p_petroMagerr_u[ind] = dr7_petroMagerr_u[ind7]
  p_petroMagerr_g[ind] = dr7_petroMagerr_g[ind7]
  p_petroMagerr_r[ind] = dr7_petroMagerr_r[ind7]
  p_petroMagerr_i[ind] = dr7_petroMagerr_i[ind7]
  p_petroMagerr_z[ind] = dr7_petroMagerr_z[ind7]

  phot_source[ind] = 'DR7'
endfor

dr9l = ['1237659330852421695', $
  '1237659330315223132', $
  '1237659330315288582', $
  '1237659326029365403', $
  '1237659326029365336', $
  '1237659330852159727', $
  '1237659330315485209', $
  '1237655471820701869', $
 '1237659326566301869']
dr7l = ['587733609627516989', $
 '587733609090318481', $
 '587733609090383876', $
 '587733604804460696', $
 '587733604804460628', $
 '587733609627255012', $
 '587733609090580507', $
 '587733609627189424', $
 '587733605341397148']
for k = 0, n_elements(dr9l)- 1 do begin
  ind  = where(  p_objid eq dr9l[k], cnt9)
  ind7 = where(dr7_objid eq dr7l[k], cnt7)

;  print, k, cnt9, cnt7
  p_petroMag_u[ind] =    dr7_petroMag_u[ind7]
  p_petroMag_g[ind] =    dr7_petroMag_g[ind7]
  p_petroMag_r[ind] =    dr7_petroMag_r[ind7]
  p_petroMag_i[ind] =    dr7_petroMag_i[ind7]
  p_petroMag_z[ind] =    dr7_petroMag_z[ind7]
  p_petroMagerr_u[ind] = dr7_petroMagerr_u[ind7]
  p_petroMagerr_g[ind] = dr7_petroMagerr_g[ind7]
  p_petroMagerr_r[ind] = dr7_petroMagerr_r[ind7]
  p_petroMagerr_i[ind] = dr7_petroMagerr_i[ind7]
  p_petroMagerr_z[ind] = dr7_petroMagerr_z[ind7]

  p_modelMag_u[ind] =    dr7_modelMag_u[ind7]
  p_modelMag_g[ind] =    dr7_modelMag_g[ind7]
  p_modelMag_r[ind] =    dr7_modelMag_r[ind7]
  p_modelMag_i[ind] =    dr7_modelMag_i[ind7]
  p_modelMag_z[ind] =    dr7_modelMag_z[ind7]
  p_modelMagerr_u[ind] = dr7_modelMagerr_u[ind7]
  p_modelMagerr_g[ind] = dr7_modelMagerr_g[ind7]
  p_modelMagerr_r[ind] = dr7_modelMagerr_r[ind7]
  p_modelMagerr_i[ind] = dr7_modelMagerr_i[ind7]
  p_modelMagerr_z[ind] = dr7_modelMagerr_z[ind7]

  phot_source[ind] = 'DR7'
endfor
jump1:

readcol, dircl + 'dr7phot.txt', lobjid, pmag, f = 'a,f'
hs_nmatch, p_objid, lobjid, suba, subb, nsuba, nsubb
     help, p_objid, lobjid, suba, subb, nsuba, nsubb
p_petroMag_r[suba] = pmag[subb]
 phot_source[suba] = 'DR7'

; below - i didn't update the phot 
readcol, dircl + 'badphot.txt', idbad, f = 'a'
hs_nmatch, p_objid, idbad, suba, subb, nsuba, nsubb
     help, p_objid, idbad, suba, subb, nsuba, nsubb
phot_source[suba] = 'WRONG'


ind = where(p_objid eq '1237659330315224137') & help, ind
if cnt ge 1 then print, p_petroMag_r[ind] 
ind = where(p_objid eq '1237659326566171879') & help, ind
if cnt ge 1 then print, p_petroMag_r[ind] 


;stop
;z_mmt_tfilename = dird0 + z_dfilename + '/' + z_filename
;z_mmt_tfilename = dird11 + z_filename
z_mmt_tfilename = strarr(n_elements(p_objid)) + 'NN'
ind = where(z_dfilename eq 'skysub_a2199new_1', cnt) & help, ind
if cnt ge 1 then z_mmt_tfilename[ind] = dird11 + z_filename[ind]
ind = where(z_dfilename eq 'skysub_a2199b_1', cnt) & help, ind
if cnt ge 1 then z_mmt_tfilename[ind] = dird12 + z_filename[ind]
ind = where(z_dfilename eq 'skysub_a2199a_1', cnt) & help, ind
if cnt ge 1 then z_mmt_tfilename[ind] = dird2 + z_filename[ind]
ind = where(z_dfilename eq 'skysub_a2199a_2', cnt) & help, ind
if cnt ge 1 then z_mmt_tfilename[ind] = dird3 + z_filename[ind]
ind = where(z_dfilename eq 'skysub_a2199b15_1', cnt) & help, ind
if cnt ge 1 then z_mmt_tfilename[ind] = dird4 + z_filename[ind]
ind = where(z_dfilename eq 'skysub_a2199b15_2', cnt) & help, ind
if cnt ge 1 then z_mmt_tfilename[ind] = dird5 + z_filename[ind]
ind = where(z_dfilename eq 'skysub_a2199a19_2', cnt) & help, ind
if cnt ge 1 then z_mmt_tfilename[ind] = dird6 + z_filename[ind]
ind = where(z_dfilename eq 'skysub_a2199a19_3', cnt) & help, ind
if cnt ge 1 then z_mmt_tfilename[ind] = dird7 + z_filename[ind]
ind = where(z_dfilename eq 'skysub_a2199a19_1', cnt) & help, ind
if cnt ge 1 then z_mmt_tfilename[ind] = dird8 + z_filename[ind]
ind = where(z_dfilename eq 'skysub_a2199a19_4', cnt) & help, ind
if cnt ge 1 then z_mmt_tfilename[ind] = dird9 + z_filename[ind]

ind = where(z_dfilename eq 'skysub_a2199a_1' or $
            z_dfilename eq 'skysub_a2199a_2' or $
            z_dfilename eq 'skysub_a2199b15_1' or $
            z_dfilename eq 'skysub_a2199b15_2' or $
            z_dfilename eq 'skysub_a2199a19_2', cnt) 
hs_nmatch, tmp_ofilename, z_filename[ind], suba, subb, nsuba, nsubb
     help, tmp_ofilename, z_filename[ind], suba, subb, nsuba, nsubb

ind = where(p_objid eq '1237659330852225683', cnt)
ind = where(p_objid eq '1237659330315289347', cnt)
ind = where(p_objid eq '1237655471820833457', cnt)
ind = where(p_objid eq '1237655471820833502', cnt)
ind = where(p_objid eq '1237659330315289504', cnt)
ind = where(p_objid eq '1237659330315354729', cnt)
ind = where(p_objid eq '1237659330315420341', cnt)
if cnt ge 1 then print, z_mmt_z[ind], z_mmt_tfilename[ind]

;print, p_probpsf[ind]
;p_probpsf[ind] = 1
;print, p_probpsf[ind]
save, FILENAME = dircl + 'z_' + file + 'sav', /compress, $
  phot_source, p_phtype0, p_radgal, $
  p_objid, p_ra, p_dec, $
  p_petroMag_u,p_petroMagerr_u,p_petroMag_g,p_petroMagerr_g,p_petroMag_r,p_petroMagerr_r,$
  p_petroMag_i,p_petroMagerr_i,p_petroMag_z,p_petroMagerr_z,$
  p_modelMag_u,p_modelMagerr_u,p_modelMag_g,p_modelMagerr_g,p_modelMag_r,p_modelMagerr_r, $
  p_modelMag_i,p_modelMagerr_i,p_modelMag_z,p_modelMagerr_z,$
  p_fiberMag_u,p_fiberMagerr_u,p_fiberMag_g,p_fiberMagerr_g,p_fiberMag_r,p_fiberMagerr_r, $
  p_fiberMag_i,p_fiberMagerr_i,p_fiberMag_z,p_fiberMagerr_z,$
  p_extinction_u,p_extinction_g,p_extinction_r,p_extinction_i,p_extinction_z,$
  p_petroRad_r,p_petroRadErr_r, $
  p_deVRad_i, p_deVAB_i, $
  p_run,p_rerun,p_camCol,p_field,p_efac, p_probpsf, $
;  cf_z_mmt_z, cf_z_mmt_zerr, cf_z_mmt_czxcr, $
  z_mmt_xcr, $
  z_mmt_tfilename, z_dfilename, z_filename, z_mmt_z, z_mmt_zerr, z_mmt_velqual


;endif

;CD, cdd

END
