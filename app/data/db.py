'''
Configuring access to Database
- engine (creds + database type)
- individual db-session for each request
'''
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine # just for creating DB - sync way is also afordable
from sqlalchemy_utils import database_exists, create_database

from app.data.orm import Base # all Tables from models inherits from it => can create `em here 
from app.app_config import APP_WORK_CFG # config tells: dev or prod mode is running


MODE = APP_WORK_CFG['WORK_MODE']

host, port = APP_WORK_CFG['db-hosts'][MODE], '5432'
sql_vers, driver = 'postgresql', 'psycopg'  # info about db-engine psycopg: https://pypi.org/project/psycopg/ 
usr, pwd = 'root', 'root'                   # usr/pwd can be set via ENV vars (POSTGRES_USER, POSTGRES_PASSWORD) when db-image is creating
db_name = APP_WORK_CFG['db-name']



# *temporarily* using sync engine - only to check if  database excists and create it (database_exists() works only with sync engine)
sync_engine = create_engine(f"postgresql://{usr}:{pwd}@{host}:{port}/{db_name}")

if not database_exists(sync_engine.url):
    create_database(sync_engine.url)


# switch to async engine: creating async-engine for specific DB: https://docs.sqlalchemy.org/en/20/core/engines.html
DATABSE_URL = f"{sql_vers}+{driver}://{usr}:{pwd}@{host}:{port}/{db_name}"
engine = create_async_engine(DATABSE_URL)


# Create Tables if threre`s not
#Base.metadata.create_all(engine)
async def init_models():
    async with engine.begin() as conn:  
        print('Im inside :)')
        await conn.run_sync(Base.metadata.create_all)


async def recreate_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# Remake DB
# asyncio.run(recreate_db())
# python3 -m app.data.preparing.build_some_tables
# TODO: wrap command above in exec()




# object to create new sessions
sessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False) 

# old way to handle session. now "async with sessionFactory() as session:" is my best friend (capability of AsyncSession with "with" grants right session handling like with handling files)
async def get_db_session():
    '''
        access to db,
        auto-handle db session - close when session is unused (yield gives generator - which is single-use and`ll closed after use) 
    '''
    async with sessionFactory() as db:
        yield db  # yield - not return for Session - generator => session will be lost after using
