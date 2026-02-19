from turtle import *

class Food:
		def __init__(self,position):
				self.x = position[0]
				self.y = position[1]
				self.size = 5

		def render(self, debug = False):

			if debug:
				pencolor("red")
			else:
				pencolor("orange")

			penup()
			goto(self.x, self.y) 
			pendown()
			dot(self.size)
			penup()
			goto(self.x, self.y+5) 
			pendown()
			write(f"({self.x},{self.y})")
