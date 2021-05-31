import random
import time
from pprint import pprint


def generate_itemsets() -> list:
    itemsets = list()
    products_list_length = len(products)
    for _ in range(itemsets_count):
        itemset_products_count = random.randint(1, itemset_products_max_count)
        frequent_itemset = set()

        for _ in range(itemset_products_count):
            random_product_count = random.randint(0, products_list_length - 1)
            frequent_itemset.add(products[random_product_count])

        itemsets.append(frequent_itemset)
    return itemsets


def generate_enumerated_products() -> dict:
    enumerated_products = dict()
    count = 0
    for product in products:
        enumerated_products[product] = count
        count += 1
    return enumerated_products


def generate_product_counts(itemsets) -> dict:
    product_counts = dict()

    for itemset in itemsets:
        for product in itemset:
            if product in product_counts:
                product_counts[product] += 1
            else:
                product_counts[product] = 1
    return product_counts


def generate_groups_of_doubletons(itemsets, enumerated_products) -> dict:
    groups_of_doubletons = dict()
    for count, itemset in enumerate(itemsets):
        groups_of_doubletons[count] = set()
        products_list_by_itemset = list(itemset)
        itemset_slice = 0
        for product1 in products_list_by_itemset:
            itemset_slice += 1

            if product1 == products_list_by_itemset[-1]:
                continue

            for product2 in products_list_by_itemset[itemset_slice:]:
                groups_of_doubletons[count].add((enumerated_products[product1], enumerated_products[product2]))
    return groups_of_doubletons


def generate_hash_buckets_by_groups_of_doubletons(pass_number, product_counts_length, groups_of_doubletons) -> dict:
    hash_buckets = dict()

    for i in range(product_counts_length):
        hash_buckets[i] = dict()

    for number_group_of_doubletons in groups_of_doubletons:
        for doubleton in groups_of_doubletons[number_group_of_doubletons]:
            hash_bucket = (doubleton[0] + pass_number * doubleton[1]) % product_counts_length
            if doubleton not in hash_buckets[hash_bucket]:
                hash_buckets[hash_bucket][doubleton] = 1
            else:
                hash_buckets[hash_bucket][doubleton] += 1
    return hash_buckets


def checking_hash_buckets_for_support(hash_buckets):
    for hash_bucket in hash_buckets:
        quantity = 0
        for value in hash_buckets[hash_bucket].values():
            quantity += value
        if quantity < support:
            hash_buckets[hash_bucket].clear()


def get_not_in_psy_products_nums(product_counts, enumerated_products) -> set:
    not_in_psy_products = set()

    for product in product_counts:
        if product_counts[product] < support:
            not_in_psy_products.add(enumerated_products[product])

    return not_in_psy_products


def get_hash_buckets(product_counts, groups_of_doubletons) -> list:
    pass_number = 1
    hash_buckets1 = generate_hash_buckets_by_groups_of_doubletons(pass_number,
                                                                  len(product_counts),
                                                                  groups_of_doubletons)
    checking_hash_buckets_for_support(hash_buckets1)

    pass_number += 1
    hash_buckets2 = generate_hash_buckets_by_groups_of_doubletons(pass_number,
                                                                  len(product_counts),
                                                                  hash_buckets1)
    checking_hash_buckets_for_support(hash_buckets2)

    all_hash_buckets = [hash_buckets1, hash_buckets2]
    return all_hash_buckets


def delete_doubletons_in_not_in_psy_products(all_hash_buckets, not_in_psy_products) -> list:
    frequent_itemsets = list()

    for hash_buckets in all_hash_buckets:
        for hash_bucket in hash_buckets:
            for doubleton in hash_buckets[hash_bucket]:
                doubleton_without_not_in_psy_products_containing = True
                for product in not_in_psy_products:
                    if product in doubleton:
                        doubleton_without_not_in_psy_products_containing = False
                        break
                if doubleton_without_not_in_psy_products_containing:
                    frequent_itemsets.append(doubleton)

    return frequent_itemsets


def main():
    itemsets: list = generate_itemsets()
    enumerated_products = generate_enumerated_products()
    product_counts = generate_product_counts(itemsets)
    not_in_psy_products = get_not_in_psy_products_nums(product_counts, enumerated_products)

    groups_of_doubletons = generate_groups_of_doubletons(itemsets, enumerated_products)

    all_hash_buckets = get_hash_buckets(product_counts, groups_of_doubletons)

    frequent_itemsets = delete_doubletons_in_not_in_psy_products(all_hash_buckets, not_in_psy_products)

    pprint(frequent_itemsets)


if __name__ == '__main__':
    products = ['Картофель',
                'Морковь',
                'Лук',
                'Чеснок',
                'Петрушка',
                'Укроп',
                'Яблоки',
                'бананы',
                'Лимон',
                'Масло сливочное',
                'Кефир',
                'Молоко детское',
                'Сметана',
                'Творог',
                'Сыр',
                'Горчица',
                'Малиновое варенье',
                'Томатная паста',
                'Рыбная консерва',
                'Консервированный горошек',
                'Консервированная кукуруза',
                'Детское питание',
                'Сгущенка',
                'Мед',
                'Яйца',
                'Масло растительное',
                'Соевый соус',
                'Уксус обычный',
                'Баллончик со сливками',
                'Кошачий корм',
                'Фрикадельки',
                'Котлеты',
                'Суповой набор куриный',
                'Суповой набор мясной',
                'Готовый мясной бульон',
                'Готовый куриный бульон',
                'Курица',
                'Куриное филе',
                'Свинина порционная',
                'Сало',
                'Стручковая фасоль',
                'Маргарин',
                'Сливочное масло',
                'смородина',
                'клубника',
                'клюква',
                'грибы',
                'Шпинат',
                'Слоеное тесто',
                'Рыба',
                'Крабовые палочки',
                'Мука пшеничная',
                'Мука ржаная',
                'Дрожжи сухие',
                'Сода',
                'Разрыхлитель теста',
                'Сахар',
                'Сахарная пудра',
                'Желатин',
                'Горький',
                'шоколад',
                'Крахмал',
                'Масло оливковое',
                'Гречка',
                'Перловка',
                'Рис',
                'Овсяные хлопья',
                'Манка',
                'Кукурузная крупа',
                'Макароны спагетти',
                'Макароны спиральки',
                'Горох',
                'Фасоль',
                'Панировочные сухари',
                'Ваниль',
                'Корица',
                'Карри',
                'Черный перец',
                'Красный перец',
                'Соль',
                'Паприка',
                'Куркума',
                'Лавровый лист',
                'Чай ',
                'кофе',
                'Кофе растворимый',
                'Чай черный',
                'Чай зеленый',
                'Чай мятный',
                'Какао порошок',
                'Мешки для мусора',
                'Наполнитель для кошачьего туалета',
                'Пакеты пищевые',
                'Пищевая пленка',
                'Фольга',
                'Бумага для выпечки',
                'Губки для мытья посуды']
    support = 10
    itemsets_count = 100
    itemset_products_max_count = 15

    start = time.time()
    print(start)
    main()
    print(time.time() - start)
