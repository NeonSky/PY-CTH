import pygame as pg
from random import randint

from BlockMap import BlockMap
from HighScore import HighScore
from Shape import Shape
from Block import Block

class GameManager:

    isGameOver = False

    def __init__(self):
        print("Game starting...")
        #self.high_score = HighScore()
        self.blockMap = BlockMap()
        self.smurf_shape = None
        self.spawn_shape()

    def spawn_shape(self):
        self.currentShape = Shape((0, 0), Shape.types[randint(0, len(Shape.types)-2)], self.blockMap)

    def update(self):
        if self.isGameOver:
            self.update_it_smurf()

            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                self.isGameOver = False
                self.blockMap.empty_map()
                self.smurf_shape = None
                self.spawn_shape()
        else:
            self.update_cur_shape()
            if self.blockMap.isGameOver():
                self.show_gameover()

    fallTime = 30
    fallTimer = 0
    def update_cur_shape(self):
        if self.fallTimer >= self.fallTime:
            self.fallTimer = 0

            if not self.blockMap.collides(self.currentShape, 0, Block.width):
                keys = pg.key.get_pressed()

                # move sideways
                if keys[pg.K_RIGHT]:
                    self.currentShape.move((1, 0))
                elif keys[pg.K_LEFT]:
                    self.currentShape.move((-1, 0))

                # rotate
                if keys[pg.K_UP]:
                    self.currentShape.rotate(True)
                # elif keys[pg.K_DOWN]:
                #    self.currentShape.rotate(False)

                # fall
                if keys[pg.K_DOWN]:
                    self.fallTime = 10
                else:
                    self.fallTime = 30
                self.currentShape.fall()
            else:
                self.blockMap.applyShape(self.currentShape)
                self.spawn_shape()

        else:
            self.fallTimer += 1

    smurfFlipTime = 30
    smurfFlipTimer = 0
    def update_it_smurf(self):
        if self.smurfFlipTimer >= self.smurfFlipTime:
            self.smurfFlipTimer = 0
            self.smurf_shape.vertical_flip()
            self.smurf_shape.horizontal_flip()
        else:
            self.smurfFlipTimer += 1

    def show_gameover(self):
        self.isGameOver = True
        self.currentShape = None
        self.blockMap.empty_map()
        self.smurf_shape = Shape((0, 0), 'SMURF', self.blockMap)

    def draw(self, screen):
        self.blockMap.draw(screen)
        if self.isGameOver:
            self.smurf_shape.draw(screen)
        else:
            self.currentShape.draw(screen)