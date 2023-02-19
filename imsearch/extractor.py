import os
import sys
import shutil
import base64
import uuid
import json
import time
from tempfile import NamedTemporaryFile
from PIL import Image
import numpy as np
import redis
from io import BytesIO
from . import utils
from .storage import get_storage_object


class FeatureExtractor:
    def __init__(self, index_name):
        self.index_name = index_name
        self.redis_url = os.environ.get('REDIS_URI')
        self._redis_db = redis.StrictRedis.from_url(self.redis_url)
        if os.environ.get('STORAGE_MODE') not in ['local', 'none']:
            self._storage = get_storage_object(os.environ.get('STORAGE_MODE'))
        else:
            self._storage = os.environ.get('STORAGE_MODE')
        os.makedirs(self._get_image_path(self.index_name), exist_ok=True)

    @classmethod
    def _get_image_path(self, index_name):
        #home_dir = os.environ.get('HOME')
        home_dir = os.getcwd()
        return os.path.join(home_dir, '.imsearch', 'images', index_name)

    def _save_image(self, image, _id):
        if self._storage == 'none':
            return ''
        elif self._storage == 'local':
            dst = os.path.join(self._get_image_path(
                self.index_name), '{}.jpg'.format(_id))
            utils.save_image(image, dst)
            return dst
        else:
            with NamedTemporaryFile() as temp:
                dst = "{}.jpg".format(temp.name)
                key = "images/{}/{}.jpg".format(self.index_name, _id)
                utils.save_image(image, dst)
                return self._storage.upload(dst, key)

    def _decode_redis_data(self, data):
        '''
        Description:

        --input: 
            feature got from the redis database
        --output:
            feature after been decoded
        '''
        data = json.loads(data.decode('utf-8'))
        #def _decode(d):
        #    d['features'] = utils.base64_decode(
        #        d['features'], dtype=np.float32)
        #    return d

        #data['primary'] = list(map(_decode, data['primary']))
        #data['secondary'] = utils.base64_decode(data['secondary'], dtype=np.float32)
        #data = utils.base64_decode(data, dtype=np.float32)
        data['feature'] = utils.base64_decode(data['feature'], dtype=np.float32)
        return data

    def clean(self):
        shutil.rmtree(self._get_image_path(self.index_name))
        os.makedirs(self._get_image_path(self.index_name), exist_ok=True)

    def extract(self, image_path, save=True):
        """Send image to the redis db and extract features from image queue in redis database.

        :Parameters:
          - `image_path`: 
          - `save`: 

        :Returns:
           dict:
            - id
            - image
            - url
            - feature
        """
        image = utils.check_load_image(image_path)
    
        if image is None:
            return None
        _id = str(uuid.uuid4())
        data = {
            'id': _id,
            'image': utils.base64_encode(image),
            'shape': image.shape
        }
        self._redis_db.rpush('image_queue', json.dumps(data))

        result = None
        while result is None:
            time.sleep(0.01)
            result = self._redis_db.get(_id)

        result = self._decode_redis_data(result)
        result['id'] = _id
        if save:
            result['image'] = self._save_image(image, _id)

        if 'http' in image_path:
            result['url'] = image_path

        self._redis_db.delete(_id)
        return result

    def _extract(self, image_url : str, save=True):
        """Send image to the redis db and extract features from image queue in redis database.

        :Parameters:
          - `image_url' : 
          - `save`: 

        :Returns:
           dict:
            - id
            - feature
        """
        image = utils.check_load_image(image_url)
        if image is None:
            return None
        _id = image_url
        data = {
            'id': _id,
            'image': utils.base64_encode(image),
            'shape': image.shape
        }
        self._redis_db.rpush('image_queue', json.dumps(data))

        result = None
        while result is None:
            time.sleep(0.01)
            result = self._redis_db.get(_id)

        self._redis_db.delete(_id)
        result = self._decode_redis_data(result)
        
        result['id'] = _id
        '''
        result['image'] = ''
        if save:
            result['image'] = self._save_image(image, _id)
       
        if 'http' in image_info[1]:
            result['url'] = image_info[1]
        '''
        return result

    def extract_from_img(self, image : bytes, save=True):
        """Send image to the redis db and extract features from image queue in redis database.

        :Parameters:
          - `image`: 
          - `save`: 

        :Returns:
          - dict:
            - id
            - image
            - url
            - feature
        """
        image = BytesIO(image)
        image = np.asarray(Image.open(image))
        if image is None:
            return None
        _id = str(uuid.uuid4())
        data = {
            'id': _id,
            'image': utils.base64_encode(image),
            'shape': image.shape
        }
        self._redis_db.rpush('image_queue', json.dumps(data))

        result = None
        while result is None:
            time.sleep(0.01)
            result = self._redis_db.get(_id)

        result = self._decode_redis_data(result)
        result['id'] = _id
        if save:
            result['image'] = self._save_image(image, _id)
        self._redis_db.delete(_id)
        return result
