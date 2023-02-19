import cv2
import glob
import os
import sys

import imsearch


def create_and_save(name, images, file_path):
    index = imsearch.init(name)
    index.cleanIndex()
    index.addImageBatch(images)
    index.createIndex()
    index.saveIndex(file_path)
    index.cleanIndex()


def load_index(name, file_path):
    index = imsearch.init_from_file(file_path=file_path, name=name)
    index.createIndex()
    return index
def create_index_with_config(name):
    '''
    parameters:
        name: name of the index (unique identifier name)
        MONGO_URI
        REDIS_URI
        DETECTOR_MODE:  select 'local' or 'remote'. 
                        local: detector backend should be running on the same machine
                        remote: Process should not start detector backend
        pass any configuration you want to expose as environment variable. 
    '''
    index = imsearch.init(name=name,
                          MONGO_URI='mongodb://localhost:27017/',
                          REDIS_URI='redis://localhost:6379/0',
                          DETECTOR_MODE='local')


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
    all_images = glob.glob(os.path.join(
        os.path.dirname(__file__), '.', 'clothes_img/*.jpg'))
    #create_and_save('clothes', all_images, 'clothes_index.tar.gz')
    index = load_index('clothes', 'clothes_index.tar.gz')
    
    # query with image URL
    img_url = 'https://media.istockphoto.com/id/186854841/photo/red-trousers.jpg?s=612x612&w=0&k=20&c=bBScYK2HzUz4g_SbsNtiy7-SywnH-k2LYG91Z-9KEsI='
    similar, _ = index.knnQuery(image_path=img_url, k=10, policy='object')
    show_results(similar, img_url)

    # Create index with configuration
    index = create_index_with_config('test')

#https://stackoverflow.com/questions/38948774/python-append-folder-name-to-filenames-in-all-sub-folders
#https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
#all_images = glob.glob(os.path.join(os.path.dirname(__file__), '..', 'images'))

#for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), '.', 'images')):
#    if not files:
 #       continue
 #   prefix = os.path.basename(root)
#    print(prefix)
 #   for f in files:
        #print(os.path.join(root, "{}_{}".format(prefix, f)))

#all_images = glob.glob(os.path.join(
#        os.path.dirname(__file__), '.', 'images/*/*.jpg'))
#print(all_images)
