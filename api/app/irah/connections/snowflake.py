import os
from langchain.sql_database import SQLDatabase

SNOWFLAKE_ACCOUNT = os.getenv("ZZ_SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("ZZ_SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("ZZ_SNOWFLAKE_PASSWORD")
SNOWFLAKE_DATABASE = os.getenv("ZZ_SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("ZZ_SNOWFLAKE_SCHEMA")
SNOWFLAKE_WAREHOUSE = os.getenv("ZZ_SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_ROLE = os.getenv("ZZ_SNOWFLAKE_ROLE")

# Connect to Snowflake and keep the session alive
SNOWFLAKE_DB = SQLDatabase.from_uri(
    f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}?role={SNOWFLAKE_ROLE}&warehouse={SNOWFLAKE_WAREHOUSE}&client_session_keep_alive=True"
)

# SNOWFLAKE_DB = SQLDatabase.from_uri(f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}?role={SNOWFLAKE_ROLE}&warehouse={SNOWFLAKE_WAREHOUSE}&client_session_keep_alive=True")


# db = SQLDatabase.from_uri(f"snowflake://{os.getenv('ZZ_SNOWFLAKE_USER')}:{os.getenv('ZZ_SNOWFLAKE_PASSWORD')}@{os.getenv('ZZ_SNOWFLAKE_ACCOUNT')}/{os.getenv('ZZ_SNOWFLAKE_DATABASE')}/{os.getenv('ZZ_SNOWFLAKE_SCHEMA')}?role={os.getenv('ZZ_SNOWFLAKE_ROLE')}&warehouse={os.getenv('ZZ_SNOWFLAKE_WAREHOUSE')}")