"""
    Author: Administrator
    Time: 2020/1/8 14:56
"""
import random
from multiprocessing import Process
import os
import struct
from shutil import copyfile


def PLM(x):
    if x == 1:
        return x - 1 / (100 * N)
    elif x % (1 / N) == 0:
        return x + 1 / (100 * N)
    elif 0 < x < 1 / N:
        return MU * (N ** 2) * x * (1 / N - x)
    else:
        i = int(x * N)
        if i % 2 == 1:
            return 1 - MU * (N ** 2) * (x - i / N) * ((i + 1) / N - x)
        else:
            return MU * (N ** 2) * (x - i / N) * ((i + 1) / N - x)


def IPLM(y):
    if y == DOMAIN:
        result = (100 * N * y - DOMAIN) / (100 * N)
    elif y % (DOMAIN / N) == 0:
        result = (100 * N * y + DOMAIN) / (100 * N)
    elif 0 < y < (DOMAIN / N):
        result = (N * MU * y * (DOMAIN - N * y)) / DOMAIN
    else:
        i = int(N * y / DOMAIN)
        if i % 2 == 1:
            result = DOMAIN - (MU * (N * y - DOMAIN * i) * (DOMAIN * (i + 1) - N * y)) / DOMAIN
        else:
            result = (MU * (N * y - DOMAIN * i) * (DOMAIN * (i + 1) - N * y)) / DOMAIN
    return int(round(result, 0))


def Optimize(num):
    # half = int(PRECISION / 2)
    # # s = '0' * (PRECISION - len(bin(num)[2:])) + bin(num)[2:]
    # # temp = int(s[32:] + s[:32], 2)
    # temp = (num << half) % DOMAIN + (num >> half)
    # product = num * temp
    product = num * (DOMAIN - num)
    # s = '0' * (PRECISION * 2 - len(bin(product)[2:])) + bin(product)[2:]
    # t = int(s[PRECISION:], 2) ^ int(s[:PRECISION], 2)
    t = int(product >> PRECISION) ^ (((product << PRECISION) % (DOMAIN ** 2)) >> PRECISION)

    b = '0' * (PRECISION - len(bin(t)[2:])) + bin(t)[2:]
    nb = ''
    for i in range(PRECISION):
        key = b[i - 1] + b[i] + b[(i + 1) % len(b)]
        nb += CA_RULE[key]
    return int(nb, 2)


def CA_rule():
    rule = bin(NO)[2:]
    if len(rule) < 8:
        rule = '0' * (8 - len(rule)) + rule
    dic = {}
    for i in range(8):
        index = bin(i)[2:]
        if len(index) < 3:
            index = '0' * (3 - len(index)) + index
        dic[index] = rule[i]
    return dic


def TestU01(x):
    length = [2 ** 20, 2 ** 25, 2 ** 30]
    path = [r'D:/TyiDrive/Manuscripts2/Data/TestU01_%d_220.bin' % NO,
            r'D:/TyiDrive/Manuscripts2/Data/TestU01_%d_225.bin' % NO,
            r'D:/TyiDrive/Manuscripts2/Data/TestU01_%d_230.bin' % NO]
    wrote = 0
    if os.path.exists(path[0]):
        os.remove(path[0])
    for i in range(100):
        x = IPLM(x)
    for amount in range(3):
        with open(path[amount], 'ab+') as f:
            while wrote < length[amount]:
                x = IPLM(x)
                x = Optimize(x)
                s = '0' * (PRECISION - len(bin(x)[2:])) + bin(x)[2:]
                for n in range(int(len(s) / 8)):
                    f.write(struct.pack('B', int(s[n * 8:(n + 1) * 8], 2)))
                    wrote += 8
        print("Test\t第%d个文件写入完成！！！" % (amount + 1))
        if amount < 2:
            copyfile(path[amount], path[amount + 1])


def NIST(x):
    length = 10 ** 9
    path = r'D:/TyiDrive/Manuscripts2/Data/NIST_%d.txt' % NO
    wrote = 0
    if os.path.exists(path):
        os.remove(path)
    for i in range(100):
        x = IPLM(x)
    with open(path, 'a') as f:
        print("NIST\t写入开始！！！")
        while wrote < length:
            x = IPLM(x)
            x = Optimize(x)
            s = '0' * (PRECISION - len(bin(x)[2:])) + bin(x)[2:]
            f.write(s)
            wrote += PRECISION
    print("NIST\t写入完成！！！")


# 参数
NO = 89
MU, N = 4, 64
PRECISION = 64
DOMAIN = 2 ** PRECISION
CA_RULE = CA_rule()
if __name__ == '__main__':
    # y = random.randint(0, DOMAIN)
    # y = 4774528893380519893
    # print(y)
    # while True:
    #     y = IPLM(y)
    #     z = Optimize(y)
    #     if not 0 <= z <= DOMAIN:
    #         break
    #     print(y, z)

    x = random.randint(1, DOMAIN)
    print(x, '0' * (PRECISION - len(bin(x)[2:])) + bin(x)[2:])
    p1 = Process(target=TestU01, args=(x,))
    p2 = Process(target=NIST, args=(x,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
