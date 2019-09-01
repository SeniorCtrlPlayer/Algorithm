import random
import numpy as np


def r_p(array, sum):
    """
    按权重 概率性地挑选，权重为0的项不可能被挑选
    :param array: 一维数组
    :return: 挑选的索引
    """
    # 有信息素，也有百分之20的概率随机挑选
    p = random.randint(1, sum)
    sum_p = 0
    for i, x in enumerate(array):
        sum_p += x
        if sum_p >= p:
            return i


def r_p_test():
    """
    对r_p方法进行10000次测试，结果是否满足概率比
    :return:
    """
    a = np.array([0, 1, 2, 4])
    b = np.zeros_like(a)
    print(b)
    for i in range(10000):
        b[r_p(a, 7)] += 1
    print(b)


def transfer(color, alpha):
    """
    透明度越大越亮
    :param color: basic颜色值
    :param alpha: 透明度
    :return:
    """
    r, g, b = color
    return (r * alpha, g * alpha, b * alpha)


def index_tot_delta(index):
    """
    [0 1 2]
    [3 4 5]
    [6 7 8]
    当左上角为(0,0)时
        x = index % 3
        y = index // 3
    当中心点为(0,0)时
        x = index % 3 - 1
        y = index // 3 - 1
    """
    dx = index % 3 - 1
    dy = index // 3 - 1
    return dx, dy


def index_tot_delta_test():
    for i in range(9):
        print(i, ": ", index_tot_delta(i))


if __name__ == '__main__':
    r_p_test()
    # index_tot_delta_test()
