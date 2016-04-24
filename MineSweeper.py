#!/usr/bin/env python2


#
#############################################################################
#Name        : MineSweeper
#Author      : Saket S Komawar
#Description : "MineSweeper"...
#############################################################################
#


#Modules
import pygame, sys, random, time
from pygame import *
from time import *


#Syntactic Sugars
WINDOWHEIGHT = 570
WINDOWWIDTH = 520
BOARDCOLUMNS = 10
BOARDROWS = 10
BOXSIZE = 40
GAP = 1
FPS = 30
ICON = "/home/saket/Codes/Python/MineSweeper/mine.png"
BOMB = "/home/saket/Codes/Python/MineSweeper/bomb.png"
SOUND = "/home/saket/Codes/Python/MineSweeper/bomb.ogg"
FONTSIZE = 20
RUNNING = True
XMARGIN = int((WINDOWWIDTH - (BOARDCOLUMNS * BOXSIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDROWS * BOXSIZE)) - (BOARDCOLUMNS * BOARDROWS))
LEFT = 1
RIGHT = 3


#Colors
#		   R    G    B	
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
GREY1  = (200, 200, 200)
GREY2  = (150, 150, 150)
GREY3  = (225, 225, 225)
GREY4  = (210, 210, 210)
GREEN  = (  0, 180,   0)
BLUE   = (  0,   0, 255)
BROWN  = ( 95,   0,   0) 
RED    = (245,   0,   0)
PURPLE = (205,   0, 205)
YELLOW = (205, 205,   0)


#Elements
BLANK = 0
MINE = -1
COVERED = 10
UNCOVERED = -10
NO_MINES = 18
VISITED = 100
FLAGUP = 1000


