import random
import numpy as np


def r_p(array):
    """
    按权重 概率性地挑选，权重为0的项不可能被挑选
    :param array: 一维数组
    :return: 挑选的索引
    """
    sum_array = int(sum(array))
    if sum_array != 0:
        p = random.randint(1, sum_array)
        sum_p = 0
        for i, x in enumerate(array):
            sum_p += x
            if sum_p >= p:
                return i
    else:
        return random.randint(0, len(array)-1)


def r_p_test():
    """
    对r_p方法进行10000次测试，结果是否满足概率比
    :return:
    """
    a = np.array([0, 1, 2, 3])
    b = np.zeros_like(a)
    print(b)
    for i in range(10000):
        b[r_p(a)] += 1
    print(b)


def transfer(color, alpha):
    """
    透明度越大越亮
    :param color: basic颜色值
    :param alpha: 透明度
    :return:
    """
    r,g,b = color
    return (r*alpha, g*alpha, b*alpha)


if __name__ == '__main__':
    r_p_test()