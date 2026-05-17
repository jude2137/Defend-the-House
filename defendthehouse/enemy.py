import pyglet
from random import choice, randrange
from constants import *
from HUD import Wall

class Enemy():

	def __init__(self, x, y, type_):
		self.x = x
		self.y = y
		self.original_y = self.y #this helps us to do the sin function
		self.type = type_
		self.width = 20
		self.height = 40
		self.running = True
		self.i = 0 #controls animation
		self.animation_speed = 0 #controls animation speed
		self.attack_speed = 0
		self.path_to_walk = choice([path_to_walk1,
			path_to_walk2,
			path_to_walk3,
			None,
			None,
			None,
			None,
			None,
			None,
			None,
			None,
			None,
			None,
			])

		if self.type == "gunman":
			self.health = 4
			self.vel = randrange(1, 3)
			self.attack_rate = 10
			self.damage = 2
		elif self.type == "swordman":
			self.health = 2
			self.vel = randrange(1, 3)
			self.attack_rate = 30
			self.damage = 1

	def move_forward(self, dt):
		if self.path_to_walk != None:
			self.y = self.original_y + self.path_to_walk[self.x + 20] * dt * 60
		self.x += self.vel

	def attack_wall(self):
		self.attack_speed += 1
		if self.attack_speed % self.attack_rate == 0:
			Wall.health -= self.damage

	def draw_to_screen(self):
		if self.running:
			list_of_walking_animations[self.i % 8].blit(self.x, self.y)
			self.animation_speed += 1
			if self.animation_speed % 5 == 0:
				self.i += 1
		else:
			list_of_attacking_animations[self.i % 8].blit(self.x, self.y)
			self.animation_speed += 1
			if self.animation_speed % 3 == 0:
				self.i += 1


class Rocketman():
	
	def __init__(self, x, y, type_):
		self.x = x
		self.y = y
		self.type = type_
		self.width = 20
		self.height = 40
		self.running = True
		self.i = 0 #controls animation
		self.animation_speed = 0 #controls animation speed
		self.health = 8
		self.vel = 1
		#attacking_wall/shooting
		self.damage = 50
		self.attack_speed = 0
		self.attack_rate = 230
		self.random_stop_point = randrange(70, 180) #randomly stops & begins attacking
		self.one_time_check = False #makes sure bullet animation starts at gun

	def move_forward(self, dt):
		self.x += self.vel

	def attack_wall(self):
		self.attack_speed += 1
		if self.attack_speed % self.attack_rate == 0:
			Wall.health -= self.damage

	def draw_to_screen(self):
		if self.running:
			rocket_attack.blit(self.x, self.y)
			self.animation_speed += 1
			if self.animation_speed % 5 == 0:
				self.i += 1
		else:
			if self.i % 75 != 0 and not self.one_time_check:
				self.one_time_check = True
				self.i = 75
			rocket_attack.blit(self.x, self.y)
			bullet.blit(self.x + bullet_moves[self.i % 75] + 20, self.y + 25)
			self.animation_speed += 1
			if self.animation_speed % 3 == 0:
				self.i += 1



class Repairman():

	repair_number = []

	def __init__(self):
		self.create_repair_time(self)

	@classmethod
	def create_repair_time(cls, self):
		while True:
			i = randrange(1, 121)
			if i not in cls.repair_number:
				self.repair_time = i
				cls.repair_number.append(self.repair_time)
				break
		else:
			self.repair_time = randrange(1, 121)


class Sniper():

	list_of_snipers = []
	sniper_animation_time = 0

	def __init__(self):
		self.window = choice([(872, 134), (852, 153), (832, 173)]) #random one of the 3 windows
		self.create_snipe_time(self)

	@classmethod
	def create_snipe_time(cls, self):
		while True:
			i = randrange(1, 481)
			if i not in cls.list_of_snipers:
				self.snipe_time = i
				cls.list_of_snipers.append(self.snipe_time)
				break
		else:
			self.snipe_time = randrange(1, 481)
			cls.list_of_snipers.append(self.snipe_time)

	def draw_sniper(self):
		sniper_bullet.blit(self.window[0], self.window[1])