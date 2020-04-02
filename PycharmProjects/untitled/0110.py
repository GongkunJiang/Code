"""
    Author: Dell
    Time: 2019/11/28 19:57
"""
import struct
from shutil import copyfile
import os
from multiprocessing import Process
import random
import matplotlib.pyplot as plt

"""
与一维元胞自动机结合的伪随机数生成器
"""


def xor(s1, s2):
    result = ''
    for i in range(len(s1)):
        if s1[i] == s2[i]:
            result += '0'
        else:
            result += '1'
    return result


def m(m1, m2, precision):
    product = m1 * m2
    binary = bin(product)[2:]
    if len(binary) < 2 * precision:
        binary = '0' * (2 * precision - len(binary)) + binary
    retain = binary[-precision:]
    abandon = binary[:-precision]
    result = xor(retain, abandon)
    return int(result, 2)


def func(x, precision, domain):
    return m(x, domain - x, precision)


def TestU01(No, rule, piece, precision, domain, x):
    length = [2 ** 20, 2 ** 25, 2 ** 30]
    path = [r'D:/TyiDrive/Manuscripts2/Data/TestU01_%d_%d_220.bin' % (piece, No),
            r'D:/TyiDrive/Manuscripts2/Data/TestU01_%d_%d_225.bin' % (piece, No),
            r'D:/TyiDrive/Manuscripts2/Data/TestU01_%d_%d_230.bin' % (piece, No)]
    wrote = 0
    if os.path.exists(path[0]):
        os.remove(path[0])
    for i in range(100):
        x = func(x, precision, domain)
    for amount in range(3):
        with open(path[amount], 'ab+') as f:
            while wrote < length[amount]:
                # if wrote % 1000000 == 0:
                #     print('Test\t', int((length[amount] - wrote) / 1000000))
                x = func(x, precision, domain)
                # string = '0' * (precision - len(bin(x)[2:])) + bin(x)[2:]
                cs = CA_substitute(x, precision, rule)
                string = '0' * (precision - len(bin(cs)[2:])) + bin(cs)[2:]
                y = string[-piece:]
                for n in range(int(piece / 8)):
                    f.write(struct.pack('B', int(y[n * 8:(n + 1) * 8], 2)))
                    wrote += 8
        print("Test\t第%d个文件写入完成！！！" % (amount + 1))
        if amount < 2:
            copyfile(path[amount], path[amount + 1])


def NIST(No, rule, piece, precision, domain, x):
    length = 10 ** 9
    path = r'D:/TyiDrive/Manuscripts2/Data/NIST_%d_%d.txt' % (piece, No)
    wrote = 0
    if os.path.exists(path):
        os.remove(path)
    for i in range(100):
        x = func(x, precision, domain)
    with open(path, 'a') as f:
        print("NIST\t写入开始！！！")
        while wrote < length:
            # if wrote % 1000000 == 0:
            #     print('NIST\t', int((length - wrote) / 1000000))
            x = func(x, precision, domain)
            # string = '0' * (precision - len(bin(x)[2:])) + bin(x)[2:]
            cs = CA_substitute(x, precision, rule)
            string = '0' * (precision - len(bin(cs)[2:])) + bin(cs)[2:]
            f.write(string[-piece:])
            wrote += piece
    print("NIST\t写入完成！！！")


def CA_rule(No):
    rule = bin(No)[2:]
    if len(rule) < 8:
        rule = '0' * (8 - len(rule)) + rule
    dic = {}
    for i in range(8):
        index = bin(i)[2:]
        if len(index) < 3:
            index = '0' * (3 - len(index)) + index
        dic[index] = rule[i]
    return dic


def CA_substitute(x, precision, rule):
    b = '0' * (precision - len(bin(x)[2:])) + bin(x)[2:]
    new_b = ''
    for i in range(precision):
        key = b[i - 1] + b[i] + b[(i + 1) % len(b)]
        new_b += rule[key]
    return int(new_b, 2)


if __name__ == '__main__':
    No = 240
    rule = CA_rule(No)
    piece = 64  # 每一个数保留的位数
    precision = 64
    domain = 2 ** precision
    x = random.randint(1, domain)
    print(x, '0' * (precision - len(bin(x)[2:])) + bin(x)[2:])
    p1 = Process(target=TestU01, args=(No, rule, piece, precision, domain, x))
    p2 = Process(target=NIST, args=(No, rule, piece, precision, domain, x))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # precision = 64
    # domain = 2 ** precision
    # x = random.randint(1, domain)
    # print(x, '0' * (precision - len(bin(x)[2:])) + bin(x)[2:])
    # list_s = []
    # list_n = []
    # for n in range(50000):
    #     print(n)
    #     x = func(x, precision, domain)
    #     list_s.append(x)
    #     list_n.append(n)
    # plt.scatter(list_n, list_s, marker=',', s=1, linewidths=0.1, c='b')
    # plt.xlabel('n', fontsize='16')
    # plt.ylabel(r"$x_n$", fontsize='16')
    # plt.xlim(0, 50000)
    # plt.ylim(0, )
    # plt.show()
