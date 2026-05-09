import pygame
import config


class Food:
		def __init__(self,position,screen):
				self.x = position[0]
				self.y = position[1]
				self.size = 5 #the size also affects the enough of energy gained 
				self.renderer = screen

		def __repr__(self):
			return(f"Food (object) at pos: \033[96mX:{self.x}\033[0m , \x1b[0mY:{self.y}\x1b[0m | Size:{self.size}")
			
		def render(self, debug = False):
			pygame.draw.circle(self.renderer, "red",(self.x, self.y), self.size)
