#!/bin/bash

source env/bin/activate
python data/ETL/new_sets.py
python data/ETL/spoiler_sets.py
python data/ETL/tournamens.py
