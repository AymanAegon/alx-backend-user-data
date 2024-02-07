#!/usr/bin/env python3
"""
0. Regex-ing
"""

from typing import List
import re
import logging
import mysql.connector
import os

PII_FIELDS = ("email", "phone", "ssn", "password", "name")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """init"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format"""
        log = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """gets a logger"""
    logger = logging.getLogger("user_data")
    ch = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    ch.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(ch)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    connection = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST'),
        database=os.getenv('PERSONAL_DATA_DB_NAME'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD')
    )
    return connection


def main():
    """function will obtain a database connection using get_db and
    retrieve all rows in the users table and
    display each row under a filtered format"""
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        name = "name={}; ".format(row[0])
        email = "email={}; ".format(row[1])
        phone = "phone={}; ".format(row[2])
        ssn = "ssn={}; ".format(row[3])
        password = "password={}; ".format(row[4])
        ip = "ip={} ;".format(row[5])
        last_login = "last_login={}; ".format(row[6])
        ua = "user_agent={};".format(row[7])
        message = name + email + phone + ssn + password + ip + last_login + ua
        logger = get_logger()
        logger.info(message)

    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
