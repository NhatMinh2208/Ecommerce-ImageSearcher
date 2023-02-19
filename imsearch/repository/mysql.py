import pymysql

class MySQLRepository:
    def __init__(self, index_name, passwd, database_name = 'imsearch', usr='root', hst = 'localhost'):
        self.conn = pymysql.connect(
            host=hst,
            user=usr, 
            password = passwd,  #env
            db=database_name,
        )
        self.cur = self.conn.cursor()
        self.name = index_name
        #sql = "CREATE TABLE IF NOT EXISTS "+ self.name +" (_id varchar(255),image varchar(255),url varchar(255),feature_index int);"
        #sql = "CREATE TABLE IF NOT EXISTS "+ self.name +" (_id int AUTO_INCREMENT PRIMARY KEY,image varchar(255),url varchar(255),feature_index int);"
        #self.cur.execute(sql)
    def clean(self):
        return
        #self.cur.execute("DROP DATABASE " + self.name)
    def insert_one(self, data : dict):
        """
        :input:

        - _id, image (path), url, feature_index 
        """
        sql = "INSERT INTO " + self.name + " (photoURL, feature_index) VALUES (%s, %s)"
        self.cur.execute(sql, (data['url'], data['feature_index']))
        self.conn.commit()

    def insert_many(self, data : list):
        """
        :input:

        - _id, image (path), url, feature_index 
        """
        for d in data:
            self.insert_one(d)
        

    def find_one(self, query):
        """
        :input:
        
        - index
        """
        sql = "SELECT * FROM " + self.name + " WHERE `feature_index`=%s"
        self.cur.execute(sql, (query['feature_index']))
        result =  self.cur.fetchone()
        return result

    def find(self, query):
        sql = "SELECT * FROM " + self.name + " WHERE `feature_index`=%s"
        self.cur.execute(sql, (query['feature_index']))
        result =  self.cur.fetchall()
        return result

    def update_one(self, data : dict):
        sql = "UPDATE "+ self.name +" SET feature_index = %s WHERE photoURL = %s"
        self.cur.execute(sql, (data['feature_index'] , data['_id']))
        self.conn.commit()

    def update_many(self, data : list):
        for d in data:
            self.update_one(d)
'''

class MySQLRepository:
    def __init__(self, index_name, passwd, database_name = 'imsearch', usr='root', hst = 'localhost'):
        self.conn = pymysql.connect(
            host=hst,
            user=usr, 
            password = passwd,  #env
            db=database_name,
        )
        self.cur = self.conn.cursor()
        self.name = index_name
        #sql = "CREATE TABLE IF NOT EXISTS "+ self.name +" (_id varchar(255),image varchar(255),url varchar(255),feature_index int);"
        sql = "CREATE TABLE IF NOT EXISTS "+ self.name +" (_id int AUTO_INCREMENT PRIMARY KEY,image varchar(255),url varchar(255),feature_index int);"
        self.cur.execute(sql)
    def clean(self):
        self.cur.execute("DROP DATABASE " + self.name)
    def insert_one(self, data : dict):
        """
        :input:

        - _id, image (path), url, feature_index 
        """
        sql = "INSERT INTO " + self.name + " (image, url, feature_index) VALUES (%s, %s, %s)"
        self.cur.execute(sql, (data['image'], data['url'], data['feature_index']))
        self.conn.commit()

    def insert_many(self, data : list):
        """
        :input:

        - _id, image (path), url, feature_index 
        """
        for d in data:
            self.insert_one(d)
        

    def find_one(self, query):
        """
        :input:
        
        - index
        """
        sql = "SELECT * FROM " + self.name + " WHERE `feature_index`=%s"
        self.cur.execute(sql, (query['feature_index']))
        result =  self.cur.fetchone()
        return result

    def find(self, query):
        sql = "SELECT * FROM " + self.name + " WHERE `feature_index`=%s"
        self.cur.execute(sql, (query['feature_index']))
        result =  self.cur.fetchall()
        return result

    def update_one(self, data : dict):
        sql = "UPDATE "+ self.name +" SET feature_index = %s WHERE _id = %s"
        self.cur.execute(sql, (data['feature_index'] , data['_id']))
        self.conn.commit()

    def update_many(self, data : list):
        for d in data:
            self.update_one(d)
'''