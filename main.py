from turtle import *
from cell import Cell
from food import Food
from random import randint 
import math
from world_setup import world



# fullscreen the canvas
screen = Screen()
screen.setup(world.width, world.height)
screen.tracer(0)
colormode(255)
hideturtle()


#spawn 1 cell object.
cell1 = Cell( parentpos=(0,0), attributes=[
	1,  # speed
	1,  # efficiency
	200, # health measured 200 (0.1 seconds) 
	85, # range,
	0, # movement intelligence ( direction measured in angle),
	0 # carlson
	] )


#store food objects
for i in range(10):
	world.food.append( Food( ( randint(-200,200), randint(-200,200) ) )  )


while True:

	# clear the frame
	clear()


	#render everything
	for obj in world.food:
		obj.render()

	cell1.render(debug = True)
	
	#find food 
	v = cell1.search(world.food)

	for item in v:
		item[0].render(debug = True)

	#move cell
	cell1.move()

	

	screen.update()





screen.mainloop()
