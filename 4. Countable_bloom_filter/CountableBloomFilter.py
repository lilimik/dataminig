import hashlib
import os

import bs4
import requests


def get_hashes(word):
    unnecessary_hash_funcs = ('shake_256', 'shake_128')
    hashes = set()
    for hash_func in hashlib.algorithms_guaranteed:
        if hash_func not in unnecessary_hash_funcs:
            if hash_func == 'blake2b':
                dk = hashlib.blake2b()
                dk.update(word.encode(encoding))
                dk = dk.hexdigest()
            elif hash_func == 'blake2s':
                dk = hashlib.blake2s()
                dk.update(word.encode(encoding))
                dk = dk.hexdigest()
            else:
                key_length = None
                iterations_count = 100000
                dk = hashlib.pbkdf2_hmac(
                    hash_name=hash_func,
                    password=word.encode(encoding),
                    salt=salt,
                    iterations=iterations_count,
                    dklen=key_length)
                dk = dk.hex()
            hashes.add(dk)
    return hashes


def get_words_from_site(link):
    words_set = set()
    response = requests.get(link)
    html = response.text

    tree = bs4.BeautifulSoup(html, 'html.parser')
    tags_p = tree.find_all('p')

    for tag_p in tags_p[:10]:
        tag_words = tag_p.text.split()

        for word in tag_words:
            word = word[-1] if word.endswith('.') else word
            words_set.add(word) if not word.isdigit() else None

    return words_set


def get_values_from_hashes(hashes, n):
    values = dict()
    for hash_item in hashes:
        value = int(hash_item, 24) % n
        if value in values:
            values[value] += 1
        else:
            values[value] = 1
    return values


def main(link):
    words_set = get_words_from_site(link)
    m = len(words_set)
    n = int(m * k // LN2)
    cbf = []
    [cbf.append(0) for i in range(n)]
    for word in words_set:
        hashes = get_hashes(word)
        values = get_values_from_hashes(hashes, n)

        for value in values:
            cbf[value] += values[value]

    return n, m, cbf


def to_fixed(num, digits=0):
    return f"{num:.{digits}f}"


def check_false_positive_probability(n, m, cbf):
    check_words = dict()
    words = (
        'публикаций', 'пост', 'соцсеть', 'продвижении', 'фотографиями',
        'бутылка', 'шоколад', 'трактор', 'трансформатор', 'Истерия'
    )
    for word in words:
        hashes = get_hashes(word)
        values = get_values_from_hashes(hashes, n)

        result = True
        for value in values:
            if cbf[value] == 0:
                result = False
                break

        check_words[word] = result

    for checked_word in check_words:
        print(f'{checked_word}: {check_words[checked_word]}')

    false_positive_probability = (1 - e ** -(k * m / n)) ** k
    print(f'length cbf: {len(cbf)}')
    print(f'false_positive_probability: {to_fixed(false_positive_probability, 4)}')


if __name__ == '__main__':
    encoding = 'utf-8'
    link = 'https://elenaevstratova.ru/kak-napisat-interesnyj-post-v-instagram/'
    salt = os.urandom(16)
    p = 0.0001
    k = len(hashlib.algorithms_guaranteed) - 2
    e = 2.71828182846
    LN2 = 0.69314718056

    n, m, cbf = main(link)
    check_false_positive_probability(n, m, cbf)
