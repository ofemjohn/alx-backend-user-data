#!/usr/bin/env python3
'''auth route that handles authentications'''
import bcrypt


def _hash_password(password: str) -> bytes:
    '''method hashes password using bycrypt'''
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password
