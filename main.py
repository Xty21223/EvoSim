from cell import Cell
from food import Food
from random import randint 
import math
from world_setup import world
import pygame

import config

#------
pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
clock = pygame.time.Clock()


#spawn 1 cell object.
world.cells.append( Cell( parentpos=(config.WIDTH//2,config.HEIGHT//2), attributes=[
	11,  # speed		
	1,  # efficiency
	100, # health measured 200 (0.1 seconds)
	50, # range,
	0, # movement intelligence ( direction measured in angle),
	0 # carlson
	], 
	screen=screen)
	)


#store food objects
for i in range(10):
	world.food.append( Food( 
		position = ( config.WIDTH//2+randint(-200, 200) , config.HEIGHT//2+randint(-200,200) ),
		screen = screen )
	)

running = True
while running:
	clock.tick(60)
	# for detecting keypress event 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# clear the frame
	screen.fill("white")


	#render everything
	for obj in world.food:
		obj.render(debug = config.DEBUG_ENABLED)

	for cell in world.cells:
		cell.render(debug = config.DEBUG_ENABLED)

	#move cell
	for cell in world.cells:
		cell.action()

	deletions = []

	for i in range(len(world.cells)):
		try:
			world.cells[i].health -= 0.02
			if world.cells[i].health <= 0:
				deletions.append(world.cells[i])
		except IndexError:
			print("Surpassed index!")
		
	for object in deletions:
		world.cells.remove(object)


	pygame.display.flip()

pygame.quit()

#Create another list to store all cells that needs to be remove
#iterate through the deletion list and remove each dead cell in a seperate forloop at the end of each "frame"
