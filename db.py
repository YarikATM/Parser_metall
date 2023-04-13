import pymysql.cursors
import logging
import aiomysql


# class Database:
#     def __init__(self, host, user, password, db):
#         try:
#             self.connection = pymysql.connect(
#                 host=host,
#                 user=user,
#                 password=password,
#                 database=db,
#                 cursorclass=pymysql.cursors.DictCursor
#             )
#             self.cursor = self.connection.cursor()
#             logging.info('Database connection succeed')
#         except Exception as e:
#             logging.error(f'Database connection error: {str(e)}')
#
#     def metall_exists(self, name):
#         self.cursor.execute('SELECT name FROM Metall WHERE name = %s', name)
#         res = self.cursor.fetchall()
#         return bool(len(res))
#     def create_metall(self, category, name, price, desc, company, city, img):
#         sql = 'INSERT INTO Metall (category, name, price, `desc`, company, city, img) VALUES (%s, %s, %s, %s, %s, %s, %s)'
#         self.cursor.execute(sql, (category, name, price, desc, company, city, img))
#         self.connection.commit()
#     def update_metall(self, category, name, company, city, price):
#         sql = 'UPDATE Metall SET price = %s WHERE category = %s AND name = %s AND company = %s AND city = %s'
#         self.cursor.execute(sql, (price, category, name, company, city))
#         self.connection.commit()

class Database:

    def __init__(self, loop):
        self.loop = loop
        self.pool = None
        self.conn = None
        self.cursor = None


    async def connect(self, host, port, user, password, db):
        try:
            self.pool = await aiomysql.create_pool(
                host=host,
                port=port,
                user=user,
                password=password,
                db=db,
                loop=self.loop
            )
            logging.info('Database connection succeed')
        except Exception as e:
            logging.error(f'Database connection error: {str(e)}')
        self.conn = await self.pool.acquire()
        self.cursor = await self.conn.cursor()

    async def metal_exist(self, name):
        result = await self.cursor.execute('SELECT name FROM Metall WHERE name = %s', name)
        return bool(result)

    async def update_metal(self, category, name, company, city, price):
        sql = 'UPDATE Metall SET price = %s WHERE category = %s AND name = %s AND company = %s AND city = %s'
        await self.cursor.execute(sql, (price, category, name, company, city))
        await self.conn.commit()

    async def create_metal(self, category, name, price, desc, company, city, img):
        sql = 'INSERT INTO Metall (category, name, price, `desc`, company, city, img)' \
              ' VALUES (%s, %s, %s, %s, %s, %s, %s)'
        await self.cursor.execute(sql, (category, name, price, desc, company, city, img))
        await self.conn.commit()

