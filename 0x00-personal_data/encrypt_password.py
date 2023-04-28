#!/usr/bin/env python3
'''Using Bcript for password encryptions'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''hashes a password'''
    encoded_password = password.encode()
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''checks if password and the hashed password corresponds'''
    iss_valid = False
    encoded_password = password.encode()
    if bcrypt.checkpw(encoded_password, hashed_password):
        iss_valid = True
    return iss_valid
