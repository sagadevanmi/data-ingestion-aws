import pandas as pd
from constants import DB_ENDPOINT, DB_NAME, DB_PASS, DB_PORT, DB_USERNAME
from sqlalchemy import Engine, create_engine
from sqlalchemy import exc as sqla_exc
from sqlalchemy import inspect
from utils.log_utils import Logger

logger = Logger().set_logger()


class DbUtils:
    """
    Class for Db Util Functions
    """

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

    @staticmethod
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
            engine = DbUtils.create_sqlalchemy_engine()
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
            logger.error(
                f"Exc: {exc} while trying to insert into postgres source layer"
            )
            stg_exc = str(exc)[:150] + " in load_to_postgres()"

        return count, stg_exc
