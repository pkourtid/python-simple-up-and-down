# Written by Panagiotis Kourtidis

import pygame
from pygame.locals import *
from pygame import mixer
from pygame import freetype
from os import listdir
from os.path import isfile, isdir, join
import xml.etree.ElementTree
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
strGamesFolder = "games"
lstDirectories = [f for f in listdir(strGamesFolder) if isdir(join(strGamesFolder, f))]

# =============================================================================

# =============================================================================
# Game variables
# =============================================================================

# Load resources

dicResources = {}
dicResources["imgTitle"] = pygame.image.load("graphics/title.png")
dicResources["imgCursorArrowRed"] = pygame.image.load("graphics/cursor_arrow_red.png")

dicFont = {}
dicFont["0"] = pygame.image.load("graphics/fonts/0.png")
dicFont["1"] = pygame.image.load("graphics/fonts/1.png")
dicFont["2"] = pygame.image.load("graphics/fonts/2.png")
dicFont["3"] = pygame.image.load("graphics/fonts/3.png")
dicFont["4"] = pygame.image.load("graphics/fonts/4.png")
dicFont["5"] = pygame.image.load("graphics/fonts/5.png")
dicFont["6"] = pygame.image.load("graphics/fonts/6.png")
dicFont["7"] = pygame.image.load("graphics/fonts/7.png")
dicFont["8"] = pygame.image.load("graphics/fonts/8.png")
dicFont["9"] = pygame.image.load("graphics/fonts/9.png")
dicFont["A"] = pygame.image.load("graphics/fonts/A.png")
dicFont["B"] = pygame.image.load("graphics/fonts/B.png")
dicFont["C"] = pygame.image.load("graphics/fonts/C.png")
dicFont["D"] = pygame.image.load("graphics/fonts/D.png")
dicFont["E"] = pygame.image.load("graphics/fonts/E.png")
dicFont["F"] = pygame.image.load("graphics/fonts/F.png")
dicFont["G"] = pygame.image.load("graphics/fonts/G.png")
dicFont["H"] = pygame.image.load("graphics/fonts/H.png")
dicFont["I"] = pygame.image.load("graphics/fonts/I.png")
dicFont["J"] = pygame.image.load("graphics/fonts/J.png")
dicFont["K"] = pygame.image.load("graphics/fonts/K.png")
dicFont["L"] = pygame.image.load("graphics/fonts/L.png")
dicFont["M"] = pygame.image.load("graphics/fonts/M.png")
dicFont["N"] = pygame.image.load("graphics/fonts/N.png")
dicFont["O"] = pygame.image.load("graphics/fonts/O.png")
dicFont["P"] = pygame.image.load("graphics/fonts/P.png")
dicFont["Q"] = pygame.image.load("graphics/fonts/Q.png")
dicFont["R"] = pygame.image.load("graphics/fonts/R.png")
dicFont["S"] = pygame.image.load("graphics/fonts/S.png")
dicFont["T"] = pygame.image.load("graphics/fonts/T.png")
dicFont["U"] = pygame.image.load("graphics/fonts/U.png")
dicFont["V"] = pygame.image.load("graphics/fonts/V.png")
dicFont["W"] = pygame.image.load("graphics/fonts/W.png")
dicFont["X"] = pygame.image.load("graphics/fonts/X.png")
dicFont["Y"] = pygame.image.load("graphics/fonts/Y.png")
dicFont["Z"] = pygame.image.load("graphics/fonts/Z.png")

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


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Create a function to draw a sentence

def drawSentence(strSentence, intOffsetX, intOffsetY, intWidth, intHeight):
    # Iterate through all characters
    for i in range( len(strSentence) ):
        if strSentence[i] in dicFont:
            # screen.blit(imgObject, (100,100))
            imgObjectResized = pygame.transform.scale(dicFont[strSentence[i]], (intWidth*decScaleGame,intHeight*decScaleGame))
            screen.blit(imgObjectResized, (decOffsetWidth + (intOffsetX*decScaleGame) + (((intWidth*decScaleGame))*i), decOffsetHeight + (intOffsetY*decScaleGame)))
            



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Create a function to load the configuration of a game

def loadConfig(strConfig):
	print("Loading Game Config...")
	
	# Load the configuration tree
	xmlTree = xml.etree.ElementTree.parse(strConfig)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Create a function to load new game

def loadGame(strSelectedGame):
    global intGameState, intGameWidth, intGameHeight, dicResources
    # Load the board
    dicResources["imgBoard"] = pygame.image.load("games/"+strSelectedGame+"/board.png")
    dicResources["imgPlayer1"] = pygame.image.load("games/"+strSelectedGame+"/player_1.png")
    dicResources["imgPlayer2"] = pygame.image.load("games/"+strSelectedGame+"/player_2.png")
    dicResources["imgPlayer3"] = pygame.image.load("games/"+strSelectedGame+"/player_3.png")
    dicResources["imgPlayer4"] = pygame.image.load("games/"+strSelectedGame+"/player_4.png")
    dicResources["imgPlayer5"] = pygame.image.load("games/"+strSelectedGame+"/player_5.png")
    dicResources["imgPlayer6"] = pygame.image.load("games/"+strSelectedGame+"/player_6.png")
    dicResources["imgPlayer7"] = pygame.image.load("games/"+strSelectedGame+"/player_7.png")
    intGameWidth = dicResources["imgBoard"].get_width()
    intGameHeight = dicResources["imgBoard"].get_height()
    resize_display()
    intGameState = 1
    

# =============================================================================
# Starting the game loop
# =============================================================================

blnRunning = True
resize_display()

intGameState = 0

pygame.mouse.set_visible(False)
# loadGame("ladders")


while blnRunning:
	
	# Clear the Screen
	screen.fill(black)
	
	# Check the game state
	
	# **************************
	# Ready to play the game
	
	if (intGameState == 0):
		
		# Menu that allows you to load a game
		drawImage(dicResources["imgTitle"], 0, 0, 250, 40)        
		drawSentence("CREATE GAME STEPS", 100, 100, 10, 10)
	
	elif (intGameState == 1):
		drawImage(dicResources["imgTitle"], 0, 0, 250, 40)      
		drawImage(dicResources["imgBoard"], 0, 0, dicResources["imgBoard"].get_width(), dicResources["imgBoard"].get_height())
		drawImage(dicResources["imgPlayer1"], 160, 160, 10, 10)
	
	# drawImage(dicResources["imgCursorArrowRed"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 10, 10) 
	screen.blit(dicResources["imgCursorArrowRed"], pygame.mouse.get_pos())
	
	for event in pygame.event.get():
		if event.type == QUIT:
			blnRunning = False            
		elif event.type == VIDEORESIZE:
			resize_display()
		
	pygame.display.update()
	
pygame.quit()

        
