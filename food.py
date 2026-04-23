from turtle import *

class Food:

		def __init__(self,position):
				self.x = position[0]
				self.y = position[1]
				self.size = 5 #the size also affects the enough of energy gained 

		def __repr__(self):
			return(f"Food (object) at pos: \033[96mX:{self.x}\033[0m , \x1b[0mY:{self.y}\x1b[0m | Size:{self.size}")
			
		def render(self, debug = False):
			pencolor("orange")

			penup()
			goto(self.x, self.y) 
			pendown()
			dot(self.size)
			penup()

			if debug:
				pencolor("red")
				goto(self.x, self.y+5) 
				pendown()
				write(f"({self.x},{self.y})")
