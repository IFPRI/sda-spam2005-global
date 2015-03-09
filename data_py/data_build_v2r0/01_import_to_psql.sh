cd /Users/maria/Projects/spam2005-global/data_py/data_build_v2r0/data_in

mv spam2005v2r0_yield.csv spam2005v2r0_yield_latin1.csv
mv spam2005v2r0_production.csv spam2005v2r0_production_latin1.csv
mv spam2005v2r0_physical-area.csv spam2005v2r0_physical-area_latin1.csv
mv spam2005v2r0_harvested-area.csv spam2005v2r0_harvested-area_latin1.csv

iconv -f latin1 -t utf-8 spam2005v2r0_harvested-area_latin1.csv > spam2005v2r0_harvested-area.csv
iconv -f latin1 -t utf-8 spam2005v2r0_physical-area_latin1.csv > spam2005v2r0_physical-area.csv
iconv -f latin1 -t utf-8 spam2005v2r0_production_latin1.csv > spam2005v2r0_production.csv
iconv -f latin1 -t utf-8 spam2005v2r0_yield_latin1.csv > spam2005v2r0_yield.csv

# server
sudo -u postgres ogr2ogr -f "PostgreSQL" PG:"user=djuser dbname=djspamdata password=djpass" spam2005v2r0_harvested-area.csv
sudo -u postgres ogr2ogr -f "PostgreSQL" PG:"user=djuser dbname=djspamdata password=djpass" spam2005v2r0_yield.csv
sudo -u postgres ogr2ogr -f "PostgreSQL" PG:"user=djuser dbname=djspamdata password=djpass" spam2005v2r0_physical-area.csv
sudo -u postgres ogr2ogr -f "PostgreSQL" PG:"user=djuser dbname=djspamdata password=djpass" spam2005v2r0_production.csv

# local:
/Applications/Postgres.app/Contents/Versions/9.3/bin/ogr2ogr -f "PostgreSQL" PG:"user=djuser dbname=djspamdata password=djpass" spam2005v2r0_harvested-area.csv
/Applications/Postgres.app/Contents/Versions/9.3/bin/ogr2ogr -f "PostgreSQL" PG:"user=djuser dbname=djspamdata password=djpass" spam2005v2r0_yield.csv
/Applications/Postgres.app/Contents/Versions/9.3/bin/ogr2ogr -f "PostgreSQL" PG:"user=djuser dbname=djspamdata password=djpass" spam2005v2r0_physical-area.csv
/Applications/Postgres.app/Contents/Versions/9.3/bin/ogr2ogr -f "PostgreSQL" PG:"user=djuser dbname=djspamdata password=djpass" spam2005v2r0_production.csv