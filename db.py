import pymysql.cursors
import logging



class Database:
    def __init__(self, host, user, password, db):
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=db,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            logging.info('Database connection succeed')
        except Exception as e:
            logging.error(f'Database connection error: {str(e)}')





