# Written by Panagiotis Kourtidis

import pygame
from pygame.locals import *
from pygame import mixer
import random

# =============================================================================
# We need some helper classes

# This simpler timer class will be use to time certain events
# Not super accurate when used within the event loop but good enough
# for simple games like this

class clsSimpleTimer:
    
    def __init__(self):
        self.start_ticks = pygame.time.get_ticks()

    def resetTimer(self):
        self.start_ticks = pygame.time.get_ticks()
    
    def checkTimePassed(self, intMsCheck):
        
        intMsPassed = (int(pygame.time.get_ticks()) - int(self.start_ticks))
        
        if (intMsPassed > intMsCheck):
            return True
        else:
            return False


#
#class clsPlayer:
#map_position = False
#    player_graphic = ""
    
   

# =============================================================================
# Initialize pygame
# =============================================================================

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Simple Up/Down')
screen = pygame.display.set_mode((500, 500), RESIZABLE)
# =============================================================================

# =============================================================================
# Game variables
# =============================================================================

# Load resources

dicResources = {}
dicResources["imgTitle"] = pygame.image.load("graphics/title.png")

# Some sounds for the game
#sndGameOver = pygame.mixer.Sound("sounds/gameover.mp3")

decScaleWidth = 1.0
decScaleHeight = 1.0
decScaleGame = 1.0;
decOffsetWidth = 0.0;
decOffsetHeight = 0.0;

intGameWidth = 400.0
intGameHeight = 400.0
white = (255, 255, 255)
black = (0, 0, 0)

intGameState = 0


# =============================================================================
# Define game functions
# =============================================================================

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# resetGame() resets all variables as needed for the game to restart

def resetGame():
    
    global intGameState
    
    intGameState = 0;


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# When the screen is resized this function is triggered
# We calculate some variables to help up scale and center the whole game 
          
def resize_display():
    
    #calculate the scale to be used and the offset from center
    
    global decScaleWidth, decScaleHeight, decScaleGame, decOffsetWidth, decOffsetHeight
    
    # get the screen size
    x, y = screen.get_size()

    decScaleWidth = float(x) / intGameWidth
    decScaleHeight = float(y) / intGameHeight
    
	# set a few scaling variables
    if (decScaleWidth < decScaleHeight):
        decScaleGame = decScaleWidth
        decOffsetHeight = (y - (intGameHeight*decScaleGame))/2
        decOffsetWidth = 0.0
    else:
        decScaleGame = decScaleHeight;
        decOffsetWidth = (x - (intGameWidth*decScaleGame))/2
        decOffsetHeight = 0.0

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Create a function to draw an image on the canvas honoring the scale

def drawImage(imgObject, intOffsetX, intOffsetY, intWidth, intHeight):
    # screen.blit(imgObject, (100,100))
    imgObjectResized = pygame.transform.scale(imgObject, (intWidth*decScaleGame,intHeight*decScaleGame))
    screen.blit(imgObjectResized, (decOffsetWidth + (intOffsetX*decScaleGame), decOffsetHeight + (intOffsetY*decScaleGame)))


# =============================================================================
# Starting the game loop
# =============================================================================

blnRunning = True
resize_display()

while blnRunning:

    # Clear the Screen
    screen.fill(black)
    
    # Check the game state
 
    # **************************
    # Ready to play the game
    if (intGameState == 0):
                   
        drawImage(dicResources["imgTitle"], 0, 0, 250, 40)
        
    for event in pygame.event.get():
        if event.type == QUIT:
            blnRunning = False            
        elif event.type == VIDEORESIZE:
            resize_display()
        
    pygame.display.update()
    
pygame.quit()

        
