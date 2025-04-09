import os
import json
import uuid
import datetime as dt
from pydantic import parse_obj_as, BaseModel
import pandas as pd
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, parse_obj_as


class JSONBase:
    DATA_DIR = "app/store/data"

    def __init__(self, table: str, schema: BaseModel):
        if os.path.exists(f"{self.DATA_DIR}/{table}.json"):
            self.filename = f"{self.DATA_DIR}/{table}.json"
            self.schema = schema

            if os.path.exists(self.filename):
                self._read()
            else:
                self.db = pd.DataFrame()
                self._commit()
        else:
            os.makedirs(self.DATA_DIR, exist_ok=True)  # Create the directory if it doesn't exist
            with open(f"{self.DATA_DIR}/{table}.json", 'w') as outfile:
                json.dump({}, outfile)
            
            self.filename = f"{self.DATA_DIR}/{table}.json"
            self.schema = schema

            if os.path.exists(self.filename):
                self._read()
            else:
                self.db = pd.DataFrame()
                self._commit()

    def _commit(self):
        with open(self.filename, "w") as f:
            self.db.to_json(f, orient="index")
        self._read()

    def _read(self):
        with open(self.filename, "r") as f:
            if f.read().strip():
                f.seek(0)  # reset file pointer to start
                self.db = pd.read_json(f, orient="index", convert_dates=False).sort_index()
            else:
                self.db = pd.DataFrame()


class JSONObject(JSONBase):
    def __init__(self, table: str, schema: BaseModel):
        super().__init__(table, schema)

    def _new_key(self):
        return uuid.uuid4().hex.upper()

    def _exists(self, key: str) -> bool:
        return key in self.db.index

    def to_obj(self, key: str):
        dict_data = self.db.loc[key, :].to_dict()
        return self.schema(**dict_data)

    def from_obj(self, item) -> dict:
        return jsonable_encoder(item)

    def get(self, key):
        return self.to_obj(key)

    def create(self, item):
        staging = self.schema(**item.dict())
        staging.key = self._new_key()
        staging.created = dt.datetime.utcnow()
        staging.modified = staging.created
        if not self.db.empty:
            self.db.loc[staging.key] = self.from_obj(staging)
        else:
            self.db = pd.DataFrame([self.from_obj(staging)], index=[staging.key])
        self._commit()
        return self.to_obj(staging.key)

    def insert(self, key, item):
        staging = self.schema(**item.dict())
        staging.key = key
        staging.created = dt.datetime.utcnow()
        staging.modified = staging.created
        if not self.db.empty:
            self.db.loc[staging.key] = self.from_obj(staging)
        else:
            self.db = pd.DataFrame([self.from_obj(staging)], index=[staging.key])
        self._commit()
        return self.to_obj(staging.key)

    def update(self, key: str, updates: dict):
        staging = self.to_obj(key)
        updated = staging.copy(update=updates)
        updated.modified = dt.datetime.now()
        self.db.loc[key] = self.from_obj(updated)
        self._commit()
        return self.to_obj(key)

    def delete(self, key):
        self.db = self.db.drop(index=key)
        self._commit()
        return "deleted"