#Main Function
def main():
	#Global Declaration
	global DISPLAYSURF, FONTOBJECT, MINESLIST, FPSCLOCKOBJECT, MINEIMG, TIME

	#Start of Pygame
	pygame.init()
	
	#Setting of Main Window
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption("MineSweeper")
	pygame.display.set_icon(pygame.image.load(ICON))

	#Setting FontObject
	FONTOBJECT = pygame.font.Font("freesansbold.ttf", FONTSIZE)

	#Loading MineImage 
	MINEIMG = pygame.image.load(BOMB)

	#Initialize MainBoard
	MainBoard = InitBoard()

	#Mines Initialization
	MINESLIST = []

	#No. of Flags Remaining
	NO_FLAGS = NO_MINES

	#Initializes Time
	TIME = 0.0

	#FpsClockObject
	FPSCLOCKOBJECT = pygame.time.Clock()

	#To Get Best Time
	BestTime = HighestScoreRead()

	#Used to Store x and y coordinates of mouse event
	mousex = 0 
	mousey = 0 

	#FirstClick Flag
	FirstClick_L = False
	FirstClick_R = False

	#GameLoop
	while RUNNING:
		#BackGroundColor
		DISPLAYSURF.fill(GREY3)
		
		#To Draw Restart Button
		pygame.draw.rect(DISPLAYSURF, GREY3, (XMARGIN + 345, YMARGIN + 440, 81, 40))#(X + 360, 15)
		textsurfobj = FONTOBJECT.render("Restart", True, BLACK)
		textrectobj = textsurfobj.get_rect()
		textrectobj.center = (XMARGIN + 385, YMARGIN + 460)#XMARGIN + 199
		DISPLAYSURF.blit(textsurfobj, textrectobj)

		#To Draw Flag and its Count
		pygame.draw.polygon(DISPLAYSURF, RED, ((XMARGIN + 2, 35), (XMARGIN + 12, 25), (XMARGIN + 12, 39)))
		pygame.draw.line(DISPLAYSURF, BLACK, (XMARGIN + 13, 25), (XMARGIN + 13, 45), 2)
		textsurfobj = FONTOBJECT.render(str(NO_FLAGS), True, BLACK)
		textrectobj = textsurfobj.get_rect()
		textrectobj.center = (XMARGIN + 35, 35)
		DISPLAYSURF.blit(textsurfobj, textrectobj)

		#To Draw Best Time Box
		pygame.draw.rect(DISPLAYSURF, WHITE, (XMARGIN + 10, YMARGIN + 440, 80, 40))
		textsurfobj = FONTOBJECT.render("Best:", True, BLACK)
		textrectobj = textsurfobj.get_rect()
		textrectobj.center = (XMARGIN - 20, YMARGIN + 460)#XMARGIN + 199
		DISPLAYSURF.blit(textsurfobj, textrectobj)
		textsurfobj = FONTOBJECT.render("s", True, BLACK)
		textrectobj = textsurfobj.get_rect()
		textrectobj.center = (XMARGIN + 98, YMARGIN + 460)#XMARGIN + 199
		DISPLAYSURF.blit(textsurfobj, textrectobj)
		textsurfobj = FONTOBJECT.render(BestTime, True, BLACK)
		textrectobj = textsurfobj.get_rect()
		textrectobj.center = (XMARGIN + 49, YMARGIN + 460)#XMARGIN + 199
		DISPLAYSURF.blit(textsurfobj, textrectobj)

		#Drawing the Board
		DrawMainBoard(MainBoard)

		#Event Handling Loop
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminator()
			elif event.type == MOUSEBUTTONUP and event.button == LEFT:#Handles Left Click
				mousex, mousey = event.pos
				#Return the Coordinates	of the Clicked Box
				boxx, boxy = GetBoxAtPixel(mousex, mousey)
				#FirstClick Case
				if(boxx != None and boxy != None and FirstClick_L == False):
					if(MainBoard[boxx - 1][boxy - 1][1] != FLAGUP):
						if(FirstClick_R == False):
							START = time()
						MainBoard = ReadyBoard(MainBoard, boxx, boxy) 
						MainBoard = UnCoverBoxes(MainBoard, boxx, boxy)
						FirstClick_L = True
				elif(boxx != None and boxy != None):
					if(MainBoard[boxx - 1][boxy - 1][1] != FLAGUP):
						#To Check the End of the Game
						if(MainBoard[boxx - 1][boxy - 1][0] == MINE):
							PlaySound()
							GameOverWin(MainBoard, 0)
						MainBoard = UnCoverBoxes(MainBoard, boxx, boxy)
				#To Restart	the Game
				RectBox = pygame.Rect(XMARGIN + 345, YMARGIN + 440, 81, 40)
				if RectBox.collidepoint(mousex, mousey):
					main()
			
			elif event.type == MOUSEBUTTONUP and event.button == RIGHT:#Handles Right Click
				if(FirstClick_L == False and FirstClick_R == False):
					START = time()
					FirstClick_R = True
				mousex, mousey = event.pos
				#Return the Coordinates	of the Clicked Box
				boxx, boxy = GetBoxAtPixel(mousex, mousey)
				if(boxx != None and boxy != None):
					if MainBoard[boxx - 1][boxy - 1][1] == COVERED:
						MainBoard[boxx - 1][boxy - 1][1] = FLAGUP
						NO_FLAGS -= 1
					elif MainBoard[boxx - 1][boxy - 1][1] == FLAGUP:
						MainBoard[boxx - 1][boxy - 1][1] = COVERED
						NO_FLAGS += 1

		#Checking the Win
		WinGame(MainBoard)

		#To Print Time-Elapsed
		pygame.draw.rect(DISPLAYSURF, GREY3, (XMARGIN + 360, 15, 81, 40))
		if FirstClick_L == True or FirstClick_R == True:
			TIME = "%.1f" % float(time() - START)
		textsurfobj = FONTOBJECT.render(str(TIME), True, BLACK)
		textrectobj = textsurfobj.get_rect()
		textrectobj.center = (XMARGIN + 400, 35)
		DISPLAYSURF.blit(textsurfobj, textrectobj)
		pygame.display.update()

		#Drawing MainBoard
		DrawMainBoard(MainBoard)
		
		#Updating DisplaySurfaceObject
		pygame.display.update()
		FPSCLOCKOBJECT.tick(FPS)


#Return Top and Left of the Box
def GetTopLeftOfBox(bx, by):
	top = YMARGIN + (by - 1) * (BOXSIZE + GAP) - (GAP * BOARDROWS / 2)
	left = XMARGIN + (bx - 1) * (BOXSIZE + GAP) - (GAP * BOARDCOLUMNS / 2)
	return top, left


