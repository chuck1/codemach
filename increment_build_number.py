#!/usr/bin/env python3

import re
import sys

def inc_build():
    
    s = open('VERSION.txt').read()
    
    pat = re.compile('(\d+\.\d+[ab])(\d+)')
    
    m = pat.match(s)
    
    if not m:
        print('error in version string')
        sys.exit(1)
    
    bn = int(m.group(2))
    s2 = m.group(1) + str(bn+1)

    print('old version = '+s)
    print('new version = '+s2)

    open('VERSION.txt','wb').write(s2.encode())

if __name__=='__main__':
    inc_build()
    sys.exit(0)

