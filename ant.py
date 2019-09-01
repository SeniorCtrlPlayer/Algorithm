# -*- coding:utf-8 -*-
import sys, math, copy
import pygame
from pygame.locals import QUIT, KEYDOWN
import numpy as np
import random
from tools import r_p, transfer, index_tot_delta


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
            pygame.draw.rect(self.screen, transfer(self.rect_color, max(1 - (map[x][y] / 255), 0)),
                             (x * win.d1, y * win.d1, self.d, self.d), 0)


class Ant:

    def __init__(self, i, j, live, info_d, a_color=(224, 224, 224)):
        """
        蚂蚁类
        :param i: 虚拟横坐标
        :param j: 虚拟纵坐标
        :param live: 最大生命数，每走一格损失一条生命
        :param a_color: 蚂蚁颜色
        """
        self.maxlive = live
        self.live = live
        self.info_d = info_d
        self.x = i
        self.y = j
        self.a_color = a_color
        # 路径表
        self.last = []
        temp = 4
        while temp == 4:
            temp = random.randint(0, 8)
        self.last.append(temp)
        self.flag = False

    def move(self, info):
        if self.flag:
            self.info_d = self.info_d * 100
            # 找到食物，按原路返回
            try:
                next = self.last.pop()
                # print("回家路上",self.x,self.y,next)
            except:
                self.info_d = 20
                self.flag = False
                return None, None
        else:
            if self.live < 0:
                # print("生命值用完")
                return None, None
            # self.x, self.y, last = info.get_next(self.x, self.y, self.last[-1])
            next_list = info.info[self.x:self.x + 3, self.y:self.y + 3].flatten()
            # 禁止选择上一个位置
            last_index = self.last[-1]
            next_list[last_index] = 0
            # 禁止选择当前位置
            next_list[4] = 0
            sum_array = sum(next_list)
            next = None
            if sum_array != 0:
                if random.randint(1, self.maxlive) < self.maxlive - self.live:
                    next = r_p(next_list, sum_array)
                else:
                    next = last_index
            while next in [4, last_index, None]:
                next = random.randint(0, len(next_list) - 1)
            self.last.append(8 - next)
            # 蚂蚁携带信息素衰变值
            self.live -= self.info_d
        dx, dy = index_tot_delta(next)
        self.x += dx
        self.y += dy
        info.info[self.x + 1, self.y + 1] += self.info_d
        return self.x, self.y


class map:

    def __init__(self, size, info=None):
        self.size = size
        if info is None:
            self.info = np.ones((size, size))
        else:
            self.info = info
        # 解决矩阵边界点没有九宫格的问题
        # (i) of input = (i+1) of info
        self.info = np.pad(self.info, (1, 1), 'constant')
        self.threshold = 25
        """
        得到i,j为中心的九宫格的信息素浓度
        :param i: 中心点x
        :param j: 中心点y
        :return: 下一个点的坐标
        """

    def get_info(self):
        """
        信息素更新
        如果浓度大于threshold，则衰减5%，若小于threshold，则衰减
        :return:
        """
        temp = self.info - self.info // 5
        temp1 = np.select([temp > 0], [temp])
        self.info = np.select([self.info >= self.threshold, self.info > 0],
                              [self.info - self.info // self.threshold, self.info - 1])
        return self.info[1:self.size + 1, 1:self.size + 1]


class Ant_Group:
    def __init__(self, count, basic_ant):
        self.count = count
        self.basic_ant = basic_ant
        self.group = []

    def draw(self, win):
        for ant in self.group:
            pygame.draw.circle(win.screen, ant.a_color, (ant.x * win.d1 + 10, ant.y * win.d1 + 10), 6, 6)
            # info.get_next(ant1)
            x, y = ant.move(info)
            if (x == foodx and y == foody):
                ant.flag = True
                # print("找到食物")
            if x == None:
                # print("找到食物")
                self.group.remove(ant)
                self.group.append(copy.deepcopy(self.basic_ant))


if __name__ == '__main__':
    fps = 2
    clock = pygame.time.Clock()
    win = Window(31, 31, 20, 2)
    maxlive = int(10 * math.sqrt(2)) * 20
    basic_ant = Ant(31 // 2, 31 // 2, maxlive, 20)
    group = Ant_Group(2, basic_ant)

    # i*d1,j*d1
    info = map(31)
    foodx = 25
    foody = 15

    win.refresh_line()
    i = 5
    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()
        if len(group.group) < group.count and i > 0:
            group.group.append(copy.deepcopy(group.basic_ant))
            i = random.randint(3, 9)
        else:
            i -= 1
        # win.refresh()
        win.update(info.get_info())
        # 多只蚂蚁移动
        group.draw(win)

        pygame.draw.rect(win.screen, (224, 0, 0), (foodx * win.d1, foody * win.d1, win.d, win.d))
        clock.tick(fps)
        pygame.display.update()
