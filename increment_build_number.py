#!/usr/bin/env python3
import os
import re
import sys

def inc_build(folder='.'):
    
    s = open(os.path.join(folder, 'VERSION.txt')).read()
    
    pat = re.compile('(\d+\.\d+[ab])(\d+)')
    
    m = pat.match(s)
    
    if not m:
        print('error in version string: ',repr(s))
        sys.exit(1)
    
    bn = int(m.group(2))
    s2 = m.group(1) + str(bn+1)

    print('old version = '+s)
    print('new version = '+s2)

    open(os.path.join(folder, 'VERSION.txt'),'wb').write(s2.encode())

if __name__=='__main__':

    if len(sys.argv) == 2:
        inc_build(sys.argv[1])
        sys.exit(0)

    inc_build()
    inc_build('myexecutor_pkg')
    inc_build('mysocket_pkg')
    inc_build('storage_pkg')
    inc_build('sheets_pkg')
    inc_build('sheets_backend_pkg')
    sys.exit(0)

