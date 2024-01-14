# Tinkertools

A set of web-based utilities for the sci-fi MMORPG Anarchy Online. 

### Tinkerplants

Implant design and planning, with full requirements to build and equip

### Tinkernanos

Profession-specific nano program list with skill-based filtering

### Tinkernukes

Nanotechnician nuke table that suggests best available nukes for your setup

### Tinkerfite

Weapon table that suggests weapon options for your setup

### Tinkerpocket

Symbiant and Pocket Boss database

## Dependencies

See requirements.txt for the full list. Tinkertools is built and runs on Ubuntu linux, but is written in python3 so can probably be made to run on about anything. 

## Setup

1. Clone this repository: `git clone`

2. Install dependencies: `pip3 install -r requirements.txt`

3. Migrate database: `python3 manage.py migrate`

4. Populate database: `python3 update_db.py`

## Running

1. `python3 manage.py runserver`

## Updating the database

This repo includes up-to-date data (data.json) for the latest AO client as of June 2023. This will be kept up to the best of my ability, but future updates can be accomplished by anyone using these steps:

1. Update your AO client.

2. Get bitnykk's versions of Auno's database dumper (adbd) from https://github.com/bitnykk/adbd and database parser (aoppa) from https://github.com/bitnykk/aoppa.

3. Dump the AO database using adbd (on Windows where the AO client is). At a minimum this needs to be done twice to dump the items and nanos. 

    `adbd.exe "C:\\Funcom\\Anarchy Online" item`

    `adbd.exe "C:\\Funcom\\Anarchy Online" nano`

    This will create two .dat files, one for items and one for nanos. 

4. Parse the dumped data into XML using aoppa (on Linux, unless you're building from bitnykk's source).

    `./aoppa -p input-gzip.so -p output-xml.so ../adbd/Release/items-18086100ep1.dat > items.xml`

    `./aoppa -p input-gzip.so -p output-xml.so ../adbd/Release/nanos-18086100ep1.dat > nanos.xml`

    This will create two XML files, one for items and one for nanos. Tinkertools needs these files to populate the database. 

5. Clean up the raw database data into something Tinkertools can use.

    `python3 dump_json.py -i items.xml -n nanos.xml -o data.json`

    This outputs a single data.json file that includes all items, nanos, symbiants, and pocket boss information (taken from symbiants.csv - thank you AOPocket!) - everything the Tinkertools need. 

6. Update the database with the new data.

    `python3 update_db.py`

    The Tinkertools database is now updated and ready to use!



