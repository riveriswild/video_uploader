import databases
import sqlalchemy
import ormar


metadata = sqlalchemy.MetaData()  # to work with sqlalchemy orm that generates requests
database = databases.Database("sqlite:///sqlite.db")