PRO nedmatch

ver = '12'

C = 2.99792458d5    ; km/s.
omegam=0.3
omegal=0.7
omegak=0.
H0    = 100. ; km/s/Mpc
phy1kpc = 1.

dircl= '/Users/hhwang/Research/Work/LIRGs/clcat/'
dirg = '/Users/hhwang/Research/Work/LIRGs/galcat/'
dir  = '/Users/hhwang/Research/Work/WISEcfa/IndivCluster/A2199/'
dirc = dir + 'z_DATA/'

radcut = 400.
racen  = 247.15933d
decen  =  39.55127d
;zcl = 9370./c
zcl = 0.031255d

degMpc = zang(phy1kpc*1d3, zcl, $
   h0=H0, k = omegak, Lambda0 = omegal, Omega_m = omegam)/3600. ; deg/Mpc


;Rines 02
readcol, dirc + 'R02datafile3.txt', rah, ram, ras, ded, dem, des, r02_cz, r02_cze, r02_ref, $
 f = 'i,i,f, i,i,f, i,i,i', skipline = 32
r02_ra = 15d * (rah + ram/60. + ras/3600.)
r02_de =  1d * (ded + dem/60. + des/3600.)
r02_id = string(indgen(n_elements(rah)) + 1, f = '(i4)')
gcirc, 2, 247.16067, 39.08333, r02_ra, r02_de, distg
ind = sort(distg)
print, distg[ind[0:2]]
 r02_ra[ind[0]] = 247.160998861d
 r02_de[ind[0]] =  39.087676836d


;file  = 'MLNa2199phot21_26DR9_hshwang.sav'
file  = 'a2199phot21_5DR9_hshwang.sav'
filew = 'nz_' + file

; Data from NED
mynum = 5000000l & mysk=0
;filefsc = 'nedz20131126.txt'
filefsc = 'nedz20190109.txt'
readfmt, dirc +filefsc, $
 '(3x, a33, i2,1x,i2,1x,f4.1, 2x,a1,i2,1x,i2,1x,i2, 2x, a6, 7x, d10.6, a5)', $
 gid1, rah1, ram1, ras1, design1, ded1, dem1, des1, type1, z1, qual1, $
 skipl = 17, numl = 999
readfmt, dirc +filefsc, $
 '(4x, a33, i2,1x,i2,1x,f4.1, 2x,a1,i2,1x,i2,1x,i2, 2x, a6, 7x, d10.6, a5)', $
 gid2, rah2, ram2, ras2, design2, ded2, dem2, des2, type2, z2, qual2, $
 skipl = 1016, numl = 9000l
readfmt, dirc +filefsc, $
 '(5x, a33, i2,1x,i2,1x,f4.1, 2x,a1,i2,1x,i2,1x,i2, 2x, a6, 7x, d10.6, a5)', $
 gid3, rah3, ram3, ras3, design3, ded3, dem3, des3, type3, z3, qual3, $
 skipl = 10016l;, numl = 9000l

gid = [gid1, gid2, gid3]
rah = [rah1, rah2, rah3]
ram = [ram1, ram2, ram3]
ras = [ras1, ras2, ras3]
design = [design1, design2, design3]
ded = [ded1, ded2, ded3]
dem = [dem1, dem2, dem3]
des = [des1, des2, des3]
type = [type1, type2, type3]
z = [z1, z2, z3]
qual = [qual1, qual2, qual3]


zerrned = z * 0. - 9.

;readfmt, dirc +filefsc, $
;  '(3x, a33, i2,1x,i2,1x,f4.1, 2x,a1,i2,1x,i2,1x,i2, 2x, a6, 7x, d10.6, a5)', $
;  gid, rah, ram, ras, design, ded, dem, des, type, z, qual, skipl = 21

print, rah[0:3]
print, ram[0:3]
print, ras[0:3]
print, ded[0:3]
print, dem[0:3]
print, des[0:3]
rafsc = 15d * (rah + ram/60. + ras/3600.)
defsc =  1d * (ded + dem/60. + des/3600.)
tmp = where(design eq '-', cnt)
if cnt ge 1 then defsc[tmp] =  -defsc[tmp]

