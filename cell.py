import random
from random import randint
import math
from food import Food
from world_setup import world
import config
import time
import pygame

#single cell organism
class Cell():

	def __init__(self, parentpos, attributes, screen, parent=False):
		if True:
			self.carlson = attributes[5]  # tree level
			self.speed = attributes[0]
			self.efficiency = attributes[1]
			if not parent:	
				self.health = attributes[2]
				self.startinghealth = attributes[2]
			else:
				self.health = attributes[2]+200
				self.startinghealth = attributes[2]+200
			self.range = attributes[3]
			self.movement_intelligence = attributes[4]
			try:
				self.UID = (
					str(self.carlson) + str(self.speed) + str(self.efficiency) +
					str(self.startinghealth) + str(self.range) +
					str(self.movement_intelligence))
			except ValueError as value_err:
				print(f"Error:", value_err)
				print(f" UID: {str(self.carlson) + str(self.speed) + str(self.efficiency) +
					str(self.startinghealth) + str(self.range) +
					str(self.movement_intelligence)}")
			self.x = parentpos[0]
			self.y = parentpos[1]
			self.visible_food = []
			if not parent:
				self.fat_enough = self.health/self.efficiency
			else: self.fat_enough = 25
			self.current_fat = 0
			self.startingticks = 100
			self.goal = None
			self.state = "wander"
			self.color = "black"
			self.size = 8
			self.consume_sound = pygame.mixer.Sound('beep.wav')
		self.renderer = screen

	def render(self, debug=False):
		pygame.draw.circle(self.renderer, "white",(self.x, self.y), self.size)
		
		if debug:
			pygame.draw.circle(self.renderer, "blue", (self.x,self.y),self.range, width =1 ) # width=1 means hollow circle
			
			if self.goal:
				pygame.draw.circle(self.renderer, "green",(self.goal[0], self.goal[1]), 2)

	def action(self):
		if self.startingticks <= 0:
			self.color = "black"
			global world
			"""
			-> sense nearby food within the vision range
	
					-> then move to the food at max speed
			-> it can also rest
	
			-> attack if "possible" 
			-> food is for reproduction
			-> energy recovers overtime.
			-> if it sense a "enemy/predatory" cell nearby it attacks
			-> food is top priority 
			"""
			# when the cell.current_fat reaches cell.fat_enough then 
			# the cell will reproduce
			
			#if self.current_fat < self.fat_enough and self.state == "hunting":
				#print("seeking food")
			self.seekFood(world.food)
				#print("finding food")
			if self.current_fat >= self.fat_enough:
				#print(f"{self} is cloning---")
				self.mitosis()
				self.state = "cloning"
				return 1
			elif self.state == "wander":
				if self.goal == None:
					self.goal = (config.WIDTH//2+randint(-700, 400) , config.HEIGHT//2+randint(-400,400))


				#if we have goal and reached the goal
				if getDistance((self.x,self.y), self.goal) <= self.speed:
					self.goal = (config.WIDTH//2+randint(-700, 400) , config.HEIGHT//2+randint(-400,400))
				
				self.move()
		else:
			self.color = "green"
			self.startingticks -= 1

	def seekFood(self, food_list):
		#check if food within visvion range
		self.visible_food = []
		for food in food_list:
			dx = self.x - food.x
			dy = self.y - food.y
			distance = math.sqrt(dx * dx + dy * dy)
			if distance <= self.range:
				self.visible_food.append((food, distance))
		if self.visible_food == []:
			self.state = "wander"
			return
		else: 
			self.state = "hunting"


		closest = None
		close_dst = 9999999
		for food in self.visible_food:
			if food[1] < close_dst:
				closest = food[0]
				close_dst = food[1]
				self.goal = (closest.x, closest.y)
				
		self.move()
		
		if close_dst <= 1:
			world.food.remove(closest)
			#self.consume_sound.play()
			self.current_fat += closest.size * 5
			world.food.append( Food( 
				position = ( config.WIDTH//2+randint(-700, 400) , config.HEIGHT//2+randint(-400,400) ),
				screen = self.renderer)
			)

	def move(self):
		"""
		change the cell's x & y to head toward self.goal 
		self.goal is simply a tuple with the x & y value.
		"""
		#print(self.x, self.y)
		if self.goal != None:
			y = self.goal[1] - self.y
			x = self.goal[0] - self.x
			
			angle = math.degrees(math.atan2(y, x))
	
			dist = math.sqrt(x * x + y * y)

			# calculate how much the cell should
			# walk in y & x direction to maintain
			# angle to the closest food.
			# print("dist:",dist)
			if dist > 1:
				stepx = x / (dist * 10) * self.speed
				stepy = y / (dist * 10) * self.speed
				#print("stepx:", stepx, "stepy:", stepy)
			else:
				stepx = 0
				stepy = 0

			self.x += stepx
			self.y += stepy
			#print("moving!")


	def mitosis(self):
		if random.randint(1, config.MUTATION_RATE) == 1:
			print("yay")

		
		for i in range(random.randint(1,3)):
			neweff = self.efficiency + random.randint(-1,1)  # efficiency
			if neweff == 0:
				neweff = 1
			newcell =Cell( parentpos=(self.x,self.y), attributes=[
				self.speed + random.randint(-2,1),
				neweff,
				self.startinghealth + random.randint(-20,20), # health measured 200 (0.1 seconds) 
				self.range + random.randint(-10,10), # range,
				self.movement_intelligence, # movement intelligence ( direction measured in angle),
				self.carlson + 1 # carlson
				], screen=self.renderer)

			
			# print(f"""created: {newcell} \n
			# with starting health:{newcell.startinghealth}\n
			# with current fat:{newcell.current_fat}\n
			# with fat enough: {newcell.fat_enough}\n
			# """)
			world.cells.append(newcell)
			
		self.current_fat = 0



def getDistance(pos1, pos2):
	"""
	pos1 = (x,y)
	pos2 = (x2,y2)
	"""
	y = pos2[1] - pos1[1]
	x = pos2[0] - pos1[0]
	dist = math.sqrt(x * x + y * y)
	return dist


	
