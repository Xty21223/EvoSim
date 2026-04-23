from turtle import *
from cell import Cell
from food import Food
from random import randint 
import math
from world_setup import world

import config

screen = Screen()
screen.setup(world.width, world.height)
screen.tracer(0)
colormode(255)
hideturtle()




#spawn 1 cell object.
world.cells.append(Cell( parentpos=(0,0), attributes=[
	3,  # speed		
	1,  # efficiency
	100, # health measured 200 (0.1 seconds)
	50, # range,
	0, # movement intelligence ( direction measured in angle),
	0 # carlson
	] ))


#store food objects
for i in range(10):
	world.food.append( Food( ( randint(-200,200), randint(-200,200) ) )  )


while True:

	# clear the frame
	clear()


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


	screen.update()





#Create another list to store all cells that needs to be remove
#iterate through the deletion list and remove each dead cell in a seperate forloop at the end of each "frame"