ind = where((strcompress(type, /remove) eq 'G'    or $
  strcompress(type, /remove) eq 'QSO') and $
  strcompress(gid, /remov) ne '2MASSJ16282856+3909083' and $ ;Wrong redshift in NED because of wrong match
  strcompress(gid, /remov) ne 'SDSSJ162719.46+391934.0' and $ ;Wrong redshift in NED because of wrong z in BOSS
  strcompress(gid, /remov) ne 'SDSSJ163111.05+391104.3' and $ ;Wrong redshift in NED because of wrong z in BOSS
  strcompress(gid, /remov) ne 'SDSSJ162622.93+384445.5' and $ ;Wrong redshift in NED because of wrong z in BOSS
  strcompress(gid, /remov) ne 'SDSSJ162446.62+400821.9' and $ ;Wrong redshift in NED because of wrong z in BOSS
  strcompress(gid, /remov) ne 'SDSSJ162328.37+393322.1' and $ ;Wrong redshift in NED because of wrong z in BOSS
  strcompress(gid, /remov) ne 'SDSSJ163359.77+394608.5' and $ ;Wrong redshift in NED because of wrong z in BOSS
  strcompress(gid, /remov) ne 'SDSSJ163350.55+392225.7' and $ ;Wrong redshift in NED because of wrong z in BOSS
 (strcompress(qual, /remove) eq '' or $
  strcompress(qual, /remove) eq 'SPEC'), cnt)

;ind = where((strcompress(type, /remove) eq 'G'    or $
;	     strcompress(type, /remove) eq 'QSO') and $
;             strcompress(gid, /remov) ne 'SDSSJ162828.55+390908.3' and $ ;Wrong redshift in NED because of wrong match

;             strcompress(gid, /remov) ne 'SDSSJ155744.61+270119.0' and $ ;Wrong redshift in NED because of wrong match
;	     strcompress(qual, /remove) eq '', cnt)

;ind = where(strcompress(type, /remove) ne 'GClstr' and $
;            strcompress(type, /remove) ne 'GGroup' and $
;            strcompress(type, /remove) ne 'GPair' and $
;            strcompress(qual, /remove) eq '', cnt)
gid   = gid[ind]
rafsc = rafsc[ind]
defsc = defsc[ind]
type  = type[ind]
z     = z[ind]
zerrned = zerrned[ind]
qual  = qual[ind]

ind = where(strcompress(gid, /remov) eq '2MASXJ16525968+4021449', cnt)
if cnt ge 1 then begin
  rafsc[ind] = 253.24664d
  defsc[ind] =  40.35942d
endif
ind = where(strcompress(gid, /remov) eq '2MASXJ16322040+4023344', cnt)
if cnt ge 1 then begin
  rafsc[ind] = 248.085549d
  defsc[ind] =  40.393074d
endif
ind = where(strcompress(gid, /remov) eq 'SHOC544', cnt)
if cnt ge 1 then begin
rafsc[ind] = 249.725460d
defsc[ind] =  42.192138d
endif
ind = where(strcompress(gid, /remov) eq 'SHOC542', cnt)
if cnt ge 1 then begin
rafsc[ind] = 249.186605d
defsc[ind] =  43.125544d
endif


cnt = 3
for i = 0, cnt-1 do $
  print, strcompress(gid[i], /remove),  rafsc[i], defsc[i],  z[i], $
    i + 1, $
    f = '(a20, 2d11.6, d8.4, i4)'

;For some point sources left in Rines+13
; Table 2
filer  = 'apj464013t2_mrted.txt'
readfmt, dircl + filer, $
  '(i2,i3,f7.3, 1x, a1,i2,i3,f7.3, i7, i4, 7x, A1,i2)', $
  rah, ram, ras, design, ded, dem, des, $
  czgal, eczgal, qual, mem, skiplin = 30
r13_ra  = 15d * (rah + ram/60. + ras/3600.)
r13_dec =  1d * (ded + dem/60. + des/3600.)
ind = where(design eq '-', cnt)
if cnt ge 1 then r13_dec[ind] = -r13_dec[ind]
r13_id   = strcompress(string(rah) + '_' + string(ram) + '_' +string(ras), /remove)

smem = strarr(n_elements(r13_ra)) + 'N'
ind  = where(mem eq 1, cnt)
if cnt ge 1 then smem[ind] = 'Y'

gcirc, 2, racen, decen, r13_ra, r13_dec, distg
indr13 = where(qual eq 'Q' and distg le radcut * 60., cntr13) & help, indr13
if cntr13 ge 1 then begin
 r13_id   =  r13_id[indr13]
 r13_ra   =  r13_ra[indr13]
 r13_dec  = r13_dec[indr13]
 r13_mem  =    smem[indr13]
 r13_z    =   czgal[indr13] / c
 r13_zerr =  eczgal[indr13] / c
