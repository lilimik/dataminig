from pprint import pprint
import numpy as np


b = 0.85

# for me
# A = np.matrix([
#     [0, 0.2, 1, 0.5, 0],
#     [0, 0.2, 0, 0, 0],
#     [0.5, 0.2, 0, 0, 0],
#     [0, 0.2, 0, 0, 0],
#     [0.5, 0.2, 0, 0.5, 1],
# ])

# for Sabina
A = np.matrix([
    [0.5, 0.33, 0.5, 0.5, 0.5],
    [0, 0.33, 0, 0, 0],
    [0.5, 0, 0, 0, 0.5],
    [0, 0, 0, 0, 0],
    [0, 0.33, 0.5, 0.5, 0],
])

V0 = np.matrix('0.2; 0.2; 0.2; 0.2; 0.2')

e = np.matrix('0.03; 0.03; 0.03; 0.03; 0.03')


def multiple_matrix(B):
    return b * A.dot(B) + e


if __name__ == '__main__':
    num = int(input('введите кол-во итераций: '))
    result = V0

    for i in range(num):
        result = multiple_matrix(result)
        print(f'матрица на {i + 1} итерации')
        pprint(result)
        print()
