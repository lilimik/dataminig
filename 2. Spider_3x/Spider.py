import asyncio
import re


def link_normalization(src, protocol, domain):
    if src.startswith(protocol):
        return src
    if src.startswith('//'):
        return f'{protocol}{src}'
    if src.startswith('/'):
        return f'{protocol}{domain}{src}'


async def spider_for_link(link):

    if link in all_links:
        return

    

    protocol, domain = link.split(':')
    protocol = f'{protocol}:'


if __name__ == '__main__':
    # input('ведите начальную ссылку: ')
    href = 'https://ria.ru/20180205/1513977064.html'
    href_pattern = re.compile(r'^(http://|https://)')
    extensions = ['jpg', 'png', 'jpeg']
    all_links = []

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(spider_for_link(href))
