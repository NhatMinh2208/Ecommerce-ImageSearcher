from .config import config_init
from .index import Index
from .backend import run


def init(name='index', db_passwd = 'root', **config):
    config_init(config)
    return Index(name=name, db_passwd=db_passwd)


def init_from_file(file_path, name=None, **config):
    config_init(config)
    return Index.loadFromFile(file_path, name=name)


def run_detector(redis_url):
    run(redis_url)
