# -*- coding:utf-8 -*-
import pygame, math
from pygame.locals import QUIT,KEYDOWN
import sys
# 分辨率长为 格子数*格子宽度 + 光带数*光带宽度
# 未吃到食物的蚂蚁颜色
# 设信息素浓度为k
# 地点颜色为 0,128,176-k
# 原点颜色 255,165,0
# 食物点颜色 128,128,0
# 分割线色 128,128,128 分割线宽度 2
# width = x_num*d1-interval

class window:

    def __init__(self, x_num, y_num, d, interval, rect_color=(0,128,176)):
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
        self.d1 = d+interval
        self.bg_color = 128,128,128
        self.rect_color = rect_color
        self.width = x_num*self.d1-self.interval
        self.height = y_num*self.d1-self.interval
        pygame.init()
        self.screen = pygame.display.set_mode((self.width,self.height), depth=0)

    def refresh(self):
        self.screen.fill(self.bg_color)

        for x in range(0, self.x_num):
            for y in range(0, self.y_num):
                pygame.draw.rect(self.screen, self.rect_color,
                                 (x * self.d1, y * self.d1, self.d, self.d), 0)


if __name__ == '__main__':
    fps = 36
    fcclock = pygame.time.Clock()
    x = 10
    y = 10
    color=255,255,255
    win = window(30,30,20,2)

    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()
        win.refresh()
        pygame.draw.circle(win.screen,color,(x,y),10,10)
        x += 2
        x = x % win.width
        fcclock.tick(fps)
        pygame.display.update()