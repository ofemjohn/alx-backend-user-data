#!/usr/bin/env python3
'''regex to replace occurences'''
import re


def filter_datum(fields, redaction, message, separator):
    '''compile a regex'''
    pattern = re.compile('|'.join(fields))
    return pattern.sub(redaction, message)
