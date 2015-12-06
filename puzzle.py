from cell import *

class Puzzle(object):

	"""Represents a Puzzle"""

	def __init__(self, endOnReward):

		self.maze = [ [ Cell(x, y) for y in range(6)] for x in range(6) ]
		self.endOnRewardState = endOnReward
		self.discountFactor = 0.7

	def printUtilities(self):

		for x in xrange(0,6):
			for y in xrange(0,6):
				print self.maze[x][y].utility, "\t",
			print "\n"

	def readInMaze(self):
		# File containing maze
		file = open("maze.txt", "r")

		x = 0

		# Set the wall status and the rewards here
		for line in file:

			# Remove the \n
			line = line.rstrip()

			elements = line.split("\t")
			y = 0

			for character in elements:
				if character == 'T':
					self.maze[x][y].setWall()
					self.maze[x][y].setReward(0.0)
				elif character == 'F':
					pass
				else:
					self.maze[x][y].setReward(int(character))

				y += 1

			x += 1

		file.close()

	def setUtilitiesMDP(self):
		
		for n in range(1,500):

			for x in (range(0,6)):

				for y in range(0,6):

					if self.maze[x][y].wall == True:
						continue

					# Reward States are terminal and we reached a reward state
					if (self.endOnRewardState == True) and (abs(self.maze[x][y].reward) >= 1):
						self.maze[x][y].utility = self.maze[x][y].reward
						continue
						#raise Exception('Reached a Reward State')

					# Leftwards, Upwards, Rightwards, Downwards
					potentialValues = [0, 0, 0, 0]

					# Intended Direction is left
					if (y-1 < 0) or (self.maze[x][y-1].wall == True):
						potentialValues[0] = 0
					else:
						if y-1 >= 0:
							potentialValues[0] += 0.8 * self.maze[x][y-1].utility
					if x-1 >= 0:
						potentialValues[0] += 0.1 * self.maze[x-1][y].utility
					if x+1 <= 5:
						potentialValues[0] += 0.1 * self.maze[x+1][y].utility

					# Intended Direction is up
					if (x-1 < 0) or (self.maze[x-1][y].wall == True):
						potentialValues[1] = 0
					else:
						if x-1 >= 0:
							potentialValues[1] += 0.8 * self.maze[x-1][y].utility
					if y-1 >= 0:
						potentialValues[1] += 0.1 * self.maze[x][y-1].utility
					if y+1 <= 5:
						potentialValues[1] += 0.1 * self.maze[x][y+1].utility

					# Intended Direction is right
					if (y+1 > 5) or (self.maze[x][y+1].wall == True):
						potentialValues[2] = 0
					else:
						if y+1 <= 5:
							potentialValues[2] += 0.8 * self.maze[x][y+1].utility
					if x-1 >= 0:
						potentialValues[2] += 0.1 * self.maze[x-1][y].utility
					if x+1 <= 5:
						potentialValues[2] += 0.1 * self.maze[x+1][y].utility

					# Intended Direction is down
					if (x+1 > 5) or (self.maze[x+1][y].wall == True):
						potentialValues[3] = 0
					else:
						if x+1 <= 5:
							potentialValues[3] += 0.8 * self.maze[x+1][y].utility
					if y-1 >= 0:
						potentialValues[3] += 0.1 * self.maze[x][y-1].utility
					if y+1 <= 5:
						potentialValues[3] += 0.1 * self.maze[x][y+1].utility

					self.maze[x][y].utility = self.maze[x][y].reward + self.discountFactor * max(potentialValues)

	def setUtilitiesTDQL(self):
		pass
		#startX = 3, startY = 1

		#for n in range(1,500):

		#	time = 0




def main():
	puzzle = Puzzle(True)	# Reward States are considered Terminal States
	puzzle.readInMaze()
	puzzle.setUtilitiesMDP()
	puzzle.printUtilities()

if __name__ == '__main__':
	main()