#!/bin/bash

filegas="mech_gas.inp"
filesurf="mech_surf.inp"

# site density (for Pt(111))
SDEN=2.9E-9

# eV to calories/mole conversion
eV2cal=3.8293E-20
avg=6.0221367E23

sed 's/*/X/g' mech | sed 's/->/=/g' > mech_v0.txt
awk 'NR>3 && NR<12 {print}' mech_V0.txt > mech_v0Stick.txt
awk '{print $2"  1.0  0.0  0.0"; print "STICK"}' mech_v0Stick.txt > tmp1; mv tmp1 mech_v0Stick.txt
awk 'NR>11 && NR<53 {print}' mech_V0.txt > mech_v0Regular.txt
awk -v sd=${SDEN} -v e2c=${eV2cal} -v av=${avg} '{printf("%s \t\t%e 0.0 %e\n"),$2,$6/sd,$5*e2c*av}' mech_v0Regular.txt > tmp1; mv tmp1 mech_v0Regular.txt

cat mech_v0Stick.txt mech_v0Regular.txt | \
    awk '{print $1}' | \
    sed 's/+/ /g' | \
    sed 's/=/ /g' | \
    awk '{for (i = 1; i <= NF; i++) {print $i}}' | \
    sed 's/^[0-9]\+*//g' | \
    awk '!NF || !seen[$0]++' | sed 's/STICK//g' | awk 'NF' > species.txt

# Gas-phase input
sed 's/[^ ]*X[^ ]*//g' species.txt | awk 'NF'> species_gas.txt
sort -o tmp1 species_gas.txt; mv tmp1 species_gas.txt
echo -e "ELEM\nH\nC\nO" > ${filegas}
echo -e "X /63.546/\nEND" >> ${filegas}
echo "SPEC"              >> ${filegas}
cat ${filegas} species_gas.txt > tmp1; mv tmp1 ${filegas}
echo "END"               >> ${filegas}
echo -e "THERMO\nEND"    >> ${filegas}
echo -e "REACTIONS\nEND" >> ${filegas}

# Surface input
sort -o tmp1 species.txt; mv tmp1 species.txt
comm -23 species.txt species_gas.txt > species_surf.txt
echo "SITE SDEN/${SDEN}/" > ${filesurf}
cat ${filesurf} species_surf.txt > tmp1; mv tmp1 ${filesurf}
echo "END" >> ${filesurf}
echo -e "THERMO\nEND" >> ${filesurf}
echo -e "REACTIONS"   >> ${filesurf}
cat ${filesurf} mech_v0Stick.txt mech_v0Regular.txt > tmp1; mv tmp1 ${filesurf}
echo "END" >> ${filesurf}

# cleanup 
#/bin/rm species.txt

exit