endif



restore, dirg +  'Mgaldr' + ver + '_stars.sav'
indm = where(ss3_survey eq 'MMT_A2199', cntm)
ind = where(ss3_survey eq 'boss' or $
 ss3_survey eq 'sdss' or $
 ss3_survey eq 'segue1' or $
 ss3_survey eq 'segue2', cnt, compl = nind)
if cnt ge 1 then begin
 ss3_survey[ind]  = 'SDSS'
 ss3_survey[nind] = 'SDSS_NED'
endif
;if cntm ge 1 then ss3_survey[indm] = 'MMT_A2199' ; REMOVE LATER

restore, dirg + 'Mgaldr' + ver + '_flags.sav'
print, s3_survey(uniq(s3_survey, sort(s3_survey)))
indm = where(s3_survey eq 'MMT_A2199', cntm)
ind = where(s3_survey eq 'boss' or $
 s3_survey eq 'sdss' or $
 s3_survey eq 'segue1' or $
 s3_survey eq 'segue2', cnt, compl = nind)
if cnt ge 1 then begin
 s3_survey[ind]  = 'SDSS'
 s3_survey[nind] = 'SDSS_NED'
endif
;if cntm ge 1 then s3_survey[indm] = 'MMT_A2199' ; REMOVE LATER


help, s3_survey
restore, dirg + 'Mgaldr' + ver + '_cluster.sav'
restore, dirg + 'Mgaldr' + ver + '_id.sav'
restore, dirg + 'Mgaldr' + ver + '_mpa.sav'
restore, dirg + 'Mgaldr' + ver + '_spec.sav'

; Stellar Masses
;readcol, dirc + 'Formass20140414_MLNa426phot22DR9_hshwang.txt', $
;  oj_objid, f = 'x,x,x,a', skipline = 1
;readcol, dirc + 'output_lephare_MLNa426.txt', $
;  ojid, oinf_jmass, ojmass, osup_jmass, f = 'a,d,d,d', skipline = 51

restore, dirc + 'z_' + file



ind = where(s3_objid eq '1237659326029365297', cnt) & help, ind
if cnt ge 1 then $
  s3_zerr[ind]= 0.000143d

;ind = where(s3_objid eq '1237655373036585119')
;s3_z[ind]= 0.028143d
;s3_zerr[ind]= 0.000087d

;ind = where(s3_objid eq '1237659324955492627')
; s3_z[ind]= 0.030071d
;s3_zerr[ind]= 0.000073d

;ind = where(s3_objid eq '1237655472357310527')
;s3_z[ind]= 0.02846d
;s3_zerr[ind]= 0.000093d

;ind = where(s3_objid eq '1237659324955951172')
;s3_z[ind]= 0.033453d
;s3_zerr[ind]= 0.00024d

;ind = where(s3_objid eq '1237665569296613766')
;s3_z[ind]= 0.03353152d
;s3_zerr[ind]= 1.184405d-5
;s3_phtype[ind]= 2


v_dispersion = p_ra * 0. - 9.
v_disp_err   = p_ra * 0. - 9.
v_SN         = p_ra * 0. - 9.
v_chisq      = p_ra * 0. - 9.

inf_jmass = z_mmt_z * 0. - 9.
    jmass = z_mmt_z * 0. - 9.
sup_jmass = z_mmt_z * 0. - 9.
;match, p_objid, oj_objid, suba, subb
; help, p_objid, oj_objid, suba, subb
;inf_jmass[suba] = oinf_jmass[subb]
;    jmass[suba] =     ojmass[subb]
;sup_jmass[suba] = osup_jmass[subb]


;tmp=where(s3_objid eq '1237662226235392009', cnt) ; change redshift
;if cnt ge 1 then begin
;    s3_z[tmp[0]]= -0.00059832393d  ; Star From APOGEE in SDSS explorer
; s3_zerr[tmp[0]]=  0.00001d
;endif

;s3_objid  = [s3_objid, ss3_objid]
;s3_z      = [s3_z,     ss3_z]
;s3_zerr   = [s3_zerr,  ss3_zerr]
;s3_phtype = [s3_phtype, intarr(n_elements(ss3_objid)) + 3]


toto = where(s3_zWarning eq 0 and $
;  s3_survey ne 'MMT_A2199' and $ ;CHANGE LATER
  s3_objid ne '1237659330314895992') ; wrong redshift
