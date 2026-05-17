import pyglet
from time import time
from random import randrange, choice
from enemy import Enemy, Rocketman, Repairman, Sniper
from constants import *
from HUD import Wall, Gun, HUD, Money


class Mainscreen():

	def __init__(self, *args, **kwargs):
		self.type = "Mainscreen" #to identify in the main loop
		self.play_button = play
		self.list_to_shoot = []
		self.is_play = False
		self.label = pyglet.text.Label("Welcome, Player.",
                          font_name=wall_font,
                          font_size=36,
                          x = int(1063 / 2), y = int(592 / 2 + 200),
                          color = (0, 0, 0, 255),
                          anchor_x='center', anchor_y='center')
		self.label2 = pyglet.text.Label("Click to shoot, space to reload. 25 rounds.",
                          font_name=wall_font,
                          font_size=23,
                          x = int(1063 / 2), y = int(592 / 2 - 260),
                          color = (0, 0, 0, 255),
                          anchor_x='center', anchor_y='center')

	def on_mouse_motion(self, x, y, dx, dy):
		if x in range(411, 651) and y in range(300, 366):
			if self.play_button != play_highlight:
				select_sound.play()
			self.play_button = play_highlight
		else:
			self.play_button = play

	def on_mouse_press(self, x, y, button, modifiers):
		self.list_to_shoot.append((Gun(), (x, y)))
		if button == 1:
			if x in range(411, 651) and y in range(300, 366):
				gunman_sound.play()
				self.is_play = True
			else:
				bullet_sound.play()
		else:
			bullet_sound.play()

	def on_draw(self):
		background.blit(0, 0)
		self.label.draw()
		self.label2.draw()
		self.play_button.blit(411, 300)
		for bullet in self.list_to_shoot:
			bullet[0].draw_animation(bullet[1], list_of_craters)
			bullet[0].animation_ticker += 1
			if bullet[0].animation_ticker % 16 == 0:
				self.list_to_shoot.remove(bullet)
				del bullet

	def update(self, dt):
		pass


