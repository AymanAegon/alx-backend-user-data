#!/usr/bin/env python3
"""
0. Regex-ing
"""

from typing import List
import re
import logging

PII_FIELDS = ("email", "phone", "ssn", "password", "user_agent")


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
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
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