#Returns Box [x, y]
def GetBoxAtPixel(mousex, mousey):
	for bx in range(1, BOARDCOLUMNS + 1):
		for by in range(1, BOARDROWS + 1):
			top, left = GetTopLeftOfBox(bx, by)
			RectBox = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
			if RectBox.collidepoint(mousex, mousey):
				return bx, by
	return None, None


#Return a DataStructure with 0 as Initial value and Covered Boxes
def InitBoard():
	board = []
	for i in range(BOARDCOLUMNS):
		tmp = []
		for j in range(BOARDROWS):
			tmp.append([0, COVERED])
		board.append(tmp)
	return board


#Return ReadyBoard after First Click
def ReadyBoard(board, boxx, boxy):
	ShowBoxes = SurroundingBox(boxx, boxy)
	ShowBoxes.append([boxx, boxy])
	n = 0
	while(n < NO_MINES):
		bx = random.randint(1, 999999999) % BOARDCOLUMNS + 1
		by = random.randint(1, 999999999) % BOARDROWS + 1
		if [bx, by] not in ShowBoxes and [bx, by] not in MINESLIST:
			MINESLIST.append([bx, by])
			board[bx - 1][by - 1][0] = MINE
			n += 1
	for i in range(1, BOARDCOLUMNS + 1):
		for j in range(1, BOARDROWS + 1):
			if(board[i - 1][j - 1][0] != MINE):
				count = 0
				surrondboxes = SurroundingBox(i, j)
				for k in range(len(surrondboxes)):
					if(board[surrondboxes[k][0] - 1][surrondboxes[k][1] - 1][0] == MINE):
						count += 1
				board[i - 1][j - 1][0] = count
	return board


#To Uncover the Box(STUD !!! :) 
def UnCoverBoxes(board, boxx, boxy):
	if board[boxx - 1][boxy - 1][1] != FLAGUP:
		board[boxx - 1][boxy - 1][1] = UNCOVERED
	surroundboxes = []
	surroundboxes = SurroundingBox(boxx, boxy)
	surroundboxes.append([boxx, boxy])
	for surround in surroundboxes:
		if(board[surround[0] - 1][surround[1] - 1][0] == 0):
			board[surround[0] - 1][surround[1] - 1][0] = VISITED
			UnCoverSurrondingBoxes(board, surround[0], surround[1])
			UnCoverBoxes(board, surround[0], surround[1])
	return board


#Uncover Complete Surrounding Boxes
def UnCoverSurrondingBoxes(board, boxx, boxy):
	surrondboxes = SurroundingBox(boxx, boxy)
	for surround in surrondboxes:
		if(board[surround[0] - 1][surround[1] - 1][1] != FLAGUP):
			board[surround[0] - 1][surround[1] - 1][1] = UNCOVERED


#Draws Flags
def DrawFlag(board, boxx, boxy):
	top, left = GetTopLeftOfBox(boxx, boxy)
	pygame.draw.rect(DISPLAYSURF, GREY2, (left, top, BOXSIZE, BOXSIZE))
	pygame.draw.polygon(DISPLAYSURF, RED, ((left + 12, top + 20), (left + 22, top + 10), (left + 22, top + 24)))
	pygame.draw.line(DISPLAYSURF, BLACK, (left + 23, top + 10), (left + 23, top + 30), 2)


#To Read HighestScore from a file
def HighestScoreRead():
	output = ".highestscore"
	try:
		ReadFile = open(output)
	except:
		WriteFile = open(output, 'w')
		WriteFile.write("99999")
		return "99999"
	lines = ReadFile.readlines()
	hscore = lines[0][:len(lines[0])]
	return hscore


#To Write HighestScore into a file
def HighestScoreWrite():
	output = ".highestscore"
	try:
		ReadFile = open(output)
	except:
		WriteFile = open(output, 'w')
		BestTime = str(TIME) + '\n'
		WriteFile.write(BestTime)
		return		
	lines = ReadFile.readlines()
	hscore = lines[0][:len(lines[0])]
	if(hscore == '99999' or float(hscore) > float(TIME)):
		WriteFile = open(output, 'w')
		BestTime = str(float(TIME))

		WriteFile.write(TIME)


