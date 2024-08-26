import os
import sys

import pandas as pd
import pg8000 as pg
import sqlparse
from sqlalchemy import Engine, create_engine
from sqlalchemy import exc as sqla_exc
from sqlalchemy import inspect

sys.path.append("C:\\Users\\sagad\\Desktop\\data-ingestion-aws")
from pathlib import Path

from scripts.definitions import SCRIPTS_DIR
from scripts.utils.log_utils import Logger
from scripts.constants import DB_ENDPOINT, DB_NAME, DB_PASS, DB_PORT, DB_USERNAME

logger = Logger().set_logger()


def setup_rdbms():
    """
    Function to setup mock RDBMS database with all objects required for processing
    """
    try:
        con = None
        con = pg.connect(
            database=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASS,
            host=DB_ENDPOINT,
            port=DB_PORT,
        )
        cursor = con.cursor()
        logger.info("RDBMS Connection successful")
        ROOT_DIR = Path(SCRIPTS_DIR).parent.absolute()
        postgres_ddl_path = os.path.join(ROOT_DIR, "sql", "ddl", "setup_ddls.sql")
        print(postgres_ddl_path)
        file = open(postgres_ddl_path, "r")

        statements = sqlparse.split(file.read())

        for statement in statements:
            logger.info(statement)
            cursor.execute(statement)
            logger.info("Execution successful")

        file.close()

    except Exception as exc:
        logger.error(f"Some exception occurred in function setup_rdbms: {exc}")

    finally:
        if con is not None:
            con.commit()
            cursor.close()


def create_sqlalchemy_engine() -> Engine:
    """Create SQLAlchemy Engine

    Returns:
        sqlalchemy.Engine: SQLAlchemy Engine
    """
    try:
        engine = create_engine(
            f"postgresql://{DB_USERNAME}:{DB_PASS}@{DB_ENDPOINT}:{DB_PORT}/{DB_NAME}",
            pool_pre_ping=True,
        )
        logger.info("Sqlalchemy engine created")
        return engine
    except Exception as exc:
        logger.error(f"Exc: {exc} while trying to create sqlalchemy engine")
        raise exc


def load_to_postgres(table_name: str, dataframe: pd.DataFrame) -> (int, str):
    """Load a dataframe to a Postgres table.

    Args:
        table_name (str): The name of the table.
        dataframe (pd.DataFrame): The dataframe to load.

    Returns:
        (int, str): The number of rows loaded and any errors.
    """
    stg_exc = None
    count = 0
    try:
        engine = create_sqlalchemy_engine()
        insp = inspect(engine)
        if not insp.has_table(f"{table_name}", schema="public"):
            raise Exception(f"Table {table_name} not present in Postgres")
        logger.info(f"Insertion into source layer for {table_name} started")
        count = dataframe.to_sql(
            table_name,
            engine,
            # schema="public",
            if_exists="append",
            index=False,
        )
        if not count:
            count = 0
        logger.info(f"{count} rows inserted into stg layer for {table_name}")
    except sqla_exc.DBAPIError as excep:
        logger.error(
            f"DBInterface error while trying to insert into postgres source layer"
        )
        logger.error(excep)
        stg_exc = str(excep)[:150] + " in load_to_postgres()"
    except Exception as exc:
        logger.error(f"Exc: {exc} while trying to insert into postgres source layer")
        stg_exc = str(exc)[:150] + " in load_to_postgres()"

    return count, stg_exc


ROOT_DIR = Path(SCRIPTS_DIR).parent.absolute()
FILES_DIR = Path(ROOT_DIR).parent.absolute()
products_path = os.path.join(FILES_DIR, "SourceFiles", "products.csv")
transactions_path = os.path.join(FILES_DIR, "SourceFiles", "transactions.csv")

products_df = pd.read_csv(products_path)
products_df.columns = map(str.lower, products_df.columns)
transactions_df = pd.read_csv(transactions_path)
transactions_df.columns = map(str.lower, transactions_df.columns)

setup_rdbms()
load_to_postgres("products", products_df)
load_to_postgres("transactions", transactions_df)
