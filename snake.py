#!/usr/bin/python
# Snake console graphics game
import time
import random

import os

import kbhit

def clearScreen():
	if os.name == 'nt':
		os.system('cls') # clear screen using DOS command
	else:
		print '\x1b[2J',
		print '\x1bc',
		print '\x1bH',
		print '\x1bF',

class Tile:
	blinkState = False
	invert = False
	def __init__(self):
		self.state = 'empty'
		
	def set(self,state):
		self.state = state
		
	def getString(self):
		tile = ' '
		if self.state == 'empty':
			if self.invert:
				tile = '\xdb'
		elif self.state == 'head':
			if self.blinkState:
				tile = '\xb1'
			else:	
				tile = '\xb2'
		elif self.state == 'alien':
			if self.blinkState:
				tile = '\xe8'
			else:	
				tile = '\xf8'
		elif self.state == 'tail':
			tile = '\x69' #'\xb0'
		return tile

class Board:
	def __init__(self,rows,cols):
		Tile.invert = False
		self.rows = rows
		self.cols = cols
		self.board = [[Tile() for j in range(cols)] for i in range(rows)]
		
	def draw(self):
		clearScreen()
		print
		for row in self.board:
			line = ''
			for cell in row:
				line += cell.getString()
			print line
		print
	
	def setTile(self,row, col,state):
		self.board[row][col].set(state)

	def getTile(self,row, col):
		return self.board[row][col].state

	def setRandom(self, state):
		while True:
			newRow = random.randint(0,self.rows-1)
			newCol = random.randint(0,self.cols-1)
			if self.getTile(newRow,newCol) == 'empty':
				self.setTile(newRow,newCol,state)
				break
		return (newRow,newCol)


def Snake():
	boardSize = 10
	board = Board(boardSize,boardSize)
	pos = board.setRandom('head')
	row = pos[0]
	col = pos[1]
	board.setRandom('alien')
	
	tail = []
	gameOver = False
	while not gameOver:
		board.draw()	
		print "Score = %d" % len(tail)
		#action = raw_input("move?")
		if kb.kbhit():
			action = kb.getch()
			lastRow = row
			lastCol = col
			if action=='w' and row > 0:
				row -= 1
			elif action=='s' and row < boardSize-1:
				row += 1
			elif action=='a' and col > 0:
				col -= 1
			elif action=='d' and col < boardSize-1:
				col += 1
			elif action =='q':
				return True
			else:
				continue
				
			board.setTile(lastRow,lastCol,'tail')
			tail.insert(0,(lastRow,lastCol))				
				
			if board.getTile(row,col) == 'tail':
				print '\a'*4,	# bell	
				for i in range(4):
					Tile.invert = not Tile.invert
					board.draw()
					print
					print "Game Over!"
					time.sleep(.5)
				gameOver = True
			elif board.getTile(row,col) == 'alien':
				print '\a'*2, # bell
				board.setRandom('alien')
			else:
				c = tail.pop()
				board.setTile(c[0],c[1],'empty')
			
			board.setTile(row,col,'head')
			print '\a',  # bell
		else:
			time.sleep(.3)
			Tile.blinkState = not Tile.blinkState

	kb.set_normal_term()
	return False


kb = kbhit.KBHit()
done = False
while (not done):
	done = Snake()

kb.set_normal_term()

	
