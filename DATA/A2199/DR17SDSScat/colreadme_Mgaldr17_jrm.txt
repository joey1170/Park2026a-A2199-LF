# NOTE that the number of galaxies in this file is different from those in other files.
# Therefore, you should find MATCHES using idd, matched with s3_objid in Mgaldr12_id.sav
# SEE https://sites.google.com/site/decompir/ for details about this SED fitting routine
idd        STRING    : ObjId in SDSS DR9
outall     STRUCTURE : structure containing all the fit parameters and a number of useful values derived from the fit
ojlir      FLOAT     : log of (total IR luminosity/Lsun) 
ojafrac    FLOAT     : AGN contribution to total IR luminosity  
ojfitflag  INT       : 2 - ojlir means lower limits, 1 - normal galaxies with proper SED fit, 0 - not fitted with decompir 
