import codecs
import base64


def str2bytes(string):
    return bytearray(string, 'utf8')

def hex2bytes(hexin):
    return bytearray.fromhex(hexin)

def base642bytes(base64in):
    return base64.b64decode(base64in.encode('utf-8'))

def bytes2str(bytesin):
    return bytesin.decode("utf8", errors='replace')
    
def bytes2hex(bytesin):
    return codecs.encode(bytesin, encoding='hex')

def bytes2base64(bytesin):
    return codecs.encode(bytesin, encoding='base64')