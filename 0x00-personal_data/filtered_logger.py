#!/usr/bin/env python3
'''Personal data for pid
'''
import mysql.connector
import logging
import os
from typing import List
import re

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_data(fields: List[str], redaction: str, message: str,
                separator: str) -> str:
    '''filter data'''
    for field in fields:
        message = re.sub(rf"{field}=(.*?)\{separator}",
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ RedactingFormatter class. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Init """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Format """
        return filter_data(self.fields, self.REDACTION,
                           super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    '''get logger'''

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''connect to mysqldb'''
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    if not password or not username or not host or not db_name:
        logging.error("Missing environment variables")
        return None
    con = mysql.connector.connect(
        host=host,
        database=db_name,
        user=username,
        password=password)
    return con


def main() -> None:
    """ Implement a main function
    """
    db = get_db()
    if not db:
        return
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
            f"ssn={row[3]}; password={row[4]};ip={row[5]}; " +\
            f"last_login={row[6]}; user_agent={row[7]};"
        print(message)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