#Return the MainBoard
def DrawMainBoard(board):
	for i in range(1, BOARDCOLUMNS + 1):
		for j in range(1, BOARDROWS + 1):
			top, left = GetTopLeftOfBox(i, j)
			if(board[i - 1][j - 1][1] == COVERED):
				pygame.draw.rect(DISPLAYSURF, GREY2, (left, top, BOXSIZE, BOXSIZE))
			elif(board[i - 1][j - 1][0] == -1 and board[i - 1][j - 1][1] == UNCOVERED):
				pygame.draw.rect(DISPLAYSURF, GREY1, (left, top, BOXSIZE, BOXSIZE))
				DISPLAYSURF.blit(MINEIMG, (left + 3, top + 3))
			elif(board[i - 1][j - 1][1] == UNCOVERED):
				pygame.draw.rect(DISPLAYSURF, GREY1, (left, top, BOXSIZE, BOXSIZE))
			elif(board[i - 1][j - 1][1] == FLAGUP):
				DrawFlag(board, i, j)
			if(board[i - 1][j - 1][1] == UNCOVERED and board[i - 1][j - 1][0] != -1 and board[i - 1][j - 1][0] != VISITED):
				textsurfobj, textrectobj = MakeText(board[i - 1][j - 1][0], top, left)
				DISPLAYSURF.blit(textsurfobj, textrectobj)
	pygame.display.update()


#Checks Win
def WinGame(board):
	count = 0
	for i in range(1, BOARDCOLUMNS + 1):
		for j in range(1, BOARDROWS + 1):
			if([i, j] not in MINESLIST and board[i - 1][j - 1][1] == UNCOVERED):
				count += 1
	if count == (BOARDCOLUMNS * BOARDROWS - NO_MINES):
		GameOverWin(board, 1)


#Return TextColor
def TextColor(text):
	if(text == 1):
		color = BLUE
	elif(text == 2):
		color = GREEN
	elif(text == 3):
		color = RED
	elif(text == 4):
		color = BROWN
	elif(text == 5):
		color = WHITE
	elif(text == 6):
		color = PURPLE
	else:
		color = YELLOW
	return color


#Return TextSurfObj and TextRectObj
def MakeText(text, top, left):
	color = TextColor(text)
	textsurfobj = FONTOBJECT.render(str(text), True, color)
	textrectobj = textsurfobj.get_rect()
	textrectobj.center = (left + (BOXSIZE / 2), top + (BOXSIZE / 2))
	return textsurfobj, textrectobj


#Return GameOverWin Board
def GameOverWin(board, Flag):
	#To Print Final-Time
	pygame.draw.rect(DISPLAYSURF, GREY3, (XMARGIN + 360, 15, 81, 40))
	if Flag == 0:
		color = RED
	else:
		color = GREEN
	textsurfobj = FONTOBJECT.render(str(TIME), True, color)
	textrectobj = textsurfobj.get_rect()
	textrectobj.center = (XMARGIN + 400, 35)
	DISPLAYSURF.blit(textsurfobj, textrectobj)
	if(Flag == 0):
		for mines in MINESLIST:
			board[mines[0] - 1][mines[1] - 1][1] = UNCOVERED
		DrawMainBoard(board)
		top, left = GetTopLeftOfBox(4, 5)
		l = left
		t = top + 250
		textsurfobj = FONTOBJECT.render("GAME OVER", True, RED)
		textrectobj = textsurfobj.get_rect()
		textrectobj.center = (l + 81, t + 41)
		DISPLAYSURF.blit(textsurfobj, textrectobj)
		pygame.display.update()
		mousex, mousey = 0, 0
		while True:
			for event in pygame.event.get():
				if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
					terminator()
				elif event.type == MOUSEBUTTONUP and event.button == LEFT:
					mousex, mousey = event.pos
			#To Restart	the Game
			RectBox = pygame.Rect(XMARGIN + 345, YMARGIN + 440, 81, 40)
			if RectBox.collidepoint(mousex, mousey):
				main()
	else:
		#To Draw Best Score
		HighestScoreWrite()
		BestTime = HighestScoreRead()
		pygame.draw.rect(DISPLAYSURF, WHITE, (XMARGIN + 5, YMARGIN + 440, 81, 40))
		textsurfobj = FONTOBJECT.render(BestTime, True, BLACK)
		textrectobj = textsurfobj.get_rect()
		textrectobj.center = (XMARGIN + 49, YMARGIN + 460)#XMARGIN + 199
		DISPLAYSURF.blit(textsurfobj, textrectobj)
		
		DrawMainBoard(board)
		top, left = GetTopLeftOfBox(4, 5)
		l = left
		t = top + 250
		textsurfobj = FONTOBJECT.render("YOU WIN", True, GREEN)
		textrectobj = textsurfobj.get_rect()
		textrectobj.center = (l + 81, t + 41)
		DISPLAYSURF.blit(textsurfobj, textrectobj)
		pygame.display.update()
		mousex, mousey = 0, 0
		while True:
			for event in pygame.event.get():
				if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
					terminator()
				elif event.type == MOUSEBUTTONUP and event.button == LEFT:
					mousex, mousey = event.pos
			#To Restart	the Game
			RectBox = pygame.Rect(XMARGIN + 345, YMARGIN + 440, 81, 40)
			if RectBox.collidepoint(mousex, mousey):
				main()


