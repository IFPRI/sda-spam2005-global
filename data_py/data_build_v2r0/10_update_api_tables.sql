ALTER TABLE quickstart_yield RENAME TO quickstart_yield_v1r0;
create table quickstart_yield as select * from spam2005v2r0_yield;
alter table quickstart_yield rename column ogc_fid to id;
alter table quickstart_yield add column x numeric(19,5);
alter table quickstart_yield add column y numeric(19,5);
alter table quickstart_yield add column hc_seq5m numeric(19,5);
alter table quickstart_yield owner to djuser;
alter table quickstart_yield alter column cell5m type integer using cell5m::integer;

ALTER TABLE quickstart_prod RENAME TO quickstart_prod_v1r0;
create table quickstart_prod as select * from spam2005v2r0_production;
alter table quickstart_prod rename column ogc_fid to id;
alter table quickstart_prod add column x numeric(19,5);
alter table quickstart_prod add column y numeric(19,5);
alter table quickstart_prod add column hc_seq5m numeric(19,5);
alter table quickstart_prod owner to djuser;
alter table quickstart_prod alter column cell5m type integer using cell5m::integer;

ALTER TABLE quickstart_area RENAME TO quickstart_area_v1r0;
create table quickstart_area as select * from spam2005v2r0_physical_area;
alter table quickstart_area rename column ogc_fid to id;
alter table quickstart_area add column x numeric(19,5);
alter table quickstart_area add column y numeric(19,5);
alter table quickstart_area add column hc_seq5m numeric(19,5);
alter table quickstart_area owner to djuser;
alter table quickstart_area alter column cell5m type integer using cell5m::integer;

ALTER TABLE quickstart_harvested RENAME TO quickstart_harvested_v1r0;
create table quickstart_harvested as select * from spam2005v2r0_harvested_area;
alter table quickstart_harvested rename column ogc_fid to id;
alter table quickstart_harvested add column x numeric(19,5);
alter table quickstart_harvested add column y numeric(19,5);
alter table quickstart_harvested add column hc_seq5m numeric(19,5);
alter table quickstart_harvested owner to djuser;
alter table quickstart_harvested alter column cell5m type integer using cell5m::integer;

create index on quickstart_yield(id);
create index on quickstart_prod(id);
create index on quickstart_harvested(id);
create index on quickstart_area(id);

create index on quickstart_yield(cell5m);
create index on quickstart_prod(cell5m);
create index on quickstart_harvested(cell5m);
create index on quickstart_area(cell5m);

CREATE INDEX quickstart_yield_geom_idx ON quickstart_yield USING GIST (wkb_geometry);
CREATE INDEX quickstart_prod_geom_idx ON quickstart_prod USING GIST (wkb_geometry);
CREATE INDEX quickstart_area_geom_idx ON quickstart_area USING GIST (wkb_geometry);
CREATE INDEX quickstart_harvested_geom_idx ON quickstart_harvested USING GIST (wkb_geometry);

for i in whea rice maiz barl pmil smil sorg ocer pota swpo yams cass orts bean chic cowp pige lent opul soyb grou cnut oilp sunf rape sesa ooil sugc sugb cott ofib acof rcof coco teas toba bana plnt trof temf vege rest whea_i rice_i maiz_i barl_i pmil_i smil_i sorg_i ocer_i pota_i swpo_i yams_i cass_i orts_i bean_i chic_i cowp_i pige_i lent_i opul_i soyb_i grou_i cnut_i oilp_i sunf_i rape_i sesa_i ooil_i sugc_i sugb_i cott_i ofib_i acof_i rcof_i coco_i teas_i toba_i bana_i plnt_i trof_i temf_i vege_i rest_i whea_r rice_r maiz_r barl_r pmil_r smil_r sorg_r ocer_r pota_r swpo_r yams_r cass_r orts_r bean_r chic_r cowp_r pige_r lent_r opul_r soyb_r grou_r cnut_r oilp_r sunf_r rape_r sesa_r ooil_r sugc_r sugb_r cott_r ofib_r acof_r rcof_r coco_r teas_r toba_r bana_r plnt_r trof_r temf_r vege_r rest_r; do sudo -u postgres psql -d djspamdata -c "alter table quickstart_yield alter column ${i} type double precision using ${i}::double precision;"; done;

