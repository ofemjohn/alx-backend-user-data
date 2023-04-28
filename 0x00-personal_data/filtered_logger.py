#!/usr/bin/env python3
'''perdonla data source'''
import logging
from typing import List
from os import environ
import mysql.connector
import re

PII_FIELDS = ("name", "email", "phone", "ssn", "password")

REDACTION = "***"
FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
SEPARATOR = ";"


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''regex pattern'''
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    '''return logger information'''
    logg_er = logging.getLogger("user_data")
    logg_er.setLevel(logging.INFO)
    logg_er.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logg_er.addHandler(stream_handler)

    return logg_er


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''connect to mydal database'''
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    conn = mysql.connector.connection.MySQLConnection(user=username,
                                                      password=password,
                                                      host=host,
                                                      database=db_name)
    return conn


class RedactingFormatter(logging.Formatter):
    '''redacting '''

    def __init__(self, fields: List[str]):
        '''init'''
        super(RedactingFormatter, self).__init__(FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''formating'''
        record.msg = filter_datum(self.fields, REDACTION,
                                  record.getMessage(), SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def main():
    '''the main program'''
    db = None  # Initialize db to None
    cursor = None  # Initialize cursor to None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users;")
        field_names = [i[0] for i in cursor.description]

        logger = get_logger()

        for row in cursor:
            str_row = ''.join(
                f'{f}={str(r)}; ' for r, f in zip(
                    row, field_names))
            logger.info(str_row.strip())

    except mysql.connector.Error as err:
        logging.error(f'Error connecting to database: {err}')
    finally:
        if cursor is not None:  # Check if cursor is not None
            cursor.close()
        if db is not None:  # Check if db is not None
            db.close()


if __name__ == '__main__':
    main()
