# PSQL
CREATE INDEX ON hc_grid5m (cell5m);

alter table spam2005v2_yield alter column cell5m type numeric(19,5) using cell5m::numeric;
alter table spam2005v2_harvested_area alter column cell5m  type numeric(19,5) using cell5m::numeric;
alter table spam2005v2_production alter column cell5m type numeric(19,5) using cell5m::numeric;
alter table spam2005v2_physical_area alter column cell5m  type numeric(19,5) using cell5m::numeric;

SELECT AddGeometryColumn ('spam2005v2_yield','wkb_geometry',4326,'POLYGON',2);
SELECT AddGeometryColumn ('spam2005v2_harvested_area','wkb_geometry',4326,'POLYGON',2);
SELECT AddGeometryColumn ('spam2005v2_production','wkb_geometry',4326,'POLYGON',2);
SELECT AddGeometryColumn ('spam2005v2_physical_area','wkb_geometry',4326,'POLYGON',2);
CREATE INDEX spam2005v2_yield_geom_idx ON spam2005v2_yield USING GIST (wkb_geometry);
CREATE INDEX spam2005v2_harvested_area_geom_idx ON spam2005v2_harvested_area USING GIST (wkb_geometry);
CREATE INDEX spam2005v2_production_geom_idx ON spam2005v2_production USING GIST (wkb_geometry);
CREATE INDEX spam2005v2_physical_area_geom_idx ON spam2005v2_physical_area USING GIST (wkb_geometry);

CREATE INDEX ON spam2005v2_yield (cell5m);
CREATE INDEX ON spam2005v2_harvested_area (cell5m);
CREATE INDEX ON spam2005v2_production (cell5m);
CREATE INDEX ON spam2005v2_physical_area (cell5m);

update spam2005v2_yield y set wkb_geometry = (select h.wkb_geometry from hc_grid5m h where h.cell5m = y.cell5m);
update spam2005v2_harvested_area y set wkb_geometry = (select h.wkb_geometry from hc_grid5m h where h.cell5m = y.cell5m);
update spam2005v2_production y set wkb_geometry = (select h.wkb_geometry from hc_grid5m h where h.cell5m = y.cell5m);
update spam2005v2_physical_area y set wkb_geometry = (select h.wkb_geometry from hc_grid5m h where h.cell5m = y.cell5m);





alter table spam2005v2_yield_chunck alter column maiz type numeric(19,5) using maiz::numeric;
alter table spam2005v2_harvested_area_chunck alter column maiz  type numeric(19,5) using maiz::numeric;
alter table spam2005v2_yield_chunck alter column vege type numeric(19,5) using vege::numeric;
alter table spam2005v2_harvested_area_chunck alter column vege  type numeric(19,5) using vege::numeric;
alter table spam2005v2_yield_chunck alter column soyb type numeric(19,5) using soyb::numeric;
alter table spam2005v2_harvested_area_chunck alter column soyb  type numeric(19,5) using soyb::numeric;
alter table spam2005v2_yield_chunck alter column whea type numeric(19,5) using whea::numeric;
alter table spam2005v2_harvested_area_chunck alter column whea type numeric(19,5) using whea::numeric;
alter table spam2005v2_yield_chunck alter column rice type numeric(19,5) using rice::numeric;
alter table spam2005v2_harvested_area_chunck alter column rice type numeric(19,5) using rice::numeric;

