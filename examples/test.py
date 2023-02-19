# importing module
#from pymongo import MongoClient
    
# Connect with the portnumber and host
#client = MongoClient('mongodb://localhost:27017/')
  
# Access database
#mydatabase = client["test_database"]
  
# Access collection of the database
#mycollection=mydatabase["my_collection"]
  
# dictionary to be added in the database
#mydict = { "name": "John", "address": "Highway 37" }

#x = mycollection.insert_one(mydict)
  
#print(x.inserted_id)

#import redis
#r = redis.Redis()
#r.set('foo', 'bar')
#value = r.get('foo')
#print(value)
#import glob
#import os
#all_images = glob.glob(os.path.join(
#        os.path.dirname(__file__), '..', 'images/*.jpg'))
#print(all_images)



#print(os.path.join(".",".imsearch",'tmp', "{}.pkl".format(str(uuid.uuid4()))))
"""
path = os.path.join(".",".imsearch",'indices',"test" ,"index.h5")
print(path)
isExist = os.path.exists(path)
print(isExist)
print(os.listdir())
"""

import cv2
import glob
import os
import sys

import imsearch

def load_from_db(name, passwd):
    # Initialize the index
    index = imsearch.init(name, passwd)

    # Clear the index and data if any exists
    index.cleanIndex()
    index.loadFromDB()
    index.createIndex()
    return index
 
def show_results(similar, qImage):
    qImage = imsearch.utils.check_load_image(qImage)
    qImage = cv2.cvtColor(qImage, cv2.COLOR_RGB2BGR)
    cv2.imshow('qImage', qImage)
    for _i, _s in similar:
        rImage = cv2.imread(_i['image'])
        print([x['name'] for x in _i['primary']])
        print(_s)
        cv2.imshow('rImage', rImage)
        cv2.waitKey(0)


if __name__ == "__main__":
    index = load_from_db(name='products', passwd='')    
    img_url = 'https://nationaltoday.com/wp-content/uploads/2020/12/National-Horse-Day-1.jpg'
    #index.addImage('https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/African_buffalo_%28Syncerus_caffer_caffer%29_male_with_cattle_egret.jpg/1200px-African_buffalo_%28Syncerus_caffer_caffer%29_male_with_cattle_egret.jpg')
    similar = index.knnQuery(image_path=img_url, k=10, policy='global')
    for obj, distance in similar:
        if obj != None:
            print(obj[6])
        else:
            print('Not found')
  
  

