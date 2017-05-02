#!/usr/bin/env python3

import sheets_backend.sockets

def test():

    sheet = sheets_backend.sockets.SheetProxy('0')
    
    print(sheet.set_cell(0,0,'\'hello\''))
    
    print(sheet.get_cell_data())

if __name__ == '__main__':
    test()