class Levels():

	sniper_man_list = []
	repair_man_list = []
	sniper_rifle = False

	def __init__(self, level):
		self.type = "Levels" #to identify in the main loop
		self.list_of_enemies = []
		self.list_of_active_snipers = []
		self.attack_rate = 0 #determines how fast enemy attacks
		self.attack_speed = 40
		self.flag = False
		self.i = 0 #end time
		self.t1 = 0
		self.dt = 0
		self.is_play = False

		for level_difficulty in dict_of_levels:
			if level_difficulty == level:
				self.level = level #this is the level you are on currently
				self.enemy_spawn_rate = dict_of_levels[level_difficulty][0]
				self.time_duration = dict_of_levels[level_difficulty][1]
				self.rocket_spawn_rate = dict_of_levels[level_difficulty][2]
				self.in_the_beginning = time()

		#final level allows only sniper
		if self.level == 24:
			Gun.max_clip = 99
			Levels.sniper_man_list = []
			Levels.repair_man_list = []
			Levels.sniper_rifle = True
			Gun.type_of = "sniper"

	def on_mouse_motion(self, x, y, button, modifiers):
		pass

	def on_mouse_press(self, x, y, button, modifiers):
		if button == 1:
			if Gun.clip > 0 and self.flag == False:
				bullet_sound.play()
				for enemy in self.list_of_enemies:
					if x in range(int(enemy.x), int(enemy.x + enemy.width)):
						if y in range(int(enemy.y), int(enemy.y + enemy.height)):
							if Gun.type_of == "rifle":
								enemy.health -= 1
							elif Gun.type_of == "sniper":
								enemy.health -= 2
							Gun.draw_shoot_animation.append([Gun(), (x, y)])
					if enemy.health <= 0:
						self.list_of_enemies.remove(enemy)
						if enemy.type == "swordman":
							Money.money += 100
						elif enemy.type == "gunman":
							Money.money += 200
						else:
							Money.money += 400
				Gun.clip -= 1

	def on_key_press(self, symbol, modifiers):
		if symbol == 32 and self.flag == False:
			reload_sound.play()
			self.flag = True
			self.t1 = time()

	def spawn_new_enemy(self): #spawns a new enemy occasinaly
		i = randrange(1, self.enemy_spawn_rate)
		if i == 2:
			if self.level > 4:
				enemy_type = choice(["gunman", "swordman"])
			else:
				enemy_type = "swordman"

			enemy = Enemy(-20, randrange(25, 175), enemy_type)
			self.list_of_enemies.append(enemy)

	def spawn_rocket_man(self):
		if self.level >= 9:
			i = randrange(1, self.rocket_spawn_rate)
			if i == 2:
				rocket = Rocketman(-20, randrange(25, 175), "rocketman")
				self.list_of_enemies.append(rocket)

	def enemy_activity(self):
		for enemy in self.list_of_enemies:
			if enemy.type == "swordman" or enemy.type == "gunman":
				if enemy.y - (.5 * enemy.width) - 560 < round(((-159 / 160) * (enemy.x)) + 255): #linear equation to calculate the fence
					enemy.move_forward(self.dt)
				else:
					if enemy.running:
						enemy.running = False
					enemy.attack_wall()
			elif enemy.type == "rocketman":
				if enemy.x >= enemy.random_stop_point:
					if enemy.running == True or enemy.x != round(enemy.x):
						enemy.running, enemy.x = False, round(enemy.x)
					enemy.attack_wall()
				else:
					enemy.move_forward(self.dt)

	def sniper_shoot(self):
		for sniper in Levels.sniper_man_list:
			sniper.snipe_time += 1
			if sniper.snipe_time % 190 == 0 and len(self.list_of_enemies) > 0:
				gunman_sound.play()
				del self.list_of_enemies[randrange(0, len(self.list_of_enemies))]
				Money.money += 150
				self.list_of_active_snipers.append(sniper)

	def repair_wall(self):
		if Wall.health < Wall.max_health:
			for repairman in Levels.repair_man_list:
				if repairman.repair_time % 60 == 0:
					Wall.health += 1
				repairman.repair_time += 1

	def check_reload(self):
		if self.flag == True and (time() - self.t1) >= .8:
			Gun.clip = Gun.max_clip
			self.flag = False

	def check_loss(self):
		if Wall.health <= 0:
			self.is_play = True

	def check_end_of_level(self):
		self.i += 1
		if self.i % 1000 == 0:
			Repairman.repair_time = 0
			Sniper.sniper_animation_time = 0
			t2 = time()
			if t2 - self.in_the_beginning >= self.time_duration:
				Money.money -= int(Money.money * choice([1, 5, 10, 15, 20]) * .01) #tax
				self.is_play = True

	@classmethod
	def draw_hud(self): #this draws the HUD
		HUD.draw_hud_bg()
		HUD.draw_wall_health()
		HUD.draw_money()
		HUD.draw_bullets(Gun.clip, Gun.max_clip)

	def on_draw(self):
		background.blit(0, 0)
		self.draw_hud()
		for enemy in self.list_of_enemies:
			enemy.draw_to_screen()
		for bullet in Gun.draw_shoot_animation:
			bullet[0].draw_animation(bullet[1])
			bullet[0].animation_ticker += 1


			if bullet[0].animation_ticker % 30 == 0:
				del bullet[0]
				Gun.draw_shoot_animation.remove(bullet)
		for active_sniper in self.list_of_active_snipers:
			active_sniper.draw_sniper()
			Sniper.sniper_animation_time += 1
			if Sniper.sniper_animation_time % 10 == 0:
				self.list_of_active_snipers.clear()

	def update(self, dt):
		self.dt = dt
		self.spawn_new_enemy()
		self.spawn_rocket_man()
		self.enemy_activity()
		self.sniper_shoot()
		self.repair_wall()
		self.check_reload()
		self.check_end_of_level()
		self.check_loss()


