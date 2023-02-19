from imsearch.repository import get_repository
import pymysql
if __name__ == "__main__":
    '''
    repository_db = get_repository('clothes', 'mysql')
    data = {
        "image": "./image.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/d/de/Nokota_Horses_cropped.jpg",
        'feature_index' : -1
    }
    repository_db.insert(data)
    data = {
        "image": "./image2.png",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Koe_in_weiland_bij_Gorssel.JPG/1200px-Koe_in_weiland_bij_Gorssel.JPG",
        'feature_index' : -1
    }
    repository_db.insert(data)
    '''
    repository_db = get_repository('products', 'mysql', '')
    result = repository_db.find({'feature_index' : 3})
    if result != None:
        print(result[6])
    else:
        print('Not found') 
    #result = repository_db.dump()
    #images = [x[6] for x in result]
    #print(images)
    