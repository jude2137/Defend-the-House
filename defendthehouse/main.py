import pyglet
import pyglet.gl
from pyglet.gl import *
from game import Mainscreen, Levels, Game
from constants import icon

def main():
	screen = Game(1063, 592, "Defend The House")
	screen.set_icon(icon)
	screen.set_vsync(True)
	while not screen.has_exit:
		dt = pyglet.clock.tick()
		screen.dispatch_events()
		screen.update(dt)
		screen.dispatch_event('on_draw')
		screen.flip()

if __name__ == "__main__":
	main() 