import asyncpg


class ConnectionManager:

    def __init__(self):
        self.conn = None

    async def get_conn(self):
        self.conn = await asyncpg.connect(
            database="postgres",
            user="postgres",
            password="081011235813MiXaIl",
            host="db-course.ccjvz2nfguyj.us-east-1.rds.amazonaws.com",
            port="5432"
        )
        return self.conn

    async def get_connection(self):
        if self.conn is None:
            self.conn = await self.get_conn()
        return self.conn

    async def close_connection(self):
        await self.conn.close()


async def delete_all_from_db(conn, table):
    await conn.execute(f'delete from {table} where 1 = 1;')


async def save_data(conn, values):
    query = f'INSERT INTO sites (url, page_rank)  values {values};'

    try:
        await conn.execute(query)
    except Exception as msg:
        print(msg)
