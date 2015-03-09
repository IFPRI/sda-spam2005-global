cd /Users/maria/Projects/SPAM2005v2_data_build/20150225/data_out

/Applications/Postgres.app/Contents/Versions/9.3/bin/gdal_rasterize -a maiz -te -180 -90 180 90 -ts 4320 2160 -a_srs EPSG:4326 -a_nodata -9999 -co "COMPRESS=LZW" -l spam2005v2_yield_chunck PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_yield_maiz.tiff
/Applications/Postgres.app/Contents/Versions/9.3/bin/gdal_rasterize -a whea -te -180 -90 180 90 -ts 4320 2160 -a_srs EPSG:4326 -a_nodata -9999 -co "COMPRESS=LZW" -l spam2005v2_yield_chunck PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_yield_whea.tiff
/Applications/Postgres.app/Contents/Versions/9.3/bin/gdal_rasterize -a vege -te -180 -90 180 90 -ts 4320 2160 -a_srs EPSG:4326 -a_nodata -9999 -co "COMPRESS=LZW" -l spam2005v2_yield_chunck PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_yield_vege.tiff
/Applications/Postgres.app/Contents/Versions/9.3/bin/gdal_rasterize -a soyb -te -180 -90 180 90 -ts 4320 2160 -a_srs EPSG:4326 -a_nodata -9999 -co "COMPRESS=LZW" -l spam2005v2_yield_chunck PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_yield_soyb.tiff
/Applications/Postgres.app/Contents/Versions/9.3/bin/gdal_rasterize -a rice -te -180 -90 180 90 -ts 4320 2160 -a_srs EPSG:4326 -a_nodata -9999 -co "COMPRESS=LZW" -l spam2005v2_yield_chunck PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_yield_rice.tiff

/Applications/Postgres.app/Contents/Versions/9.3/bin/gdal_rasterize -a maiz -te -180 -90 180 90 -ts 4320 2160 -a_srs EPSG:4326 -a_nodata -9999 -co "COMPRESS=LZW" -l spam2005v2_harvested_area_chunck PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_harvested_area_maiz.tiff
/Applications/Postgres.app/Contents/Versions/9.3/bin/gdal_rasterize -a whea -te -180 -90 180 90 -ts 4320 2160 -a_srs EPSG:4326 -a_nodata -9999 -co "COMPRESS=LZW" -l spam2005v2_harvested_area_chunck PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_harvested_area_whea.tiff
/Applications/Postgres.app/Contents/Versions/9.3/bin/gdal_rasterize -a vege -te -180 -90 180 90 -ts 4320 2160 -a_srs EPSG:4326 -a_nodata -9999 -co "COMPRESS=LZW" -l spam2005v2_harvested_area_chunck PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_harvested_area_vege.tiff
/Applications/Postgres.app/Contents/Versions/9.3/bin/gdal_rasterize -a soyb -te -180 -90 180 90 -ts 4320 2160 -a_srs EPSG:4326 -a_nodata -9999 -co "COMPRESS=LZW" -l spam2005v2_harvested_area_chunck PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_harvested_area_soyb.tiff
/Applications/Postgres.app/Contents/Versions/9.3/bin/gdal_rasterize -a rice -te -180 -90 180 90 -ts 4320 2160 -a_srs EPSG:4326 -a_nodata -9999 -co "COMPRESS=LZW" -l spam2005v2_harvested_area_chunck PG:"host=localhost user=djuser dbname=djspamdata password=djpass" spam2005v2_harvested_area_rice.tiff

// this is not producing good nc files, use qGis batch transform instead
/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/gdal_translate -of netCDF -co COMPRESS=DEFLATE -co ZLEVEL=9 spam2005v2_yield_maiz.tiff spam2005v2_yield_maiz.nc
/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/gdal_translate -of netCDF -co COMPRESS=DEFLATE -co ZLEVEL=9 spam2005v2_yield_whea.tiff spam2005v2_yield_whea.nc
/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/gdal_translate -of netCDF -co COMPRESS=DEFLATE -co ZLEVEL=9 spam2005v2_yield_vege.tiff spam2005v2_yield_vege.nc
/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/gdal_translate -of netCDF -co COMPRESS=DEFLATE -co ZLEVEL=9 spam2005v2_yield_soyb.tiff spam2005v2_yield_soyb.nc
/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/gdal_translate -of netCDF -co COMPRESS=DEFLATE -co ZLEVEL=9 spam2005v2_yield_rice.tiff spam2005v2_yield_rice.nc

/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/gdal_translate -of netCDF -co COMPRESS=DEFLATE -co ZLEVEL=9 spam2005v2_harvested_area_maiz.tiff spam2005v2_harvested_area_maiz.nc
/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/gdal_translate -of netCDF -co COMPRESS=DEFLATE -co ZLEVEL=9 spam2005v2_harvested_area_whea.tiff spam2005v2_harvested_area_whea.nc
/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/gdal_translate -of netCDF -co COMPRESS=DEFLATE -co ZLEVEL=9 spam2005v2_harvested_area_vege.tiff spam2005v2_harvested_area_vege.nc
/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/gdal_translate -of netCDF -co COMPRESS=DEFLATE -co ZLEVEL=9 spam2005v2_harvested_area_soyb.tiff spam2005v2_harvested_area_soyb.nc
/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/gdal_translate -of netCDF -co COMPRESS=DEFLATE -co ZLEVEL=9 spam2005v2_harvested_area_rice.tiff spam2005v2_harvested_area_rice.nc
