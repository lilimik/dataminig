import re
import time
import aiovk
import asyncio
from managers.ConnectionManager import ConnectionManager, delete_all_from_db


async def save_data(conn, values):
    query = f'INSERT INTO words (data, total) values {values} ON CONFLICT(data) DO UPDATE SET total = words.total + 1;'
    print(query)

    try:
        await conn.execute(
            query
        )
    except Exception as msg:
        print(msg)


async def get_posts(owner_id, count, offset):
    posts = await vk_api.wall.get(owner_id=owner_id, count=count, offset=offset, v=5.92)
    return posts


def split_text_from_post(posts):
    items = posts['items']
    dictionary = {}

    for item in items:
        text = item['text']
        words = text.split()

        for word in words:

            if dictionary.get(word):
                dictionary[word] += 1
            else:
                dictionary[word] = 1

    return dictionary


async def saving_data(conn, dictionary):
    values = ''
    for word, count in dictionary.items():
        word = re.sub('\'', '', word)
        string = f'(\'{word}\', {count})'
        if values == '':
            values = string
        else:
            values += ', ' + string

    if values != '':
        await save_data(conn, values)


async def spider():
    start = time.time()
    print(start)
    json = []
    owner_id = None
    count = 100
    offset = 0
    conn = await manager.get_connection()

    if offset == 0:
        await delete_all_from_db(conn, TABLE)

    while not json:
        domain = 'https://vk.com/itis_kfu'
        # domain = input('введите ссылку на группу: ')
        domain = re.match(href_pattern, domain)

        if domain is not None:
            screen_name = domain.group('name')
            json = await vk_api.utils.resolveScreenName(screen_name=screen_name, v=5.92)
            owner_id = json['object_id']

            if json['type'] == 'group':
                owner_id *= -1

    co_posts = list()
    while offset != total:
        co_posts.append(get_posts(owner_id, count, offset))
        offset += count

    for co_post in asyncio.as_completed(co_posts):
        posts = await co_post
        dictionary = split_text_from_post(posts)
        await saving_data(conn, dictionary)

    await manager.close_connection()
    await session.close()
    print(time.time() - start)


if __name__ == "__main__":
    TABLE = 'words'
    token = "ae40397aae40397aae40397a9dae3682b9aae40ae40397ace0bf838aa1fa57fa14979f7"
    session = aiovk.TokenSession(access_token=token)
    vk_api = aiovk.API(session)

    manager = ConnectionManager()
    href_pattern = re.compile(r'https://vk.com/(?P<name>\w+)')
    # total = int(input('Введите кол-во постов (кол-во / 100)'))
    total = 200

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(spider())