;toto = where(s3_objid ne 'q')
help, s3_zWarning, toto

;tmp = where(s3_objid[toto] eq '1237659330852225683') & help, tmp
;print, s3_survey[toto[tmp]]

match, p_objid, s3_objid[toto], suba, subb0
subb = toto[subb0]
help, suba

ngal = n_elements(p_ra)
z_sdss_z = dblarr(ngal) - 9.
z_tot_z  = dblarr(ngal) - 9.
z_sdss_zerr = dblarr(ngal) - 9.
z_tot_zerr  = dblarr(ngal) - 9.

z_sdss_vdisp_cas    = fltarr(ngal) - 9.
z_sdss_errvdisp_cas = fltarr(ngal) - 9.
z_sdss_vdisp_wis    = fltarr(ngal) - 9.
z_sdss_errvdisp_wis = fltarr(ngal) - 9.
z_sdss_vdisp_mpa    = fltarr(ngal) - 9.
z_sdss_errvdisp_mpa = fltarr(ngal) - 9.
z_sdss_vdisp_pm     = fltarr(ngal) - 9.
z_sdss_errvdisp_pm  = fltarr(ngal) - 9.

z_plate   = strarr(ngal) + '000'
z_mjd     = strarr(ngal) + '00000'
z_fiberID = strarr(ngal) + '000'
z_specobjid = strarr(ngal) + 'N'
z_dr7specobjid = strarr(ngal) + 'N'

z_specclass = strarr(ngal) + 'N'
z_subclass  = strarr(ngal) + 'N'

memflag     = strarr(ngal) + 'N' 
p_phtype    = intarr(ngal) + 9

;-----------------------
;Matching Catalogs
;-----------------------
tolerance= 1.5
hs_radecmatch,tolerance, rafsc, defsc, p_ra, p_dec, $
  indxfile1call,indxfile2call,nonindxfile1call,nonindxfile2call, $
  dra12,ddec12,dist12,pa12,kindx12,matchednum12
par = 'ned'
hs_match, dra12, ddec12, tolerance, gid, p_objid, $
  indxfile1call, indxfile2call, kindx12, dist12, $
  dir = dir, par = par

print,  gid[nonindxfile1call[0:5]]
ind = where(dist12 gt tolerance * 0.9, cnt)
cnt = 10
if cnt ge 1 then $
for i = 0, cnt-1 do $
  print, p_objid[indxfile2call[ind[i]]], $
    p_ra[indxfile2call[ind[i]]], p_dec[indxfile2call[ind[i]]], $
    z_mmt_z[indxfile2call[ind[i]]], z[indxfile1call[ind[i]]], $
    gid[indxfile1call[ind[i]]], $
    i + 1, $
    f = '(a20, 2d11.6, 2d8.4, a33, i3)'

z_ned_id = strarr(ngal) + 'NN'
z_ned_z  = dblarr(ngal) - 9.
z_source = strarr(ngal) + 'U'

z_ned_id[indxfile2call] = strcompress(gid[indxfile1call], /remove)
 z_ned_z[indxfile2call] = z[indxfile1call]
 z_tot_z[indxfile2call] = z[indxfile1call]
z_tot_zerr[indxfile2call] = zerrned[indxfile1call]
  z_source[indxfile2call] = 'NED'

ind = where(z_source eq 'NED') & help, ind


;R02
tolerance= 15.
hs_radecmatch,tolerance, r02_ra, r02_de, p_ra, p_dec, $
  indxfile1call,indxfile2call,nonindxfile1call,nonindxfile2call, $
  dra12,ddec12,dist12,pa12,kindx12,matchednum12
par = 'r02'
hs_match, dra12, ddec12, tolerance, r02_id, p_objid, $
  indxfile1call, indxfile2call, kindx12, dist12, $
  dir = dir, par = par

;ind = where(z_source[indxfile2call] eq 'NED' or $
;            z_source[indxfile2call] eq 'SDSS', cnt)
print, ' '
;for i = 0, cnt - 1 do begin
;  print, r02_id[indxfile1call[i]], $
;    r02_ra[indxfile1call[i]], r02_de[indxfile1call[i]], $
;    r02_cz[indxfile1call[i]]/c, $
;    i + 1, $
;    f = '(a20, 2d11.6, f7.3, i3)'
;endfor
for i = 0, n_elements(nonindxfile1call) - 1 do begin
  print, r02_id[nonindxfile1call[i]], $
    r02_ra[nonindxfile1call[i]], r02_de[nonindxfile1call[i]], $
    r02_cz[nonindxfile1call[i]]/c, $
    i + 1, $
    f = '(a20, 2d11.6, f7.3, i3)'
