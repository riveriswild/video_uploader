import databases
import sqlalchemy


metadata = sqlalchemy.MetaData()  # to work with sqlalchemy orm that generates requests
database = databases.Database("sqlite:///sqlite.db")
engine = sqlalchemy.create_engine("sqlite:///sqlite.db")