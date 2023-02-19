from ..exception import InvalidAttributeError

from .mongo import MongoRepository
from .mysql import MySQLRepository

def get_repository(index_name, repo_type : str, db_passwd):
    if repo_type == 'mysql':
        repo = MySQLRepository(index_name, db_passwd)
    else:
        repo = MongoRepository(index_name)
    return RepositoryWrapper(repo)


class RepositoryWrapper:
    def __init__(self, repo):
        self.db = repo

    def clean(self):
        self.db.clean()

    def insert(self, data):
        if isinstance(data, dict):
            return self.db.insert_one(data)

        if isinstance(data, list):
            return self.db.insert_many(data)

        raise InvalidAttributeError(
            data, 'data of type dict or list expected, got {}'.format(type(data)))
    def update(self, data):
        if isinstance(data, dict):
            return self.db.update_one(data)

        if isinstance(data, list):
            return self.db.update_many(data)
        
        raise InvalidAttributeError(
            data, 'data of type dict or list expected, got {}'.format(type(data)))

    def find(self, query, many=False):
        if many:
            return self.db.find(query)
        else:
            return self.db.find_one(query)
    
    def dump(self):
        """
        get all the database data
        """
        if isinstance(self.db, MySQLRepository):
            sql = "SELECT * FROM " + self.db.name
            self.db.cur.execute(sql)
            result =  self.db.cur.fetchall()
            return list(result)
        else:
            return self.db.find({})
