# -*- coding:utf-8 -*-
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN
import numpy as np
from tools import r_p, transfer


# 分辨率长为 格子数*格子宽度 + 光带数*光带宽度
# 未吃到食物的蚂蚁颜色
# 设信息素浓度为k
# 地点颜色为 0,128,176-k
# 原点颜色 255,165,0
# 食物点颜色 128,128,0
# 分割线色 128,128,128 分割线宽度 2
# width = x_num*d1-interval


class Window:

    def __init__(self, x_num, y_num, d, interval, rect_color=(64, 224, 208)):
        """
        创建笛卡尔坐标系，将点放大成方格
        :param x_num: 横坐标数
        :param y_num: 纵坐标数
        :param d: 每个坐标方格的宽度
        :param interval: 方格间的间隙宽度
        :param rect_color: 方格默认颜色
        :return:
        """
        self.x_num = x_num
        self.y_num = y_num
        self.d = d
        self.interval = interval
        self.d1 = d + interval
        self.bg_color = 64, 64, 64
        self.rect_color = rect_color
        self.width = x_num * self.d1 - self.interval
        self.height = y_num * self.d1 - self.interval
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), depth=0)

    def refresh_line(self):
        # 清空
        self.screen.fill(self.rect_color)

        # 时间复杂度O(n^2)
        # for x in range(0, self.x_num):
        #     for y in range(0, self.y_num):
        #         pygame.draw.rect(self.screen, self.rect_color,
        #                          (x * self.d1, y * self.d1, self.d, self.d), 0)

        # 时间复杂度O(n)
        # for x in range(1,self.x_num):
        #     pygame.draw.rect(self.screen,self.bg_color,(x*self.d1-self.interval,0,self.interval,self.height),0)
        # for y in range(1,self.y_num):
        #     pygame.draw.rect(self.screen,self.bg_color,(0,y*self.d1-self.interval,self.width,self.interval),0)

        # 加减法版
        x = self.d
        while x < self.width:
            pygame.draw.rect(self.screen, self.bg_color, (x, 0, self.interval, self.height), 0)
            x += self.d1
        y = self.d
        while y < self.height:
            pygame.draw.rect(self.screen, self.bg_color, (0, y, self.width, self.interval), 0)
            y += self.d1

    def update(self, map):
        index = np.array(np.where(map >= 0)).T
        for x, y in index:
            pygame.draw.rect(self.screen, transfer(self.rect_color, 1-map[x][y]/208),
                             (x * win.d1, y * win.d1, self.d, self.d), 0)
        pass


class Ant:

    def __init__(self, i, j, live, a_color=(224, 224, 224)):
        """
        蚂蚁类
        :param i: 虚拟横坐标
        :param j: 虚拟纵坐标
        :param live: 最大生命数，每走一格损失一条生命
        :param a_color: 蚂蚁颜色
        """
        self.live = live
        self.x = i
        self.y = j
        self.a_color = a_color

    def move(self):
        pass


class map:

    def __init__(self, size, info=None):
        self.size = size
        if info is not None:
            self.info = np.zeros((size, size))
        self.info = info
        # 解决矩阵边界点没有九宫格的问题
        # (i) of input = (i+1) of info
        self.info = np.pad(self.info, (1, 1), 'constant')

    def get_next(self, i, j):
        """
        得到i,j为中心的九宫格的信息素浓度
        :param i: 中心点x
        :param j: 中心点y
        :return: 下一个点的坐标
        """
        # 因为矩阵大小为(size+1)x(size+1)，所以i,j对应的是map中的i+1，j+1
        next_list = self.info[i:i + 3, j:j + 3].flatten()
        # 禁止选择九宫格中心
        next_list[4] = 0
        next = r_p(next_list)
        """
        [0 1 2]
        [3 4 5]
        [6 7 8]
        当左上角为(0,0)时
            x = index // 3
            y = index % 3
        当中心点为(0,0)时
            x = index // 3 - 1
            y = index % 3 - 1
        """
        x = i + next // 3 - 1
        y = j + next % 3 - 1

        return x, y

    def get_info(self):
        return self.info[1:self.size + 1, 1:self.size + 1]


if __name__ == '__main__':
    fps = 30
    clock = pygame.time.Clock()
    win = Window(31, 31, 20, 2)
    ant1 = Ant(31 // 2, 31 // 2, 31)

    # i*d1,j*d1
    infomap = np.array([int(x * 2 / 1920 * 208) for x in range(31 * 31)]).reshape((31, 31))
    info = map(31, infomap)
    # print(info.info)

    win.refresh_line()
    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()
        # win.refresh()
        win.update(info.get_info())
        pygame.draw.circle(win.screen, ant1.a_color, (ant1.x * win.d1 + 10, ant1.y * win.d1 + 10), 6, 6)
        ant1.x, ant1.y = info.get_next(ant1.x, ant1.y)
        clock.tick(fps)
        pygame.display.update()
