cd /Users/maria/Projects/spam2005-global/data_py/data_build_v2r0/data_raw/hc_grid
import the global world grid to postgres: hc_seq5m.asc


# local:
use QGIS to convert asc to shp
gdal_polygonize.py /Users/maria/Projects/spam2005-global/data_py/data_build_v2r0/hc_grid/hc_seq5m.asc -f "ESRI Shapefile" /Users/maria/Projects/spam2005-global/data_py/data_build_v2r0/data_in/hc_grid5m2.shp hc_grid5m

import grid shp to postgis
/Applications/Postgres.app/Contents/Versions/9.3/bin/ogr2ogr -f "PostgreSQL" PG:"user=djuser dbname=djspamdata password=djpass" hc_grid5m.shp

# server
ogr2ogr -f "PostgreSQL" PG:"user=djuser dbname=djspamdata password=djpass" hc_grid5m.shp -nln hc_grid5m_all

# keep track and update missing geometries
create table null_geoms_in_v2r0 as select cell5m, alloc_key from quickstart_yield where wkb_geometry is null;

update quickstart_yield y set wkb_geometry = (select h.wkb_geometry from hc_grid5m_all h where h.dn = y.cell5m);
update quickstart_prod y set wkb_geometry = (select h.wkb_geometry from hc_grid5m_all h where h.dn = y.cell5m);
update quickstart_harvested y set wkb_geometry = (select h.wkb_geometry from hc_grid5m_all h where h.dn = y.cell5m);
update quickstart_area y set wkb_geometry = (select h.wkb_geometry from hc_grid5m_all h where h.dn = y.cell5m);

update spam2005v2r0_production y set wkb_geometry = (select h.wkb_geometry from hc_grid5m_all h where h.dn = y.cell5m);
update spam2005v2r0_harvested_area y set wkb_geometry = (select h.wkb_geometry from hc_grid5m_all h where h.dn = y.cell5m);
update spam2005v2r0_physical_area y set wkb_geometry = (select h.wkb_geometry from hc_grid5m_all h where h.dn = y.cell5m);
update spam2005v2r0_yield y set wkb_geometry = (select h.wkb_geometry from hc_grid5m_all h where h.dn = y.cell5m);

select count(*) from spam2005v2r0_production y, hc_grid5m_all h where y.cell5m = h.cell5m and y.wkb_geometry <> h.wkb_geometry;

# export spam v2r0 cell5m grid to put on the box
gdal_rasterize -a cell5m -te -180 -90 180 90 -ts 4320 2160 -a_srs EPSG:4326 -a_nodata -9999 -co "COMPRESS=LZW" -l quickstart_yield PG:"dbname=djspamdata user=postgres" hc_grid5m_spam_v2r0.tiff