endfor

   z_tot_z[indxfile2call] =  r02_cz[indxfile1call] / c
z_tot_zerr[indxfile2call] = r02_cze[indxfile1call] / c
  z_source[indxfile2call] = 'R02' ; http://adsabs.harvard.edu/cgi-bin/bib_query?2002AJ....124.1266R
;toto = where(z_source[indxfile2call] eq 'NED', cnt)
;if cnt ge 1 then z_source[indxfile2call[toto]] = 'R02' ; http://adsabs.harvard.edu/cgi-bin/bib_query?2002AJ....124.1266R


; Rines+13
z_r13_id = strarr(ngal) + 'NN'
z_r13_z  = dblarr(ngal) - 9.

if cntr13 ge 1 then begin
tolerance= 1.
hs_radecmatch,tolerance, r13_ra, r13_dec, p_ra, p_dec, $
  indxfile1call,indxfile2call,nonindxfile1call,nonindxfile2call, $
  dra12,ddec12,dist12,pa12,kindx12,matchednum12
par = 'r13'
hs_match, dra12, ddec12, tolerance, r13_id, p_objid, $
  indxfile1call, indxfile2call, kindx12, dist12, $
  dir = dir, par = par

if matchednum12 lt n_elements(r13_ra) then $
print,  r13_id[nonindxfile1call]

ind = where(dist12 gt tolerance * 0.9, cnt)
if cnt ge 1 then begin
cnt = cnt<10
for i = 0, cnt-1 do $
  print, p_objid[indxfile2call[ind[i]]], $
    p_ra[indxfile2call[ind[i]]], p_dec[indxfile2call[ind[i]]], $
    z_mmt_z[indxfile2call[ind[i]]], r13_z[indxfile1call[ind[i]]], $
    r13_id[indxfile1call[ind[i]]], $
    i + 1, $
    f = '(a20, 2d13.6, 2d8.4, a13, i3)'
endif

  z_r13_id[indxfile2call] = strcompress(r13_id[indxfile1call], /remove)
   z_r13_z[indxfile2call] = r13_z[indxfile1call]
   z_mmt_z[indxfile2call] = r13_z[indxfile1call]
   z_tot_z[indxfile2call] = r13_z[indxfile1call]
z_tot_zerr[indxfile2call] = r13_zerr[indxfile1call]
z_mmt_zerr[indxfile2call] = r13_zerr[indxfile1call]
;  z_source[indxfile2call] = 'MMT'
  z_source[indxfile2call] = 'MMT_R13'
;   memflag[indxfile2call] =  r13_mem[indxfile1call]

indr13 = where(z_source eq 'MMT_R13') & help, indr13
endif


;For Star catalog
;toto = where(ss3_zWarning eq 0) & help, ss3_zWarning, toto
toto = where(ss3_zWarning eq 0 and $
;  ss3_survey ne 'MMT_A2199' and $  ;CHANGE LATER
  ss3_objid ne '1237659330314895992') ; wrong redshift
match, p_objid, ss3_objid[toto], ssuba, ssubb0
 help, p_objid, ss3_objid[toto], ssuba, ssubb0
 ssubb = toto[ssubb0]

   p_phtype[ssuba] = 3
   z_sdss_z[ssuba] =    ss3_z[ssubb]
z_sdss_zerr[ssuba] = ss3_zerr[ssubb]
    z_tot_z[ssuba] =    ss3_z[ssubb]
 z_tot_zerr[ssuba] = ss3_zerr[ssubb]
   z_source[ssuba] = ss3_survey[ssubb]
;z_sourceType[ssuba] = ss3_sourceType[ssubb]
    z_plate[ssuba] =     ss3_plate[ssubb]
      z_mjd[ssuba] =       ss3_mjd[ssubb]
  z_fiberID[ssuba] =   ss3_fiberID[ssubb]
z_specobjid[ssuba] = ss3_specobjid[ssubb]

