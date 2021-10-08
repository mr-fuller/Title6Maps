#!/bin/bash
creds=/media/mike/OS/Users/fullerm/OneDrive/Documents/"Work Computer Files"/PycharmProjects/Title6Maps/credentials.json
#creds = ./credentials.json
year=$1
gdb_loc=$(jq .file_loc "$creds" -r)
pguser=$(jq .pg_username "$creds" -r)
pgpw=$(jq .pg_password "$creds" -r)
dbname=title6
state_abvs=('39_oh' '26_mi')
base_url=https://www2.census.gov/geo/tiger/TGRGDB${year: -2}/tlgdb_${year}_a_

for state_abv in "${state_abvs[@]}"
do
echo $base_url${state_abv}.gdb.zip
curl  $base_url${state_abv}.gdb.zip > tlgdb_${year}_a_${state_abv}.gdb.zip

#unzip the gdb
unzip tlgdb_${year}_a_${state_abv}.gdb.zip

#put in postgres the Census Tract and block group layers, and county and county subdivision
#because I'm sick of the separate shapefiles for separate counties
#note that each db has "Census"
ogr2ogr -f "PostgreSQL" PG:"host=localhost user=$pguser dbname=$dbname password=$pgpw" tlgdb_${year}_a_${state_abv}.gdb "Block_Group" -nln bg_${state_abv}_${year}
ogr2ogr -f "PostgreSQL" PG:"host=localhost user=$pguser dbname=$dbname password=$pgpw" tlgdb_${year}_a_${state_abv}.gdb "Census_Tract" -nln ct_${state_abv}_${year}
ogr2ogr -f "PostgreSQL" PG:"host=localhost user=$pguser dbname=$dbname password=$pgpw" tlgdb_${year}_a_${state_abv}.gdb "County" -nln county_${state_abv}_${year}
ogr2ogr -f "PostgreSQL" PG:"host=localhost user=$pguser dbname=$dbname password=$pgpw" tlgdb_${year}_a_${state_abv}.gdb "County_Subdivision" -nln cousub_${state_abv}_${year}
done