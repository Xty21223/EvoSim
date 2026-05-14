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
pygame.display.set_caption('EvoSim')



#spawn 1 cell object.
for i in range(1):
	world.cells.append( Cell( parentpos=(config.WIDTH//2,config.HEIGHT//2), attributes=[
	15,  # speed		
	3,  # efficiency
	100, # health measured 200 (0.1 seconds)
	50, # range,
	0, # movement intelligence ( direction measured in angle),
	0 # carlson
	], 
	screen=screen, parent=True)
	)


#store food objects
for i in range(config.FOOD_AMOUNT):
	world.food.append( Food( 
		position = ( config.WIDTH//2+randint(-700, 400) , config.HEIGHT//2+randint(-700,400) ),
		screen = screen )
	)

running = True
while running:
	clock.tick(120)
	# for detecting keypress event 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# clear the frame
	screen.fill((10, 10, 10))


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
			world.cells[i].health -= 0.25
			if world.cells[i].health <= 0:
				deletions.append(world.cells[i])
		except IndexError:
			print("Surpassed index!")
		
	for object in deletions:
		world.cells.remove(object)


	#checkf for reset	
	if len(world.cells) == 0:
		world.cells.append( Cell( parentpos=(config.WIDTH//2,config.HEIGHT//2), attributes=[
	16,  # speed		
	5,  # efficiency
	150, # health measured 200 (0.1 seconds)
	50, # range,
	0, # movement intelligence ( direction measured in angle),
	0 # carlson
	], 
	screen=screen, parent=True)
	)
	pygame.display.flip()

pygame.quit()

#Create another list to store all cells that needs to be remove
#iterate through the deletion list and remove each dead cell in a seperate forloop at the end of each "frame"
