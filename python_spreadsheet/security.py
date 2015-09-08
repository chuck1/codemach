import os
import struct
import md5

def strhex(s):
    return " ".join("{:02x}".format(ord(c)) for c in s)

class InvalidUsr(Exception):
    pass
class InvalidPwd(Exception):
    pass

def encrypt(p):
    tok1 = 'abc'
    tok2 = '123'
    m = md5.new(tok1 + p + tok2)
    d = m.digest()
    print "encrypt len",len(d)
    return d

def decode_pwd_file():
    print "decode"
    fn = os.path.join(os.path.dirname(__file__),'data','pwd.txt')
    with open(fn, 'rb') as f:
        buf = f.read()
   
    dic = {}

    while True:
        try:
            u,d = struct.unpack_from("16s16s", buf)
            
            buf = buf[32:]
            
            print "u",repr(u)
            print strhex(d)
            
            dic[u]=d
        except:
            print "eof"
            break
    
    return dic

def check_pwd(u,p):

    u = u.ljust(16)[0:16]

    dic = decode_pwd_file()

    d = encrypt(p)

    if u in dic.keys():
        if d == dic[u]:
            pass
        else:
            print strhex(dic[u])
            print strhex(d)
            raise InvalidPwd()
    else:
        raise InvalidUsr()

def create_usr(u,p):
    u = u.ljust(16)[0:16]
    d = encrypt(p)

    fn = os.path.join(os.path.dirname(__file__),'data','pwd.txt')
    
    print "saving u",u
    print strhex(d)
    
    with open(fn, 'ab') as f:
        f.write(struct.pack("16s16s",u,d))




