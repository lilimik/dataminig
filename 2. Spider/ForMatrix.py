

def matrix_multiplication(first_matrix, second_matrix):
    m = len(first_matrix)
    n = len(second_matrix)
    k = len(second_matrix[0])
    c = [[None for __ in range(k)] for __ in range(m)]

    for i in range(m):
        for j in range(k):
            c[i][j] = sum(first_matrix[i][kk] * second_matrix[kk][j] for kk in range(n))
    return c


def get_unit_vector(length):
    e = []
    for i in range(length):
        e.append([1])
    return e


def get_initial_vector(length):
    v = []
    for i in range(length):
        v.append([1 / length])
    return v


def matrix_multiplication_by_number(num, matrix):
    m = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[0])):
            row.append(matrix[i][j] * num)
        m.append(row)
    return m


def matrix_addition(first_matrix, second_matrix):
    m = len(first_matrix)
    k = len(second_matrix[0])
    c = [[None for __ in range(k)] for __ in range(m)]

    for i in range(m):
        for j in range(k):
            c[i][j] = first_matrix[i][j] + second_matrix[i][j]
    return c


def calculate_page_rank_item(matrix, result):
    b = 0.85
    length = len(matrix)
    e = get_unit_vector(length)
    if result is None:
        v = get_initial_vector(length)
    else:
        v = result
    additional_vector = matrix_multiplication_by_number((1 - b) / length, e)

    result = matrix_multiplication_by_number(b, matrix)
    result = matrix_multiplication(result, v)
    result = matrix_addition(result, additional_vector)
    return result
