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
mutations = 0
deaths = 0


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
		position = ( config.WIDTH//2+randint(-700, 400) , config.HEIGHT//2+randint(-400,400) ),
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
		a3 = cell.action()
		if a3 == 1:
			mutations += 1
	deletions = []

	for i in range(len(world.cells)):
		try:
			world.cells[i].health -= 0.25
			if world.cells[i].health <= 0 or len(world.cells)-len(deletions) > 200:
				deletions.append(world.cells[i])
		except IndexError:
			print("Surpassed index!")
		
	for object in deletions:
		deaths += 1
		world.cells.remove(object)


	#checkf for reset	
	if len(world.cells) == 0:
		mutations = 0
		deaths = 0
		world.cells.append( Cell( parentpos=(config.WIDTH//2,config.HEIGHT//2), attributes=[
		16,  # speed		
		5,  # efficiency
		150, # health measured 200 (0.1 seconds)
		50, # range,
		0, # movement intelligence ( direction measured in angle),
		0 # carlson
		], 
		screen=screen, parent=True))

	font = pygame.font.SysFont(config.FONT_PREFERENCES, 20)
	if len(world.cells) >= 190: cellsamountindicatortext = "red"
	else: cellsamountindicatortext = "white"
	indicator_text = font.render(f"Cells: {len(world.cells)}/200", True, cellsamountindicatortext)
	text_rect = indicator_text.get_rect()
	text_rect.topright = (config.WIDTH - 10, 10)

	title_text = font.render(f"Evosim: {config.VERSION_NAME}, {config.VERSION}{config.DARKLET}", True, "cyan")
	title_text_rect = title_text.get_rect()
	title_text_rect.topleft = (10, 10)

	indicator1_text = font.render(f"Births: {mutations}  |  Deaths: {deaths}", True, "green")
	indicator1_text_rect = indicator1_text.get_rect()
	indicator1_text_rect.bottomleft = (10, config.HEIGHT - 10)

	# 6. Draw the text onto the screen
	screen.blit(indicator_text, text_rect)
	screen.blit(title_text, title_text_rect)
	screen.blit(indicator1_text, indicator1_text_rect)

	frame=pygame.Rect(0, 0, 1400, 800)
	frame.center = (config.WIDTH//2,config.HEIGHT//2)
	pygame.draw.rect(screen, "white", frame, 2)

	pygame.display.flip()

pygame.quit()