import colors
import pygame
import math
import time
import numpy as np
from target import *

""" This module draws the radar screen """

pre_angle = 0
targets = {}


class RadarGridVisualizer:
    radarDisplay = None
    radarFont = None
    def __init__(self):
        pygame.init()
        self.radarDisplay = pygame.display.set_mode((1400, 800))
        self.radarFont = pygame.font.Font(pygame.font.get_default_font(), 20)
        pygame.display.set_caption("Radar Screen")

    def draw_grid(self):
        # NOTE: after this call, update always needs to be called
        self.radarDisplay.fill(colors.black)
        pygame.draw.circle(self.radarDisplay, colors.green, (700, 800), 650, 1)
        pygame.draw.circle(self.radarDisplay, colors.green, (700, 800), 550, 1)
        pygame.draw.circle(self.radarDisplay, colors.green, (700, 800), 450, 1)
        pygame.draw.circle(self.radarDisplay, colors.green, (700, 800), 300, 1)
        pygame.draw.circle(self.radarDisplay, colors.green, (700, 800), 150, 1)
        self.radarDisplay.fill(colors.black, [0, 785, 1400, 20])
        # horizental line
        pygame.draw.line(self.radarDisplay, colors.green, (30, 780), (1370, 780), 1)
        # 45 degree line
        pygame.draw.line(self.radarDisplay, colors.green, (700, 780), (205, 285), 1)
        # 90 degree line
        pygame.draw.line(self.radarDisplay, colors.green, (700, 780), (700, 80), 1)
        # 135 degree line
        pygame.draw.line(self.radarDisplay, colors.green, (700, 780), (1195, 285), 1)
        # write the 0 degree
        text = self.radarFont.render("0", 1, colors.green)
        self.radarDisplay.blit(text, (10, 780))
        # write the 45 degree
        text = self.radarFont.render("45", 1, colors.green)
        self.radarDisplay.blit(text, (180, 260))
        # write the 90 degree
        text = self.radarFont.render("90", 1, colors.green)
        self.radarDisplay.blit(text, (690, 55))
        # write the 135 degree
        text = self.radarFont.render("135", 1, colors.green)
        self.radarDisplay.blit(text, (1205, 270))
        # write the 180 degree
        text = self.radarFont.render("180", 1, colors.green)
        self.radarDisplay.blit(text, (1365, 780))

    def draw_line_and_targets(self, angle, distance):
        self.draw_grid()
        a = math.sin(math.radians(angle)) * 800.0
        b = math.cos(math.radians(angle)) * 800.0
        pygame.draw.line(
            self.radarDisplay, colors.green, (700, 780), (700 - int(b), 780 - int(a)), 2
        )

        if distance != -1 and distance < 48 and not distance < 2:
            targets[angle] = Target(angle, distance, colors.red)

        for target in targets.values():
            # calculate the coordinates and the remoteness of the target
            c = math.sin(math.radians(target.angle)) * 800.0
            d = math.cos(math.radians(target.angle)) * 800.0
            # change the scale if the range is changed
            e = math.sin(math.radians(target.angle)) * (700 / 50) * target.distance
            f = math.cos(math.radians(target.angle)) * (700 / 50) * target.distance
            # draw the line indicating the target
            pygame.draw.line(
                self.radarDisplay,
                target.color,
                (700 - int(f), 780 - int(e)),
                (700 - int(d), 780 - int(c)),
                target.width,
            )

            diffTime = time.time() - target.time

            if diffTime >= 0.0 and diffTime <= 0.5:
                target.color = colors.red1L
            elif diffTime > 0.5 and diffTime <= 1:
                target.color = colors.red2L
            elif diffTime > 1.0 and diffTime <= 1.5:
                target.color = colors.red3L
            elif diffTime > 1.5 and diffTime <= 2.0:
                target.color = colors.red4L
            elif diffTime > 2.0 and diffTime <= 2.5:
                target.color = colors.red5L
            elif diffTime > 2.5 and diffTime <= 3.0:
                target.color = colors.red6L
            elif diffTime > 3.0:
                target.width = 0

        pygame.display.update()
