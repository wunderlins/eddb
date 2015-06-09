#!/usr/bin/env bash

mv eddb.dat eddb-$(date "+%Y%m%d").dat > /dev/null 2>&1
sqlite3 eddb.dat < schema.sql 

./downloader.py
./parse.py


