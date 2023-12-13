#!/bin/bash

source env/bin/activate
#python data/ETL/sets.py
python data/ETL/cards.py
python data/ETL/faces.py
python data/ETL/prints.py


