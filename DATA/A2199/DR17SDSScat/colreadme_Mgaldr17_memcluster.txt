# Please note that this file is prepared only for the work of Rory, which means that you need to ask Ho Seong whether you can use these columns for your work.
clmemflag STRING : Cluster Membership Flag ('U' - unknown, 'N' - not a member, 'ClusterNAME' - Member of that cluster - The flags for the galaxies without Caustics membership were manually added by the velocity envelop of previously known members. This is may not be a pefect method for your work, so please use with extreme caution.)
clcomp    STRING : Spectroscopic completeness for a given magnitude limit (defined below at clmagl)
clmagl    FLOAT  : Magnitude limit used for defining the spectroscopic completeness 
bcgflag   STRING : BCG flag ('Y'-yes, 'N'-no; defined only for cluster z_cl>0.01; brightest galaxy among members at R_p<0.5*r_200)