class Shop():

	def __init__(self, level):
		self.type = "Shop" #to identify in the main loop
		self.is_play = False
		self.shop_button = shop_start
		self.bullet_image = bullet_pic
		self.hammer_image = hammer_pic
		self.upgrade_wall_image = repair_pic
		self.sniper_image = sniper
		self.fortify_image = fortify
		self.sniper_man_image = sniper_man
		self.repair_man_image = repair_man
		self.level = level
		self.label = pyglet.text.Label("Next Round: " + str(level + 1),
                          font_name=wall_font,
                          font_size=36,
                          x = int(1063 / 2), y = int(592 / 2 + 214),
                          color = (255, 255, 255, 255),
                          anchor_x='center', anchor_y='center')
		self.dict_of_cords = {
		"dbtnCords": (356, 17, 350, 35),
		"bullet_cords": (138, 405, 70, 70),
		"hammer_cords": (290, 405, 70, 70),
		"repair_cords": (453, 405, 70, 70),
		"sniper_cords": (600, 427, 150, 40),
		"fortify_cords": (800, 405, 70, 70),
		"sniper_man_cords": (138, 160, 70, 70),
		"repair_man_cords": (290, 160, 70, 70)
		}

	def on_mouse_motion(self, x, y, dx, dy):
		if x in range(356, 706) and y in range(17, 52):
			if self.shop_button != shop_start_highlight:
				select_sound.play()
			self.shop_button = shop_start_highlight
		else:
			self.shop_button = shop_start
		if x in range(138, 208) and y in range(405, 475):
			self.bullet_image = bullet_pic_highlight
		else:
			self.bullet_image = bullet_pic
		if x in range(290, 360) and y in range(405, 475):
			self.hammer_image = hammer_pic_highlight
		else:
			self.hammer_image = hammer_pic
		if x in range(453, 523) and y in range(405, 475):
			self.upgrade_wall_image = repair_pic_highlight
		else:
			self.upgrade_wall_image = repair_pic
		if x in range(600, 750) and y in range(427, 467):
			self.sniper_image = sniper_highlight
		else:
			self.sniper_image = sniper
		if x in range(800, 870) and y in range(405, 475):
			self.fortify_image = fortify_highlight
		else:
			self.fortify_image = fortify
		if x in range(138, 208) and y in range(160, 230):
			self.sniper_man_image = sniper_man_highlight
		else:
			self.sniper_man_image = sniper_man
		if x in range(290, 360) and y in range(160, 230):
			self.repair_man_image = repair_man_highlight
		else:
			self.repair_man_image = repair_man

	def on_mouse_press(self, x, y, button, modifiers):
		if x in range(356, 706) and y in range(17, 52) and button == 1:
			self.is_play = True
		if x in range(138, 208) and y in range(405, 475) and button == 1:
			if Money.money >= 1000:
				Gun.max_clip += 1
				Money.money -= 1000
		if x in range(290, 360) and y in range(405, 475) and button == 1:
			if Money.money >= 800:
				if Wall.health <= (Wall.max_health - 20):
					Wall.health += 20
					Money.money -= 800
				elif Wall.health < Wall.max_health:
					Wall.health = Wall.max_health
					Money.money -= 800
		if x in range(453, 523) and y in range(405, 475) and button == 1:
			if Money.money >= 25000:
				Wall.max_health += 150
				Money.money -= 25000
		if x in range(600, 750) and y in range(427, 467) and button == 1:
			if Money.money >= 75000 and Levels.sniper_rifle == False:
				Gun.type_of = "sniper"
				Levels.sniper_rifle = True
				Money.money -= 75000
		if x in range(138, 208) and y in range(160, 230) and button == 1:
			if Money.money >= 5000:
				Levels.sniper_man_list.append(Sniper())
				Money.money -= 5000
		if x in range(290, 360) and y in range(160, 230) and button == 1:
			if Money.money >= 8000:
				Levels.repair_man_list.append(Repairman())
				Money.money -= 8000
		if x in range(800, 870) and y in range(405, 475) and button == 1:
			if Money.money >= 100000:
				Money.money -= 100000

	def on_key_press(self, symbol, modifiers):
		pass

	def on_draw(self):
		shop_background.blit(0, 0)
		Levels.draw_hud()
		self.shop_button.blit(356, 17)
		self.bullet_image.blit(138, 405)
		self.hammer_image.blit(290, 405)
		self.upgrade_wall_image.blit(453, 405)
		self.sniper_image.blit(600, 427)
		self.fortify_image.blit(800, 405)
		self.sniper_man_image.blit(138, 160)
		self.repair_man_image.blit(290, 160)
		self.label.draw()

	def update(self, dt):
		pass

class Loss():

	def __init__(self, type_):
		self.is_play = False
		self.loser = loser_img
		self.win = win_img
		self.list_to_shoot = []
		self.type = type_

	def on_draw(self):
		if self.type != "win":
			self.loser.blit(0, 0)
		else:
			self.win.blit(0, 0)
		for bullet in self.list_to_shoot:
			bullet[0].draw_animation(bullet[1], list_of_craters)
			bullet[0].animation_ticker += 1
			if bullet[0].animation_ticker % 16 == 0:
				self.list_to_shoot.remove(bullet)
				del bullet

	def on_key_press(self, x, y):
		pass

	def on_mouse_press(self, x, y, button, b):
		self.list_to_shoot.append((Gun(), (x, y)))
		if button == 1:
			bullet_sound.play()

	def on_mouse_motion(self, x, y, dy, dx):
		pass

	def update(self, dt):
		pass


class Game(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
		pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
		self.screen_atm = Mainscreen()
		self.level = 0

	def on_mouse_motion(self, x, y, dx, dy):
		self.screen_atm.on_mouse_motion(x, y, dx, dy)

	def on_mouse_press(self, x, y, button, modifiers):
		self.screen_atm.on_mouse_press(x, y, button, modifiers)

	def on_key_press(self, symbol, modifiers):
		self.screen_atm.on_key_press(symbol, modifiers)

	def on_draw(self):
		self.clear()
		self.screen_atm.on_draw()

	def update(self, dt):
		self.screen_atm.update(dt)
		if self.screen_atm.is_play:
			if self.level >= 1 and self.screen_atm.type == "Levels": #basically checks if it is on level, so if it is on shop, it will not run this
				if Wall.health > 0:
					self.screen_atm = Shop(self.level)
				else:
					self.screen_atm = Loss("loss")
				if self.level >= 25 and Wall.health > 0:
					self.screen_atm = Loss("win")
			if self.screen_atm.is_play:
				self.screen_atm = Levels(self.level)
				Gun.clip = Gun.max_clip
				self.level += 1