for i in whea rice maiz barl pmil smil sorg ocer pota swpo yams cass orts bean chic cowp pige lent opul soyb grou cnut oilp sunf rape sesa ooil sugc sugb cott ofib acof rcof coco teas toba bana plnt trof temf vege rest whea_i rice_i maiz_i barl_i pmil_i smil_i sorg_i ocer_i pota_i swpo_i yams_i cass_i orts_i bean_i chic_i cowp_i pige_i lent_i opul_i soyb_i grou_i cnut_i oilp_i sunf_i rape_i sesa_i ooil_i sugc_i sugb_i cott_i ofib_i acof_i rcof_i coco_i teas_i toba_i bana_i plnt_i trof_i temf_i vege_i rest_i whea_r rice_r maiz_r barl_r pmil_r smil_r sorg_r ocer_r pota_r swpo_r yams_r cass_r orts_r bean_r chic_r cowp_r pige_r lent_r opul_r soyb_r grou_r cnut_r oilp_r sunf_r rape_r sesa_r ooil_r sugc_r sugb_r cott_r ofib_r acof_r rcof_r coco_r teas_r toba_r bana_r plnt_r trof_r temf_r vege_r rest_r; do sudo -u postgres psql -d djspamdata -c "alter table quickstart_harvested alter column ${i} type double precision using ${i}::double precision;"; done;

for i in whea rice maiz barl pmil smil sorg ocer pota swpo yams cass orts bean chic cowp pige lent opul soyb grou cnut oilp sunf rape sesa ooil sugc sugb cott ofib acof rcof coco teas toba bana plnt trof temf vege rest whea_i rice_i maiz_i barl_i pmil_i smil_i sorg_i ocer_i pota_i swpo_i yams_i cass_i orts_i bean_i chic_i cowp_i pige_i lent_i opul_i soyb_i grou_i cnut_i oilp_i sunf_i rape_i sesa_i ooil_i sugc_i sugb_i cott_i ofib_i acof_i rcof_i coco_i teas_i toba_i bana_i plnt_i trof_i temf_i vege_i rest_i whea_r rice_r maiz_r barl_r pmil_r smil_r sorg_r ocer_r pota_r swpo_r yams_r cass_r orts_r bean_r chic_r cowp_r pige_r lent_r opul_r soyb_r grou_r cnut_r oilp_r sunf_r rape_r sesa_r ooil_r sugc_r sugb_r cott_r ofib_r acof_r rcof_r coco_r teas_r toba_r bana_r plnt_r trof_r temf_r vege_r rest_r; do sudo -u postgres psql -d djspamdata -c "alter table quickstart_prod alter column ${i} type double precision using ${i}::double precision;"; done;

for i in whea rice maiz barl pmil smil sorg ocer pota swpo yams cass orts bean chic cowp pige lent opul soyb grou cnut oilp sunf rape sesa ooil sugc sugb cott ofib acof rcof coco teas toba bana plnt trof temf vege rest whea_i rice_i maiz_i barl_i pmil_i smil_i sorg_i ocer_i pota_i swpo_i yams_i cass_i orts_i bean_i chic_i cowp_i pige_i lent_i opul_i soyb_i grou_i cnut_i oilp_i sunf_i rape_i sesa_i ooil_i sugc_i sugb_i cott_i ofib_i acof_i rcof_i coco_i teas_i toba_i bana_i plnt_i trof_i temf_i vege_i rest_i whea_r rice_r maiz_r barl_r pmil_r smil_r sorg_r ocer_r pota_r swpo_r yams_r cass_r orts_r bean_r chic_r cowp_r pige_r lent_r opul_r soyb_r grou_r cnut_r oilp_r sunf_r rape_r sesa_r ooil_r sugc_r sugb_r cott_r ofib_r acof_r rcof_r coco_r teas_r toba_r bana_r plnt_r trof_r temf_r vege_r rest_r; do sudo -u postgres psql -d djspamdata -c "alter table quickstart_area alter column ${i} type double precision using ${i}::double precision;"; done;