;SDSS
z_specclass[suba]   = s3_specclass[subb]
z_subclass[suba]    = s3_subclass[subb]
z_sdss_vdisp_cas[suba]    = s3_vdisp_cas[subb]
z_sdss_errvdisp_cas[suba] = s3_errvdisp_cas[subb]
z_sdss_vdisp_wis[suba]    = vdispmem_wis[subb]
z_sdss_errvdisp_wis[suba] = vdispmem_err_wis[subb]
z_sdss_vdisp_mpa[suba]    = vdispmem[subb]
z_sdss_errvdisp_mpa[suba] = vdispmem_err[subb]
z_sdss_vdisp_pm[suba]     = vdispmem_pm[subb]
z_sdss_errvdisp_pm[suba]  = vdispmem_err_pm[subb]

z_plate[suba] =   s3_plate[subb]
z_mjd[suba] =     s3_mjd[subb]
z_fiberID[suba] = s3_fiberID[subb]
z_specobjid[suba] = s3_specobjid[subb]
z_dr7specobjid[suba] = s3_dr7specobjid[subb]

z_sdss_z[suba]    = s3_z[subb]
z_sdss_zerr[suba] = s3_zerr[subb]

  p_phtype[suba] = s3_phtype[subb]
   z_tot_z[suba] =      s3_z[subb]
z_tot_zerr[suba] =   s3_zerr[subb]
;   z_source[suba] = s3_survey[subb]
;tmp = where(hecs_zsource eq 'MMT', ctmp)
;if ctmp ge 1 then hecs_zsource[tmp] = 'MMT_R13'
;z_source[suba] = hecs_zsource[subb]
tmp = where(cl_zsource eq 'MMT', ctmp)
if ctmp ge 1 then s3_survey[tmp] = 'MMT_R13'
z_source[suba] = s3_survey[subb]
;if ctmp ge 1 then cl_zsource[tmp] = 'MMT_R13'
;z_source[suba] = cl_zsource[subb]

; z_source[suba] = 'SDSS'
ind = where(z_source eq 'SDSS') & help, ind

ind0 = where(z_source[suba] eq 'N') & help, ind0

;print, p_objid[suba[ind0[0:5]]]
;stop
;ind = where(z_source eq 'MMT', cnt) & help, ind
;if cnt ge 1 then begin
;   z_mmt_z[ind]    = z_tot_z[ind]
;z_mmt_zerr[ind] = z_tot_zerr[ind]
;print, 'DONE'
;endif
;help, ind



ind = where(z_dfilename eq 'skysub_a2199a_1' or $
            z_dfilename eq 'skysub_a2199a_2' or $
            z_dfilename eq 'skysub_a2199b15_1' or $
            z_dfilename eq 'skysub_a2199b15_2' or $
            z_dfilename eq 'skysub_a2199a19_1' or $
            z_dfilename eq 'skysub_a2199a19_2' or $
            z_dfilename eq 'skysub_a2199a19_3' or $
            z_dfilename eq 'skysub_a2199a19_4', cnt) 
;ind = where(z_mmt_z gt -8, cnt)
if cnt ge 1 then begin
   z_tot_z[ind]    = z_mmt_z[ind]
z_tot_zerr[ind] = z_mmt_zerr[ind]
  z_source[ind]   = 'MMT'
endif
help, ind

ind = where(z_dfilename eq 'skysub_a2199new_1' or $
            z_dfilename eq 'skysub_a2199b_1', cnt) 
if cnt ge 1 then begin
   z_tot_z[ind]    = z_mmt_z[ind]
z_tot_zerr[ind] = z_mmt_zerr[ind]
  z_source[ind]   = 'MMT_RG08'
endif
help, ind




ind = where(p_objid eq '1237655373036585119' or $
            p_objid eq '1237659330315288677', cnt)
if cnt ge 1 then z_source[ind] = '2MRS' ; http://adsabs.harvard.edu/cgi-bin/bib_query?2012ApJS..199...26H
ind = where(p_objid eq '1237659330315419891' or $
            p_objid eq '1237659326566236571' or $
            p_objid eq '1237659330852225245', cnt)
if cnt ge 1 then z_source[ind] = 'NFPS' ; http://adsabs.harvard.edu/cgi-bin/bib_query?2004AJ....128.1558S
ind = where(p_objid eq '1237659330852421695' or $
            p_objid eq '1237659325492691070', cnt)
if cnt ge 1 then z_source[ind] = 'Z90' ; http://adsabs.harvard.edu/cgi-bin/bib_query?1990ApJS...74....1Z
ind = where(p_objid eq '1237655472357508457', cnt)
if cnt ge 1 then z_source[ind] = 'W05' ; http://adsabs.harvard.edu/cgi-bin/bib_query?2005ApJ...634..715W
ind = where(p_objid eq '1237659330315681928' or $
            p_objid eq '1237659324955820509', cnt)
