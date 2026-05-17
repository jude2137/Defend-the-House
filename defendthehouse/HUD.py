import pyglet
from constants import *


class Gun():

	clip = 7
	max_clip = 7
	draw_shoot_animation = []
	type_of = "rifle"

	def __init__(self, animation_list = list_of_bloods):
		self.animation_ticker = 0

	def draw_animation(self, position, animation_list = list_of_bloods):
		balance = 10 if animation_list == list_of_craters else 5
		animation_list[self.animation_ticker % len(animation_list)].blit(position[0] - balance, position[1] - balance)


class Wall():

	health = 100
	max_health = 100

	def __repr__(self):
		return str(Wall.health)


class Money():

	money = 0


class HUD():


	@staticmethod
	def draw_hud_bg():
		hud.blit(67, 550)

	@classmethod
	def draw_wall_health(cls):
		label = pyglet.text.Label(str(Wall.health) + "/" + str(Wall.max_health),
                          font_name=wall_font,
                          font_size=20,
                          x = 834, y = 562,
                          color = (255, 0, 0, 255))
		label.draw()

	@classmethod
	def draw_money(cls):
		amount_of_money = pyglet.text.Label("$" + str(Money.money),
                          font_name=wall_font,
                          font_size=20,
                          x = 350, y = 562,
                          color = (0, 0, 0, 255))
		amount_of_money.draw()

	@classmethod
	def draw_bullets(cls, reloaad, max_reload):
		bullets = pyglet.text.Label(str(reloaad) + "/" + str(max_reload),
                          font_name=wall_font,
                          font_size=20,
                          x = 283, y = 562,
                          color = (218, 144, 33, 255))
		bullets.draw()