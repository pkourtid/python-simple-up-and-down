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

class clsGamePosition:
	number = 0
	x = 0
	y = 0
	goto = -1

class clsGamePlayer:
	position = 0
	
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

intFirstDie = 0
intSecondDie = 0

dicGameConfig = {}
dicPlayers = {}

intNumberOfPlayers = 0 # How many people are playing
intCurrentPlayer = 0 # The current players turn
intCurrentTurnState = 0 # Keep track of the steps that must be completed in a turn



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

	global dicGameConfig
	
	print("Loading Game Config...")
	
	# Load the configuration tree
	xmlTree = xml.etree.ElementTree.parse(strConfig)
	xmlRoot = xmlTree.getroot()
	
	# Load the config
	
	intCurrentElement = -1
	for positions in xmlRoot.iter('position'):
		intCurrentElement = intCurrentElement + 1
		dicGameConfig[intCurrentElement] = clsGamePosition()
		for position in positions:
			if position.tag == "number":
				dicGameConfig[intCurrentElement].number = position.text
				#print(position.tag, position.text)
			if position.tag == "x":
				dicGameConfig[intCurrentElement].x = position.text
				#print(position.tag, position.text)
			if position.tag == "y":
				dicGameConfig[intCurrentElement].y = position.text
				#print(position.tag, position.text)
			if position.tag == "rules":
				#print("rules")
				for rules in position:
					if rules.tag == "goto":
						#print(rules.tag, rules.text)
						dicGameConfig[intCurrentElement].goto = rules.text
				
			# Rules
			#
			#	if rules.tag == "rules":
			#	dicGameConfig[intCurrentElement].y = position.text
			#	print(position.tag, position.text)


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
	intGameState = 2

def movePiece(intNumber, intPlayer):
	global dicGameConfig, dicPlayers
	
	print("Looking for number:")
	print(intNumber)
	
	blnFound = False
	
	for intSelectedElement in range(len(dicGameConfig)):
		if dicGameConfig[intSelectedElement].number == str(intNumber):
			blnFound = True
			break
	
	print("Found on index:")
	print(intSelectedElement)
	
	if blnFound == True:
		dicPlayers[intCurrentPlayer].position = intSelectedElement
	# print(intSelectedElement)
	# print(dicGameConfig[intSelectedElement].goto)

def roleDice():
	global intFirstDie, intSecondDie
	
	intFirstDie = random.randint(1, 6)
	intSecondDie = random.randint(1, 6)
	
	print(str(intFirstDie) + ", " + str(intSecondDie));

# =============================================================================
# Starting the game loop
# =============================================================================

blnRunning = True
resize_display()

intGameState = 2

loadGame("ladders")
loadConfig("games/ladders/config.cfg")
# movePiece(4)
roleDice()
roleDice()
roleDice()
roleDice()
roleDice()

# Testing Game Logic
dicPlayers[0] = clsGamePlayer()
dicPlayers[0].position = 0
dicPlayers[1] = clsGamePlayer()
dicPlayers[1].position = 3

intGameState = 5
intNumberOfPlayers = 2
intCurrentPlayer = 0
intCurrentTurnState = 0


while blnRunning:

	# Clear the Screen
	screen.fill(black)
	
	# Check the game state
 
	# **************************
	# Ready to play the game
	
	if (intGameState == 0):
	
		# Menu that allows you to load a game
		drawImage(dicResources["imgTitle"], 0, 0, 250, 40)		
		drawSentence("SELECT GAME", 100, 100, 10, 10)
		drawSentence("CREDITS", 100, 120, 10, 10)
		
	elif (intGameState == 1):
		drawImage(dicResources["imgTitle"], 0, 0, 250, 40)	  
		for x in range(len(lstDirectories)):
			drawSentence(lstDirectories[x].upper(), 100, 100 + (x*12) , 10, 10)
	
	elif (intGameState == 2):
		drawImage(dicResources["imgTitle"], 0, 0, 250, 40)	  
		drawImage(dicResources["imgBoard"], 0, 0, dicResources["imgBoard"].get_width(), dicResources["imgBoard"].get_height())
		drawImage(dicResources["imgPlayer1"], 160, 160, 10, 10)
		recMousePos = pygame.mouse.get_pos()
		drawSentence("X " + str(int(float((recMousePos[0])/decScaleGame)-(decOffsetWidth/decScaleGame))) + " Y " + str(int((float(recMousePos[1])/decScaleGame)-(decOffsetHeight/decScaleGame))), 400, 20, 10, 10)
	
	elif (intGameState == 5):
		drawImage(dicResources["imgTitle"], 0, 0, 250, 40)	
		drawImage(dicResources["imgBoard"], 0, 0, dicResources["imgBoard"].get_width(), dicResources["imgBoard"].get_height())		
		for intPlayers in range(intNumberOfPlayers):
			drawImage(dicResources["imgPlayer"+str(intPlayers+1)], float(dicGameConfig[dicPlayers[intPlayers].position].x)-5, float(dicGameConfig[dicPlayers[intPlayers].position].y)-5, 10, 10)	
		recMousePos = pygame.mouse.get_pos()
		drawSentence("X " + str(int(float((recMousePos[0])/decScaleGame)-(decOffsetWidth/decScaleGame))) + " Y " + str(int((float(recMousePos[1])/decScaleGame)-(decOffsetHeight/decScaleGame))), 400, 20, 10, 10)
	
	
	for event in pygame.event.get():
		if event.type == QUIT:
			blnRunning = False
		elif event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_SPACE):
				if (intGameState == 5):
					if intCurrentTurnState == 0:
						roleDice();
						intCurrentTurnState = 1
					elif intCurrentTurnState == 1:
						movePiece(int(dicGameConfig[dicPlayers[intCurrentPlayer].position].number) + intFirstDie + intSecondDie, intCurrentPlayer)
						intCurrentPlayer = intCurrentPlayer + 1
						if intCurrentPlayer > intNumberOfPlayers - 1:
							intCurrentPlayer = 0
						intCurrentTurnState = 0
		elif event.type == VIDEORESIZE:
			resize_display()
		
	pygame.display.update()
	
pygame.quit()

		