if cnt ge 1 then z_source[ind] = 'SDSS' ; originally the spectrum is from SDSS, but reanalyzed in http://adsabs.harvard.edu/cgi-bin/bib_query?2010MNRAS.405.2302H
ind = where(p_objid eq '1237659324955492627' or $
            p_objid eq '1237659325492232304' or $
            p_objid eq '1237659326565908835' or $
            p_objid eq '1237659324955689520' or $
            p_objid eq '1237655373036912766' or $
            p_objid eq '1237659330314830167' or $
            p_objid eq '1237659330315485209' or $
            p_objid eq '1237655472357310527', cnt)
if cnt ge 1 then z_source[ind] = 'R02' ; http://adsabs.harvard.edu/cgi-bin/bib_query?2002AJ....124.1266R
ind = where(p_objid eq '1237659326565843262', cnt)
if cnt ge 1 then z_source[ind] = 'P99' ; http://adsabs.harvard.edu/cgi-bin/bib_query?1999A%26AS..137..299P
ind = where(p_objid eq '1237659326029758827', cnt)
if cnt ge 1 then z_source[ind] = 'C90' ;http://adsabs.harvard.edu/cgi-bin/bib_query?1990AJ....100...47C

ind = where(p_objid eq '1237659326029365297', cnt)
if cnt ge 1 then z_source[ind] = 'B02' ;http://adsabs.harvard.edu/cgi-bin/bib_query?2002AJ....123.2990B
ind = where(p_objid eq '1237659326029365292' or $
            p_objid eq '1237659326029430936' or $
            p_objid eq '1237659330315354275' or $
            p_objid eq '1237659326029299889', cnt)
if cnt ge 1 then z_source[ind] = 'HO98' ;http://adsabs.harvard.edu/cgi-bin/bib_query?1998AJ....116.1529H



indmmt    = where(z_source eq 'MMT')  & help, indmmt
indmmtrg  = where(z_source eq 'MMT_RG08')  & help, indmmtrg
indmmtr13 = where(z_source eq 'MMT_R13')  & help, indmmtr13
indr02  = where(z_source eq 'R02')  & help, indr02
indsdss = where(z_source eq 'SDSS') & help, indsdss
indned  = where(z_source eq 'NED')  & help, indned
indsdssned  = where(z_source eq 'SDSS_NED')  & help, indsdssned
indn = where(z_source eq 'N')  & help, indn
indu = where(z_source eq 'U' and z_tot_z gt -1)  & help, indu

print, z_source(uniq(z_source, sort(z_source)))

indmmtkias14 = where(z_dfilename eq 'skysub_a2199a_1' or $
                     z_dfilename eq 'skysub_a2199a_2', cnt) & help, indmmtkias14
indmmtkias15 = where(z_dfilename eq 'skysub_a2199b15_1' or $
                     z_dfilename eq 'skysub_a2199b15_2', cnt) & help, indmmtkias15
indmmtkias19 = where(z_dfilename eq 'skysub_a2199a19_1' or $
                     z_dfilename eq 'skysub_a2199a19_2' or $
                     z_dfilename eq 'skysub_a2199a19_3' or $
                     z_dfilename eq 'skysub_a2199a19_4', cnt) & help, indmmtkias19

; Membership from AD 2013 Aug 20
memflag     = strarr(n_elements(z_tot_z)) + 'N'
file = 'a2199.hoseong.tab.010.q25.memb'
readcol, dirc + file, mra, mde, vv, vvv, f = 'd,d,a,a', skipl = 1
vv_vvv = strcompress(vv + '_' + vvv, /remov)
ind = where(vv_vvv ne '8576.999798_2.405428' and $
		            vv_vvv ne '8976.000004_8.034377')
mra = mra[ind]
mde = mde[ind]

tolerance=0.5 ; MJKim's suggestion
;hs_radecmatch,tolerance, p_ra, p_dec, mra, mde,$
hs_radecmatch,tolerance, mra, mde, p_ra, p_dec, $
 indxfile1call,indxfile2call,nonindxfile1call,nonindxfile2call, $
 dra12,ddec12,dist12,pa12,kindx12,matchednum12
par = 'mem'
hs_match, dra12, ddec12, tolerance, string(mra), p_objid, $
 indxfile1call, indxfile2call, kindx12, dist12, $
 dir = dir, par = par
