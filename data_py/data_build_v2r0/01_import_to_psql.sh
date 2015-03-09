cd /Users/maria/Projects/SPAM2005v2_data_build/20150225/data_in

/Applications/Postgres.app/Contents/Versions/9.3/bin/ogr2ogr -f "PostgreSQL" PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_yield_chunck.csv
/Applications/Postgres.app/Contents/Versions/9.3/bin/ogr2ogr -f "PostgreSQL" PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_harvested-area_chunck.csv