#Terminator Function
def terminator():
	pygame.quit()
	sys.exit()


#Returns the List of Surrounding Boxes
def SurroundingBox(bx, by):
	surrondboxes = []
	if(bx - 1 != 0 and bx + 1 != 11 and by - 1 != 0 and by + 1 != 11):
		surrondboxes.append([bx - 1, by])
		surrondboxes.append([bx + 1, by])
		surrondboxes.append([bx, by - 1])
		surrondboxes.append([bx - 1, by - 1])
		surrondboxes.append([bx + 1, by - 1])
		surrondboxes.append([bx, by + 1])
		surrondboxes.append([bx - 1, by + 1])
		surrondboxes.append([bx + 1, by + 1])
	elif(bx - 1 == 0 and by - 1 == 0):
		surrondboxes.append([bx + 1, by])
		surrondboxes.append([bx, by + 1])
		surrondboxes.append([bx + 1, by + 1])
	elif(bx + 1 == 11 and by + 1 == 11):
		surrondboxes.append([bx - 1, by])
		surrondboxes.append([bx, by - 1])
		surrondboxes.append([bx - 1, by - 1])
	elif(bx - 1 == 0 and by + 1 == 11):
		surrondboxes.append([bx + 1, by])
		surrondboxes.append([bx, by - 1])
		surrondboxes.append([bx + 1, by - 1])
	elif(bx + 1 == 11 and by - 1 == 0):
		surrondboxes.append([bx - 1, by])
		surrondboxes.append([bx, by + 1])
		surrondboxes.append([bx - 1, by + 1])
	elif(bx + 1 == 11):
		surrondboxes.append([bx, by + 1])
		surrondboxes.append([bx, by - 1])
		surrondboxes.append([bx - 1, by])
		surrondboxes.append([bx - 1, by + 1])
		surrondboxes.append([bx - 1, by - 1])
	elif(by + 1 == 11):
		surrondboxes.append([bx - 1, by])
		surrondboxes.append([bx + 1, by])
		surrondboxes.append([bx, by - 1])
		surrondboxes.append([bx - 1, by - 1])
		surrondboxes.append([bx + 1, by - 1])
	elif(bx - 1 == 0):
		surrondboxes.append([bx, by - 1])
		surrondboxes.append([bx, by + 1])
		surrondboxes.append([bx + 1, by])
		surrondboxes.append([bx + 1, by - 1])
		surrondboxes.append([bx + 1, by + 1])
	elif(by - 1 == 0):
		surrondboxes.append([bx - 1, by])
		surrondboxes.append([bx + 1, by])
		surrondboxes.append([bx, by + 1])
		surrondboxes.append([bx - 1, by + 1])
		surrondboxes.append([bx + 1, by + 1])
	return surrondboxes


#Play Sound
def PlaySound():
	Beep = pygame.mixer.Sound(SOUND)
	Beep.play()



if __name__ == '__main__':
	main()
