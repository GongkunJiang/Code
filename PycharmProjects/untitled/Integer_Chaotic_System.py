"""
    Author: Dell
    Time: 2019/11/28 19:57
"""
import struct
from shutil import copyfile
import os
from multiprocessing import Process
import random


def xor(s1, s2):
    result = ''
    for i in range(len(s1)):
        if s1[i] == s2[i]:
            result += '0'
        else:
            result += '1'
    return result


def m(m1, m2):
    product = m1 * m2
    binary = bin(product)[2:]
    if len(binary) < 2 * precision:
        binary = '0' * (2 * precision - len(binary)) + binary
    retain = binary[-precision:]
    abandon = binary[:-precision]
    result = xor(retain, abandon)
    return int(result, 2)


def func(x):
    return m(x, domain - x)


def TestU01(x, piece):
    length = [2 ** 20, 2 ** 25, 2 ** 30]
    path = [r'./TestU01_%d_220.bin' % piece,
            r'./TestU01_%d_225.bin' % piece,
            r'./TestU01_%d_230.bin' % piece, ]
    wrote = 0
    if os.path.exists(path[0]):
        os.remove(path[0])
    for i in range(100):
        x = func(x)
    for amount in range(3):
        with open(path[amount], 'ab+') as f:
            while wrote < length[amount]:
                # if wrote % 1000000 == 0:
                #     print('Test\t', int((length[amount] - wrote) / 1000000))
                x = func(x)
                # string = '0' * (precision - len(bin(x)[2:])) + bin(x)[2:]
                cs = CA_substitute(x)
                string = '0' * (precision - len(bin(cs)[2:])) + bin(cs)[2:]
                y = string[-piece:]
                for n in range(int(piece / 8)):
                    f.write(struct.pack('B', int(y[n * 8:(n + 1) * 8], 2)))
                    wrote += 8
        print("Test\t第%d个文件写入完成！！！" % (amount + 1))
        if amount < 2:
            copyfile(path[amount], path[amount + 1])


def NIST(x, piece):
    length = 10 ** 9
    path = r'./NIST_%d.txt' % piece
    wrote = 0
    if os.path.exists(path):
        os.remove(path)
    for i in range(100):
        x = func(x)
    with open(path, 'a') as f:
        while wrote < length:
            # if wrote % 1000000 == 0:
            #     print('NIST\t', int((length - wrote) / 1000000))
            x = func(x)
            # string = '0' * (precision - len(bin(x)[2:])) + bin(x)[2:]
            cs = CA_substitute(x)
            string = '0' * (precision - len(bin(cs)[2:])) + bin(cs)[2:]
            f.write(string[-piece:])
            wrote += piece
    print("NIST写入完成！！！")


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


def CA_substitute(x):
    b = '0' * (precision - len(bin(x)[2:])) + bin(x)[2:]
    new_b = ''
    for i in range(precision):
        key = b[i - 1] + b[i] + b[(i + 1) % len(b)]
        new_b += rule[key]
    return int(new_b, 2)


precision = 64
domain = 2 ** precision
x = random.randint(1, domain)
piece = 56
rule = CA_rule(154)
if __name__ == '__main__':
    p1 = Process(target=TestU01, args=(x, piece))
    p2 = Process(target=NIST, args=(x, piece))
    p1.start()
    p2.start()
    p1.join()
    p2.join()