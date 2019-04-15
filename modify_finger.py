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
print ("Enter your id :")
enroll_id = input()
name = raw_input("enter your name : ")
try:
    print('Waiting for finger....')
    
    while (f.readImage()== False ):
        pass

    f.convertImage(0x01)

    print('Remove Finger....')
    time.sleep(2)

    print('Waiting for the same finger....')

    while (f.readImage()==False):
        pass
    
    f.convertImage(0x02)
    
    if ( f.compareCharacteristics() == 0 ):
        raise Exception('Fingers do not match')

    characterics1 = f.downloadCharacteristics(0x01)
    #print(characterics1)
    characterics2 = f.downloadCharacteristics(0x02)
    #print(characterics2)
    
    f.createTemplate()
    
    characterics3 = f.downloadCharacteristics(0x01)
    print('*'*200)
    print(characterics3)
    mydict = {"_id": enroll_id, "name": name, "finger_array": characterics3 }
    x = mycol.insert_one(mydict)

     
    myquery = { "_id": 1 }
    mydoc = mycol.find(myquery)
    for x in mydoc:
        match_char = x["finger_array"] 

    print match_char

    f.uploadCharacteristics(0x02, characteristicsData=match_char )
    character4=f.downloadCharacteristics(0x02)
    print character4
    if (character4 == match_char):
        print("finger match")
except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
