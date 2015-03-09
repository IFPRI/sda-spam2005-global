# PSQL
CREATE INDEX ON hc_grid5m (cell5m);

alter table spam2005v2_yield_chunck alter column cell5m type numeric(19,5) using cell5m::numeric;
alter table spam2005v2_harvested_area_chunck alter column cell5m  type numeric(19,5) using cell5m::numeric;

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

SELECT AddGeometryColumn ('spam2005v2_yield_chunck','geom',4326,'POLYGON',2);
SELECT AddGeometryColumn ('spam2005v2_harvested_area_chunck','geom',4326,'POLYGON',2);
CREATE INDEX spam2005v2_yield_chunck_idx ON spam2005v2_yield_chunck USING GIST (geom);
CREATE INDEX spam2005v2_harvested_area_chunck_idx ON spam2005v2_harvested_area_chunck USING GIST (geom);

CREATE INDEX ON spam2005v2_yield_chunck (cell5m);
CREATE INDEX ON spam2005v2_harvested_area_chunck (cell5m);

update spam2005v2_yield_chunck y set geom = (select h.wkb_geometry from hc_grid5m h where h.cell5m = y.cell5m);
update spam2005v2_harvested_area_chunck y set geom = (select h.wkb_geometry from hc_grid5m h where h.cell5m = y.cell5m);
