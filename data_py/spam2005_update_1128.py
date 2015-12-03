 
Remove year_data, source, scale_year from regional CSV files:

ex: cut -d, -f 218-220 --complement spam2005V2r0_OCEANIA_A.csv  > spam2005V2r0_OCEANIA_A_updated.csv

for i in `ls *.csv`; do echo $i; done;

for i in `ls *.zip`; unzip $i; done;

for i in `ls *.csv`; do cut -d, -f 218-220 --complement $i > $i_new; done;

for i in `ls *.csv`; do mv $i_new $i; done;

