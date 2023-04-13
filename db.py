import logging
import aiomysql


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
