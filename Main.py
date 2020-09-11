import pygame, TileMap
from ItemHandler import *
from Player import *
from Conveyor import *
from Button import *
from ImageCycler import *
from pygame import mixer as mx
from OrderHandler import *
from EventManager import *


# Window Setup
pygame.init()

EventMgr = EventManager("Core",60)

pygame.mixer.init()
screen = pygame.display.set_mode((1260,720))
screen.fill((0,100,0))
pygame.display.set_caption("Pizza Poppers")
icon = pygame.image.load("Images/icon.png")
pygame.display.set_icon(icon)
screenState = "Title"
paused = False
warmup = False
musicPlaying = False
createItem((200,300),"Chicken")
createItem((250,350),"Beef")
createItem((300,100),"Chicken")

order1 = Order("Complete This Order",("foo","bar"))
pbc = mx.Sound("Sound/PBC.ogg")


# Game Objects
tileMap = TileMap.TileMap(screen, 10,"test.lvl")
plr = Player(5,(100,100),"GenericCharacter.png",1)
bkg = pygame.image.load("Images/Backgrounds/SteelFloor.png")
orders = pygame.image.load("Images/Orders.png")

# Title Screen Objects
play = Button((100,250),"Play")
settings = Button((100,350),"Settings")
exitGame = Button((100,450),"Exit")
secret = Button((463,12),"Secret")

# Settings Screen Objects
settingsBkg = pygame.image.load("Images/Backgrounds/SettingsScreen1.png")
back = Button((75,700),"Back")

# Pause Screen Objects
pauseBkg = pygame.image.load("Images/Backgrounds/PauseScreen1.png")
title = Button((450,300),"MainMenu")
resume = Button((450,500),"Resume")

while True:
    #  Main Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit();
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if screenState == "Play" or screenState == "Pause":
                    paused = not paused
            if event.key == pygame.K_j:
                tileMap.purge()
    
    if screenState == "Play": # Game Window
        if paused:
            screenState = "Pause"
        else:
            if warmup:
                print("warmup")
                tileMap.warmup()
            screen.blit(orders,(960,0))
            tileMap.render([plr])
            plr.get_input()
            plr.render_frame(screen)
            renderItems(screen)
            warmup = False
            
    if screenState == "Title": # Title Screen Window
        screen.fill((0,0,0))
        screen.blit(pygame.image.load("Images/Backgrounds/food3.jpg"), (0,0))
        if play.update():
            screenState = "Play"
            warmup = True
        if exitGame.update():
            exit(); 
        if settings.update():
            back.last = "Title"
            screenState = "Settings"
        if secret.update():
            pbc.play()
        play.render(screen, (10,605))
        settings.render(screen, (430,605))
        exitGame.render(screen,(850,605))
        secret.render(screen)
        
    if screenState == "Pause": # Paused Screen
        screen.blit(pauseBkg, (0,0))
        if not paused:
            screenState = "Play"
        if settings.update():
            screenState = "Settings"
            back.last = "Pause"
        if title.update():
            paused = False
            screenState = "Title"
        if resume.update():
            paused = False
        settings.render(screen, (450,400))
        title.render(screen, (450,300))
        resume.render(screen)
        
    if screenState == "Settings": # Settings Screen
        if back.update():
            screenState = back.last
        screen.blit(settingsBkg,(0,0))
        back.render(screen,(75,600))
        
    
    pygame.display.flip()
    EventMgr.Tick()
