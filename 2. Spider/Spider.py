import asyncio
import csv
import time
import apiclient
import httplib2
import networkx as nx
import matplotlib.pyplot as plt
import bs4

from oauth2client.service_account import ServiceAccountCredentials
from openpyxl import Workbook

from ForMatrix import calculate_page_rank_item
from managers.SessionManager import SessionManager
from managers.ConnectionManager import ConnectionManager, delete_all_from_db, save_data


def link_normalization(src, protocol, domain):
    a = src
    if src.startswith('//'):
        a = f'{protocol}:{src}'
    if src.startswith('/'):
        a = f'{protocol}://{domain}{src}'
    if src.startswith('#') or src.startswith('.'):
        a = f'{protocol}://{domain}'
    if a.endswith('/'):
        a = a[:-1]
    return a


def find_extensions(link):
    for extension in extensions:
        if not link.find(extension) == -1:
            return True
    return False


async def spider_for_link(link, session):
    try:
        all_links[link] = {}
        length = 0
        protocol, domain = link.split('://')
        domain = domain.split('/')[0]

        response = await session.get(link)

        html = await response.text()
        tree = bs4.BeautifulSoup(html, 'html.parser')
        tags_a = tree.select('a')

        for tag_a in tags_a:
            if 'href' not in tag_a.attrs:
                continue
            a = tag_a.attrs['href']
            a = link_normalization(a, protocol, domain)

            if not find_extensions(a):
                unchecked_links.add(a)

                if a is not None:
                    length += 1
                    if a not in all_links[link]:
                        all_links[link][a] = 1
                    else:
                        all_links[link][a] += 1

        checked_links.add(link)

    except Exception as msg:
        pass


def create_pm_tm_matrices():
    probability_matrix = []
    transitivity_matrix = []

    for link in checked_links:
        counter = 0
        for key in all_links[link]:
            if key in checked_links:
                counter += 1
            if counter == 0:
                dead_ends.add(link)

    row_for_tm = ['link']
    for link in checked_links:
        if link not in dead_ends:
            row_for_tm.append(link)
    transitivity_matrix.append(row_for_tm)

    for link in checked_links:
        if link not in dead_ends:
            row_for_tm = [link]
            row_for_pm = []

            length = 0
            for key in all_links[link]:
                if key in checked_links and link not in dead_ends:
                    length += all_links[link][key]

            for key in checked_links:
                if key not in dead_ends:
                    if key in all_links[link]:
                        row_for_tm.append(1)
                        row_for_pm.append(all_links[link][key] / length)
                    else:
                        row_for_pm.append(0)
                        row_for_tm.append(0)

            transitivity_matrix.append(row_for_tm)
            probability_matrix.append(row_for_pm)

    return probability_matrix, transitivity_matrix


def write_transitivity_matrix_to_csv(transitivity_matrix):
    with open(TRANSITIVITY_MATRIX_FILE, 'w', encoding='utf-8') as csv_file:
        field_names = transitivity_matrix[0]
        writer = csv.DictWriter(csv_file, fieldnames=field_names, delimiter=',', lineterminator='\n')

        writer.writeheader()
        length = len(field_names)

        for row in transitivity_matrix[1:]:
            string = {}

            for i in range(length):
                string[field_names[i]] = row[i]
            writer.writerow(string)


def generate_transitivity_matrix_eval_paper(transitivity_matrix):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']
    )
    http_auth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=http_auth)

    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            'valueInputOption': 'USER_ENTERED',
            'data': [{
                'range': 'A1:ZZZ3000',
                'majorDimension': 'ROWS',
                'values': transitivity_matrix
            }]
        }
    ).execute()


def generate_transitivity_matrix_xlsx():
    wb = Workbook()
    ws = wb.active
    with open(TRANSITIVITY_MATRIX_FILE, 'r', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=","):
            ws.append(row)
    wb.save(XLSX_FILE)


def build_a_graph():
    graph = nx.DiGraph()
    graph.add_nodes_from(checked_links)
    for link in all_links:
        for value in all_links[link].values():
            graph.add_edge(link, value)

    nx.write_gml(graph, 'graph.gml')
    plt.figure(figsize=(30, 30))
    options = {
        'node_color': 'blue',
        'node_size': 12,
        'edge_color': 'grey',
        'width': 0.09,
        'label': True,
    }

    nx.draw_random(graph, **options)
    plt.savefig('graph.png')
    plt.show()


def calculate_page_rank(probability_matrix):
    result = None
    probability_matrix = [
        [x[i] for x in probability_matrix] for i in range(len(probability_matrix[0]))
    ]
    return calculate_page_rank_item(probability_matrix, result)


async def saving_data(connection, page_ranks):
    values = ''
    cl = list(checked_links)
    for i in range(len(page_ranks)):
        value = f'(\'{cl[i]}\', {page_ranks[i][0]})'
        if values == '':
            values = value
        else:
            values += ', ' + value

    if not values == '':
        await save_data(connection, values)


async def main():
    start = time.time()
    depth_now = 0
    count = 0

    connection = await connection_manager.get_connection()
    session = await session_manager.get_session()
    await delete_all_from_db(connection, TABLE)

    while not depth_now == depth:
        depth_now += 1
        co_spiders = list()
        for link in unchecked_links:
            if link not in all_links:
                co_spiders.append(spider_for_link(link, session))

        for spider in asyncio.as_completed(co_spiders):
            count += 1
            await spider

        co_spiders.clear()

    print(f'spiders worked: {time.time() - start}')
    print(f'checked links: {len(checked_links)}')
    all_links_length = 0
    for link in all_links:
        all_links_length += 1
        all_links_length += len(all_links[link])
    print(f'all links: {all_links_length}')
    probability_matrix, transitivity_matrix = create_pm_tm_matrices()
    write_transitivity_matrix_to_csv(transitivity_matrix)
    build_a_graph()
    if depth < 2:
        generate_transitivity_matrix_eval_paper(transitivity_matrix)
    else:
        generate_transitivity_matrix_xlsx()
    page_ranks = calculate_page_rank(probability_matrix)
    await saving_data(connection, page_ranks)

    await session_manager.close_session()
    await connection_manager.close_connection()
    print(f'fully worked: {time.time() - start}')


if __name__ == '__main__':
    CREDENTIALS_FILE = 'creds.json'
    TRANSITIVITY_MATRIX_FILE = 'transitivity_matrix.csv'
    XLSX_FILE = 'excel.xlsx'
    TABLE = 'sites'
    NUMBER_OF_PAGE_RANK_ITERATIONS = 10
    spreadsheet_id = '1pfhhIEnwHDdrGVdy3hicn-xuTEXKudEPNZ3gygPapT8'
    session_manager = SessionManager()
    connection_manager = ConnectionManager()
    depth = 3
    # href = input('ведите начальную ссылку: ')
    href = 'https://ria.ru/20180205/1513977064.html'
    # href = 'https://news.sportbox.ru'
    extensions = ['.jpg', '.png', '.jpeg', '.pdf', '.doc', '.docx', '.exe', '.zip']
    all_links = {}
    checked_links = set()
    unchecked_links = set()
    unchecked_links.add(href)
    dead_ends = set()

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())
