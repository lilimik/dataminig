import asyncio
import re

import asyncpg
import bs4
import requests

from pprint import pprint


# class ConnManager:
#
#     def __init__(self):
#         self.conn = None
#
#     async def get_conn(self):
#         self.conn = await asyncpg.connect(
#             database="postgres",
#             user="postgres",
#             password="081011235813MiXaIl",
#             host="db-course.ccjvz2nfguyj.us-east-1.rds.amazonaws.com",
#             port="5432"
#         )
#         return self.conn
#
#     async def get_connection(self):
#         return await self.get_conn()
#
#     async def close_connection(self):
#         await self.conn.close()
#
#
# async def delete_all_from_db(conn):
#     await conn.execute("delete from sites where 1 = 1;")
#
#
# async def save_data(conn, values):
#     query = f'INSERT INTO words (data, total) values {values} ON CONFLICT(data) DO UPDATE SET total = words.total + 1;'
#     print(query)
#
#     try:
#         await conn.execute(
#             query
#         )
#     except Exception as msg:
#         print(msg)


def link_normalization(src, protocol, domain):
    if src.startswith(protocol):
        return src
    if src.startswith('//'):
        return f'{protocol}{src}'
    if src.startswith('/'):
        return f'{protocol}{domain}{src}'


def spider(link):

    all_links.append(link)
    protocol, domain = link.split(':')
    response = requests.get(link)
    response.raise_for_status()
    html = response.text
    tree = bs4.BeautifulSoup(html, 'html.parser')
    tags_a = tree.select('a')

    for tag_a in tags_a:
        if 'href' not in tag_a.attrs:
            continue
        a = tag_a.attrs['href']

        all_links.append(a)


if __name__ == "__main__":
    # manager = ConnManager()
    href = 'https://ria.ru/20180205/1513977064.html'
    href_pattern = re.compile(r'^(http://|https://)')
    depth = 3
    extensions = ['jpg', 'png', 'jpeg']
    all_links = []
    spider(href)
    pprint(all_links)
