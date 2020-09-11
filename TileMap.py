import pygame, LevelHandler, math
from Tile import *
from StockBox import *
from Counter import *
from Trash import *
from DeliveryTable import *
from ChoppingBoard import *


tms = []

class TileMap:
    def __init__(self, screen, size, level):
        self.screen = screen
        self.size = size
        self.tiles = []
        self.level = level
        self.loadingMap = False
        self.buildMap()
        tms.append(self)
        
    def _distanceCheck(self, tile, player, tolerance=160):
        deltaX = tile.rect.x - player.rect.x
        deltaY = tile.rect.y - player.rect.y
        distance = math.sqrt(math.pow(deltaX,2) + math.pow(deltaY,2))
        if (distance <= tolerance):
            return True
        else:
            return False
        

    def buildMap(self):
        mapData = LevelHandler.loadMapFile(self.level)
        mapList = LevelHandler.parseMap(mapData)
        tileData = LevelHandler.parseData(mapData)
        try:
            stockTypes = LevelHandler.getStockBoxes(tileData)
        except:
            stockTypes = []
        boxCount = 0
        y = -1
        for line in mapList:
            x=-1
            y+=1
            for char in line:
                x+=1
                if char == "v":
                    self.tiles.append(Tile((x*80,y*80), "Images/Tiles/stove_front.png", True, False))
                if char == "s":
                    try:
                        food = stockTypes[boxCount]
                    except:
                        food = None
                    self.tiles.append(StockBox((x*80,y*80), food, True))
                    boxCount += 1
                if char == "#":
                    try:
                        top = mapList[y-1][x]
                        bottom = mapList[y+1][x]
                        left = mapList[y][x-1]
                        right = mapList[y][x+1]
                    except:
                        pass
                    if y == 0 and x != 0 and x!= 11:
                        self.tiles.append(Counter((x*80,y*80), None,"Images/Tiles/counter_front.png"))
                    elif x == 0 and y != 0:
                        self.tiles.append(Counter((x*80,y*80), None,"Images/Tiles/counter_side_left.png"))
                    elif x == 11 and y!= 0:
                        self.tiles.append(Counter((x*80,y*80), None,"Images/Tiles/counter_side_right.png"))
                    elif x == 0 and y == 0:
                        self.tiles.append(Counter((x*80,y*80), None,"Images/Tiles/counter_corner_tl.png"))
                    else:
                        self.tiles.append(Counter((x*80,y*80), None,"Images/Tiles/counter_top.png"))

                if char == "t":
                    self.tiles.append(Trash((x*80,y*80)))
                if char == "d":
                    self.tiles.append(DeliveryTable((x*80,y*80), None))
                if char == "c":
                    self.tiles.append(ChoppingBoard((x*80,y*80), None))
                if char == "-":
                    self.tiles.append(Tile((x*80,y*80), "Images/Tiles/floor.png"))
                    
    def _renderTile(self, tile, player):
        canRender = self._distanceCheck(tile, player)
        if not (canRender):
            return
        self.screen.blit(tile.image, tile.rect)
        item = None
        try:
            item = tile.holding
        except:
            pass
        if item:
            item.update(tile)
    def render(self, playerList):
        for tile in self.tiles:
            for player in playerList:
                self._renderTile(tile, player)
                
    def purge(self):
        self.tiles = []
        self.screen.fill((0,0,0))
        self.buildMap()
                
    def warmup(self):
        for tile in self.tiles:
            self.screen.blit(tile.image, tile.rect)
            item = None
            try:
                item = tile.holding
            except:
                pass
            if item:
                item.update(tile)
