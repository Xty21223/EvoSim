from turtle import *
import random
import math
from world_setup import world


#single cell organism 
class Cell():
	def __init__(self, parentpos, attributes, parent=False):
		if not parent:
			self.carlson = attributes [5] # tree level
			self.speed = attributes [0]
			self.efficiency = attributes [1]
			self.health = attributes [2]
			self.startinghealth = attributes [2]
			self.range = attributes [3]
			self.movement_intelligence = attributes [4]
			self.UID = int(str(self.carlson)+str(self.speed)+str(self.efficiency)+str(self.startinghealth)+str(self.range)+str(self.movement_intelligence))
			self.x = parentpos[0]
			self.y = parentpos[1]
			self.visible_food = []

	def render(self, debug= False):
		pencolor("black")
		penup()
		goto(self.x, self.y)
		pendown()
		dot(20)

		
		#vision 
		if debug:
			pencolor("red")
			penup()
			goto(self.x, self.y - self.range)
			pendown()
			circle(self.range)

	def action(self):
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

		#how will the cell decide what t

	def search(self, food_list):
		#check if food within visvion range
		self.visible_food = []
		for food in food_list:
			dx = self.x - food.x
			dy = self.y - food.y
			distance = math.sqrt(dx*dx+dy*dy)
			if distance <= self.range:
				self.visible_food.append((food, distance))
		return self.visible_food

	
	def move(self):
		if self.visible_food == []:
			return
		
		closest = None
		close_dst =  9999999
		for food in self.visible_food:
			if food[1] < close_dst:
				closest = food[0] 
				close_dst = food[1]
		y = closest.y - self.y
		x = closest.x - self.x
		angle = math.degrees( math.atan2(y,x) )

		dist =  math.sqrt(x*x+y*y)

		#calculate how much the cell should
		# walk in y & x direction to maintain
		# angle to the closest food.
		if dist > 0:
			stepx = x//(dist*10)
			stepy = y//(dist*10)
		else:
			stepx = 0
			stepy = 0
			#if self.x == closest.x and self.y == closest.y:
			if closest != None:
				world.food.remove(closest)


		self.x += stepx
		self.y += stepy
		