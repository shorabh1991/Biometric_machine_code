#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pymongo
from pyfingerprint.pyfingerprint import PyFingerprint


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["finger_DB"]
mycol = mydb["finger_array"]

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

try:
    print('Waiting for finger....')
    
    while (f.readImage()== False ):
        pass

    f.convertImage(0x01)

    for x in range(1,2):
        time.sleep(0.2)
        myquery = { "_id": x }
        mydoc = mycol.find(myquery)
        for y in mydoc:
            match_char = y["finger_array"] 
        f.uploadCharacteristics(0x02, characteristicsData=match_char )
        if ( f.compareCharacteristics() != 0 ):
            print ("finger_found")
            print(y["name"])
            break

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)