from datetime import date, datetime
from base64 import b64encode


def obj_parser(obj):
    """Parse datetime."""
    for key, val in obj.items():
        try:
            obj[key] = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S%z')
        except (TypeError, ValueError):
            pass
    return obj


def json_serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def find_path(src, path):
    """Simple navigation of a hierarchical dict structure using XPATH-like syntax.

    >>> find_path(dict(a=1), 'a')
    1

    >>> find_path(dict(a=1), '')
    {'a': 1}

    >>> find_path(dict(a=None), 'a')


    >>> find_path(dict(a=1), 'b')
    Traceback (most recent call last):
    ...
    KeyError: 'b'

    >>> find_path(dict(a=dict(b=1)), 'a.b')
    1

    >>> find_path(dict(a=dict(b=1)), 'a')
    {'b': 1}

    >>> find_path(dict(a=dict(b=1)), 'a.c')
    Traceback (most recent call last):
    ...
    KeyError: 'c'

    """
    if not path:
        return src
    if isinstance(path, str):
        path = path.split('.')
    return find_path(src[path[0]], path[1:])


def is_valid_path(src, path):
    """
    >>> is_valid_path(dict(a=1), 'a')
    True

    >>> is_valid_path(dict(a=1), '')
    True

    >>> is_valid_path(dict(a=1), None)
    True

    >>> is_valid_path(dict(a=1), 'b')
    False
    """
    try:
        find_path(src, path)
        return True
    except KeyError:
        return False


def owntracks_encrypt(msg, key):
    try:
        from libnacl import crypto_secretbox_KEYBYTES as keylen
        from libnacl.secret import SecretBox as secret
        key = key.encode('utf-8')
        key = key[:keylen]
        key = key.ljust(keylen, b'\0')
        msg = msg.encode('utf-8')
        ciphertext = secret(key).encrypt(msg)
        ciphertext = b64encode(ciphertext)
        ciphertext = ciphertext.decode('ascii')
        return ciphertext
    except ImportError:
        exit('libnacl missing')
    except OSError:
        exit('libsodium missing')