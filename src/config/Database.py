import sqlite3
from fastapi import Depends
from .EnvironmentVariables import EnvironmentVariables, get_environment_variables

def get_db_connection(environmentVariables: EnvironmentVariables = Depends(get_environment_variables)):
 connection = sqlite3.connect(environmentVariables.db_name)
 return connection