memflag[indxfile2call] = 'Y'
hs_stat, z_tot_z[indxfile2call]

; To update the membership for new MMT data
readcol, dirc + 'a2199.hoseong.tab.010.q25.mprof', $
 c_r, c_v, ec_v, f ='f,f,f', skipl = 1
xx = c_r * degMpc * 60.
rvtot =  (z_tot_z *c - zcl * c) / (1. + zcl)

toto = where(memflag ne 'Y' and p_radgal le 40. and $
  (z_mmt_velqual eq 'Q' or z_mmt_velqual eq 'N'), cnt)
help, toto
pc_v = p_radgal * 0.
if cnt ge 1 then begin
  pc_v[toto] = interpol([2042.5,2042.5,2042.5,c_v], [0.,1,2.,xx], p_radgal[toto])
  nind0 = where(abs(rvtot[toto]) - pc_v[toto] le 0, tcnt)
  nind  = toto[nind0]
  help, tcnt
  if tcnt ge 1 then memflag[nind] = 'Y'
;  oplot, radtot[nind], rvtot[nind]/1000., psym=8, symsi = osize, color = !green
endif




indmem = where(memflag eq 'Y')
help, indmem

ind = where(p_phtype0 lt 9, cnt)
if cnt ge 1 then $
  p_phtype[ind] = p_phtype0[ind]


ind = where(z_sdss_errvdisp_cas le 0, cnt)
if cnt ge 1 then z_sdss_vdisp_cas[ind] = -9.
ind = where(z_sdss_errvdisp_wis le 0, cnt)
if cnt ge 1 then z_sdss_vdisp_wis[ind] = -9.
ind = where(z_sdss_errvdisp_mpa le 0, cnt)
if cnt ge 1 then z_sdss_vdisp_mpa[ind] = -9.
ind = where(z_sdss_errvdisp_pm le 0, cnt)
if cnt ge 1 then z_sdss_vdisp_pm[ind] = -9.
ind = where(v_disp_err le 0, cnt)
if cnt ge 1 then v_dispersion[ind] = -9.


pointflag = intarr(n_elements(p_phtype))
tmp = where(p_probpsf ne 0 and p_phtype ne 1 and p_phtype ne 2, cnt) & help, tmp
if cnt ge 1 then pointflag[tmp] = 1
tmp = where(p_phtype eq 3, cnt) & help, tmp
if cnt ge 1 then pointflag[tmp] = 1

ind = where(p_objid eq '1237659330315289487', cnt)
if cnt ge 1 then print, z_tot_z[ind]


ind = where(p_objid eq '1237659330852225683', cnt)
if cnt ge 1 then print, z_tot_z[ind], z_mmt_z[ind], z_mmt_tfilename[ind], z_source[ind]
ind = where(p_objid eq '1237655471820833457', cnt)
ind = where(p_objid eq '1237655471820833502', cnt)
ind = where(p_objid eq '1237659330315289504', cnt)
ind = where(p_objid eq '1237659330315354729', cnt)
ind = where(p_objid eq '1237659330315420341', cnt)

;stop
ind = where(p_objid eq '1237659330315289347', cnt)

;help, z_ned_id, z_ned_z, z_sdss_z, z_tot_z, z_source
save, FILENAME=dirc + filew, /compress, $
 pointflag, $
 inf_jmass, jmass, sup_jmass, $
 p_phtype, memflag, $
 z_sdss_vdisp_cas, z_sdss_errvdisp_cas, $
 z_sdss_vdisp_wis, z_sdss_errvdisp_wis, $
 z_sdss_vdisp_mpa, z_sdss_errvdisp_mpa, $
 z_sdss_vdisp_pm,  z_sdss_errvdisp_pm, $
 z_specclass, z_subclass, $
 z_plate, z_mjd, z_fiberID, z_specobjid, z_dr7specobjid, $
 v_dispersion, v_disp_err, v_SN, v_chisq, $
; z_wegner_id, z_wegner_z, $
 z_r13_id, z_r13_z, $
 z_ned_id, z_ned_z, z_sdss_z, z_sdss_zerr, z_tot_z, z_tot_zerr, z_source

; wid, wrafsc, wdecfsc, $
; wf3p4Jy, wf3p4Jyerr, wf3p4snr, $
; wf4p6Jy, wf4p6Jyerr, wf4p6snr, $
; wf12Jy, wf12Jyerr, wf12snr, $
; wf22Jy, wf22Jyerr, wf22snr


END
