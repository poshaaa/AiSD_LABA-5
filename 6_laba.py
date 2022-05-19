import time
import random
import numpy as np
import matplotlib.pyplot as plt

def print_matrix(M, matr_name, tt):
    print("матрица " + matr_name + " промежуточное время = " + str(format(tt, '0.2f')) + " seconds.")
    for i in M:  # делаем перебор всех строк матрицы
        for j in i:  # перебираем все элементы в строке
            print("%5d" % j, end=' ')
        print()
print("\n-----Результат работы программы-------")
try:
    row_q = int(input("Введите количество строк (столбцов) квадратной матрицы больше 6 : "))
    while row_q < 6 or row_q > 100:
        row_q = int(input("Вы ввели неверное число\nВведите количество строк (столбцов) квадратной матрицы больше 6 :"))
    K = int(input("Введите число К="))
    start = time.time()
    time_next = time.time()
    A = np.zeros((row_q, row_q))
    F = np.zeros((row_q, row_q))
    for i in range(row_q):     #формируем матрицу А
        for j in range(row_q):
            A[i][j] = np.random.randint(-10, 10)
            #A[i][j] = i*10+j
    time_prev = time_next
    time_next = time.time()
    print_matrix(A, "A", time_next - time_prev)
    for i in range(row_q):      #формируем матрицу F, копируя из матрицы А
        for j in range(row_q):
            F[i][j] = A[i][j]
    time_prev = time_next
    time_next = time.time()
    print_matrix(F, "F", time_next - time_prev)

    size = row_q // 2         #размерность подматрицы
    C = np.zeros((size, size))   #формируем матрицу C
    for i in range(size):
        for j in range(size):
            C[i][j] = A[i][j]
    for i in range(0, size):  # формируем подматрицу E
        for j in range(0, size):
            C[i][j] = F[size + i][row_q - size + j]
    time_prev = time_next
    time_next = time.time()
    print_matrix(C, "C", time_next - time_prev)

    summ = 0
    sum_up = 0
    sum_rt = 0
    sum_down = 0
    sum_lt = 0
    point = 0
    for x in range(size):  # обрабатываем подматрицу C и считаем сумму чисел по ее периметру
        for y in range(size):
            if x == 0:
                sum_up += C[0][y]
            if x == size - 1:
                sum_down += C[size - 1][y]
    for x in range(1, size - 1, 1):
        for y in range(size):
            if y == size - 1:
                sum_rt += C[x][size - 1]
            if y == 0:
                sum_lt += C[x][0]

    mult = 1
    mult_rt = 1
    mult_up = 1
    point = 0
    #ищем сумму элементов по диагонали подматрицы С
    for x in range(size - 1, size // 2 - 1, -1):  # считаем диагональ снизу справа
        for y in range(size - 1, size // 2, -1):
            mult_rt *= C[x][-1 - point]
            point += 1
            break
    if size % 2 == 0:  # центр есть - идем по диагонали слева снизу
        point = 1
        for x in range(size // 2, size):
            for y in range(size // 2 - 1, 0 - 1, -1):
                mult_rt *= C[x][size // 2 - point]
                point += 1
                break
    else:  # центра нет - "перепрыгиваем" через него, продолжая идти по диагонали слева вниз
        point = 0
        for x in range(size // 2, size):
            for y in range(size // 2 - 1, 0 - 1, -1):
                mult_rt *= C[x][size // 2 - point]
                point += 1
                break
    # для диагоналей сверху
    point = 0
    for x in range(0, size // 2 - 1):  # считаем диагональ сверху справа
        for y in range(size - 1, size // 2 - 1, -1):
            mult_rt *= C[x][-1 - point]
            point += 1
            break
    if size % 2 == 0:  # центр есть - идем по диагонали слева сверху
        point = 1
        for x in range(size // 2, 0 - 1, -1):
            for y in range(size // 2 - 1, 0 - 1, -1):
                mult_up *= C[x][size // 2 - point]
                point += 1
                break
    else:  # центра нет - "перепрыгиваем" через него, продолжая идти по диагонали слева сверху
        point = 0
        for x in range(size // 2, 0 - 1, -1):
            for y in range(size // 2 - 1, 0 - 1, -1):
                mult_up *= C[x][size // 2 - point]
                point += 1
                break
    if size % 2 == 0:               #если есть центр, то из mult_up убираем центральный элемент, т.к. он уже посчитан
        for x in range(size):
            for y in range(size):
                mult_up /= C[size // 2][size // 2]
                break
            break
    mult = mult_rt + mult_up

    if summ > mult:
        print("Случай 1")
        for i in range(0, size + row_q % 2):  # меняем подматрицы B и C местами симметрично
            for j in range(size + row_q % 2, row_q): # (3, 6)
                F[i][j], F[row_q-i-1][j] = F[row_q-i-1][j], F[i][j]

    else:
        print("Случай 2")
        for i in range(0, size + row_q % 2 - 1):  # меняем подматрицы B и E местами несимметрично
            for j in range(0, size + row_q % 2 - 1, 1):
                F[i][j], F[i][size + row_q % 2 + j] = F[i][size + row_q % 2 + j], F[i][j]

    time_prev = time_next
    time_next = time.time()
    print_matrix(F, "F", time_next - time_prev)

    if np.linalg.det(A) == 0 or np.linalg.det(F) == 0:
        print("A или F вырожденая матрица,т.е вычислить нельзя")
    elif np.linalg.det(A) > sum(F.diagonal()):
        A = ((np.dot(np.linalg.matrix_power(A, -1), np.transpose(A))) - (np.dot(K, np.linalg.matrix_power(F, -1))))
        finish = time.time()
    else:
        A = np.dot((A + np.tril(A) - np.transpose(F)), K)
        finish = time.time()
    time_prev = time_next
    time_next = time.time()
    print_matrix(A, "A", time_next - time_prev)

    time_prev = time_next
    time_next = time.time()
    print_matrix(F, "F", time_next - time_prev)

    plt.title('Examples', fontsize=15)
    plt.xlabel("Number", fontsize=13)
    plt.ylabel("Resalt", fontsize=13)

    #Круговая диаграмма
    for j in range(row_q):
        plt.pie([i for i in range(row_q)])
    plt.show()

    plt.title('Examples', fontsize=15)
    plt.xlabel("Number", fontsize=13)
    plt.ylabel("Resalt", fontsize=13)

    #Стем-график
    for j in range(row_q):
        plt.stem([i for i in range(row_q)], A[j][::])
    plt.show()

    #Рассеивание (мозайка)
    fig, ax = plt.subplots()
    ax.matshow(A)
    plt.show()

    print(f"Programm time {time.time()-start}")

except ValueError:
    print("\nЭто не число")
