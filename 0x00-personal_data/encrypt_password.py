#!/usr/bin/env python3
'''Using Bcript for password encryptions'''
import bcrypt
import logging

logging.basicConfig(level=logging.INFO)


def hash_password(password: str) -> bytes:
    '''hashes a password'''
    try:
        encoded_password = password.encode()
        hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
        logging.info("Password successfully hashed")
        return hashed_password
    except Exception as e:
        logging.error("Error hashing password: %s", e)


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''checks if password and the hashed password corresponds'''
    valid = False
    try:
        encoded_password = password.encode()
        if bcrypt.checkpw(encoded_password, hashed_password):
            valid = True
            logging.info("Password is valid")
        else:
            logging.warning("Password is invalid")
    except Exception as e:
        logging.error("Error validating password: %s", e)
    return valid
