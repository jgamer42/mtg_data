import os
import sys
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
from data.dataSources import ScryFall
from databases.SQL import models as SQL_model
from databases import SQL_database
source = ScryFall()

sets_to_insert = []
for set in source.list_sets():
    if set['set_type']  in ['alchemy',"token","memorabilia"] or set["digital"] or "tokens" in set["name"].lower():
        continue
    target_set = SQL_model.Set(name=set["name"],kind=set["set_type"],code=set["code"],scry_fall_id=set["id"])
    sets_to_insert.append(target_set)
SQL_database.bulk_save_objects(sets_to_insert)
SQL_database.commit()
