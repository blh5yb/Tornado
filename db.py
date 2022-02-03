import MySQLdb
import logging
import json
import os
import sys

logger = logging.getLogger(__name__)


class ConnectingSQL:
    def __init__(self):
        """
        Connect to SQL MySQL DB using credentials from db_config.json
        """
        try:
            with open(f'db_config.json', 'r') as f:
                config_file = f.read()
                config_dict = json.loads(config_file)

        except Exception as e:
            logger.error(f"Error opening db config file: {e}")

        try:
            self.conn = MySQLdb.connect(
                user=config_dict["user"],
                password=config_dict["password"],
                host=config_dict["host"],
            )
            self.cur = self.conn.cursor()

        except Exception as e:
            logger.error(f"Error connecting to sql db: {e}")

    def execute(self, query, db):
        """
        Execute the psql query

        Parameters
        ----------
        query
            sql query
        db
            database to use

        """
        try:
            self.cur.execute(f"USE {db}")
            self.cur.execute(query)
            logger.info("Successfully executed sql query")

        except Exception as e:
            logger.error(f"Error executing sql query: {e}")

    def commit(self):
        """Commit write/ update queries"""
        try:
            self.conn.commit()
            logger.info(f"Update committed to db")

        except Exception as e:
            logger.error(f"Error updating db: {e}")

    def fetch(self):
        """
        Fetch record from db

        Returns
        -------
        MySQL record
        """
        try:
            record = self.cur.fetchall()
            logger.info("Successfully fetched record from db")
            return record

        except Exception as e:
            logger.error(f"Error fetching record from db: {e}")

    def close(self):
        """close database connection"""
        self.cur.close()
        self.conn.close()
