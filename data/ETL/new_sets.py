import os
import sys
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
from data.dataSources import ScryFall
from databases.SQL import models as SQL_model
from databases import SQL_database

source = ScryFall()
existent_set = SQL_database.query(SQL_model.Set.code).all()
existent_set = set([s[0] for s in existent_set])
sets_to_insert  = []
for set in source.list_sets():
    if set['set_type']  in ['alchemy',"token","memorabilia"] or set["digital"] or "tokens" in set["name"].lower():
        continue
    if set["code"] in existent_set:
        continue
    target_set = SQL_model.Set(name=set["name"],kind=set["set_type"],code=set["code"],scry_fall_id=set["id"],release_date=set["released_at"],is_spoiler=True)
    sets_to_insert.append(target_set)
SQL_database.bulk_save_objects(sets_to_insert)
SQL_database.commit()