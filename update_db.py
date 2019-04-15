#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib
import pymongo
from pyfingerprint.pyfingerprint import PyFingerprint

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)


if (f.getTemplateCount() > 0):
    print ("Memory is not fully empty! please format the memory ")
    exit(1)

print ("Updating Database . . . . . . . . ")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["finger_DB"]
mycol = mydb["finger_array"]

for x in range(1,5):
        myquery = { "_id": x }
        mydoc = mycol.find(myquery)
        for y in mydoc:
            match_char = y["finger_array"] 
        f.uploadCharacteristics(0x01, characteristicsData = match_char )

        positionNumber = f.getTemplateCount()
        if ( f.storeTemplate(positionNumber) == True ):
            print("Finger enrolled successfully!")
            print("New template position #" + str(positionNumber))
        
