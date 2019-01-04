#3rd party modules
import pygame
import tcod

# game files
import constants



#  ____ _____ ____  _   _  ____ _____ 
# / ___|_   _|  _ \| | | |/ ___|_   _|
# \___ \ | | | |_) | | | | |     | |  
#  ___) || | |  _ <| |_| | |___  | |  
# |____/ |_| |_| \_\\___/ \____| |_|  
                                     
class struc_Tile:
	def __init__(self, block_path):
		self.block_path = block_path
		self.explored = False



#   ___  ____      _ _____ ____ _____ ____  
#  / _ \| __ )    | | ____/ ___|_   _/ ___| 
# | | | |  _ \ _  | |  _|| |     | | \___ \ 
# | |_| | |_) | |_| | |__| |___  | |  ___) |
#  \___/|____/ \___/|_____\____| |_| |____/ 
                                           
class obj_Actor:
	def __init__(self, x, y, name_object, sprite, creature = None, ai = None):
		self.x = x # map address not display pixels
		self.y = y # map address not display pixels
		self.sprite = sprite

		self.creature = creature
		if creature:
			creature.owner = self

		self.ai = ai
		if ai:
			ai.owner = self

	def draw(self):
		# draw the object
		is_visible = tcod.map_is_in_fov(FOV_MAP, self.x, self.y)

		if is_visible:
			SURFACE_MAIN.blit(self.sprite, ( self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))

class obj_Game:
	def __init__(self):
		
		self.current_map = map_create()
		self.message_history = []
		self.current_objects = []	

class obj_Spritesheet:
	''' Class used to grab images out of a spritesheet. '''
	def __init__(self, file_name):
		# Load the sprite sheet.
		self.sprite_sheet = pygame.image.load(file_name).convert()
		self.tiledict = {'a': 1, 'b': 2, 'c': 3, 'd': 4,
						 'e': 5, 'f': 6, 'g': 7, 'h': 8,
						 'i': 9, 'j': 10, 'k': 11, 'l': 12,
						  'm': 13, 'n': 14, 'o': 15, 'p': 16}

	def get_image(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT,
				scale = None):
		''' Scale is a tuple '''

		image = pygame.Surface([width, height]).convert()

		image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column]*width, row*height, width, height ))

		image.set_colorkey(constants.COLOR_BLACK)

		if scale:
			(new_w, new_h) = scale
			image = pygame.transform.scale(image, (new_w, new_h))

		return image


class com_Creature:
	''' Creatures have health, can damage objects by attacking them. Can also die.'''
	def __init__(self, name_instance, hp = 10, death_function = None):
		self.name_instance = name_instance
		self.maxhp = hp
		self.hp = hp
		self.death_function = death_function

	def move(self, dx, dy):
		
		tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)
		
		target = map_check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)
		
		if target:
			self.attack(target, 5)

		if not tile_is_wall:
			self.owner.x += dx
			self.owner.y += dy

	def attack(self, target, damage):
		game_message(self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage!", constants.COLOR_WHITE)
		target.creature.take_damage(5)

	def take_damage(self, damage):
		self.hp -= damage
		game_message(self.name_instance + "'s health is " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_GREY)

		if self.hp <= 0:
			if self.death_function is not None:
				self.death_function(self.owner)


#TODO class com_Item:

#TODO class com_Container:



#     _    ___ 
#    / \  |_ _|
#   / _ \  | | 
#  / ___ \ | | 
# /_/   \_\___|
              

class com_AI:
	''' Once per turn, execute. '''
	def take_turn(self):
		self.owner.creature.move(tcod.random_get_int(0, -1, 1), tcod.random_get_int(0, -1, 1))

def death_monster(monster):
	''' On death, most monsters stop moving. '''
	game_message(monster.creature.name_instance + " is DEAD!", constants.COLOR_RED)
	monster.creature = None
	monster.ai = None





def map_create():
	new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

	new_map[10][10].block_path = True
	new_map[10][15].block_path = True

	for x in range(constants.MAP_WIDTH):
		new_map[x][0].block_path = True
		new_map[x][constants.MAP_HEIGHT-1].block_path = True

	for y in range(constants.MAP_HEIGHT):
		new_map[0][y].block_path = True
		new_map[constants.MAP_WIDTH-1][y].block_path = True

	map_make_fov(new_map)

	return new_map

def map_check_for_creature(x, y, exclude_object = None):

	target = None

	if exclude_object:
		# check objectlist to find creature at that location that isn't excluded
		for obj in GAME.current_objects:
			if (obj is not exclude_object and 
				obj.x == x and 
				obj.y == y and 
				obj.creature):
				target = obj
				
			if target:
				return target
	
	else:
	# check objectlist to find any creature at that location
		for obj in GAME.current_objects:
			if (obj.x == x and 
				obj.y == y and 
				obj.creature):
				target = obj
				
			if target:
				return target                                                

def map_make_fov(incoming_map):
	global FOV_MAP

	FOV_MAP = tcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

	for y in range(constants.MAP_HEIGHT):
		for x in range(constants.MAP_WIDTH):
			tcod.map_set_properties(FOV_MAP, x, y, not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)

def map_calculate_fov():
	global FOV_CALCULATE

	if FOV_CALCULATE:
		FOV_CALCULATE = False
		tcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS, constants.FOV_ALGO)





def draw_game():

	global SURFACE_MAIN

	# clear the surface
	SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

	# TODO draw the map
	draw_map(GAME.current_map)

	# Draw all objects
	for obj in GAME.current_objects:
		obj.draw()

	draw_debug()
	draw_messages()

	# update the display
	pygame.display.flip()

def draw_map(map_to_draw):

	for x in range(0, constants.MAP_WIDTH):
		for y in range(0, constants.MAP_HEIGHT):

			is_visible = tcod.map_is_in_fov(FOV_MAP, x, y)

			if is_visible:

				map_to_draw[x][y].explored = True

				if map_to_draw[x][y].block_path == True:
					# draw wall
					SURFACE_MAIN.blit(constants.S_WALL, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
				else:
					# draw floor
					SURFACE_MAIN.blit(constants.S_FLOOR, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))

			elif map_to_draw[x][y].explored:
					
				if map_to_draw[x][y].block_path == True:
				# draw wall
					SURFACE_MAIN.blit(constants.S_WALL_EXPLORED, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
				else:
				# draw floor
					SURFACE_MAIN.blit(constants.S_FLOOR_EXPLORED, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))

def draw_debug():
	draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())), (0, 0), constants.COLOR_WHITE, constants.COLOR_BLACK)

def draw_messages():

	to_draw = GAME.message_history[-(constants.NUM_MESSAGES):]

	text_height = helper_text_height(constants.FONT_MESSAGE_TEXT)
	start_y = constants.MAP_HEIGHT*constants.CELL_HEIGHT - (constants.NUM_MESSAGES * text_height)

	i = 0
	
	for message, color in to_draw:
		
		draw_text(SURFACE_MAIN, message, (0, start_y + (i * text_height)), color, constants.COLOR_BLACK)

		i += 1

def draw_text(display_surface, text_to_display, T_coords, text_color, back_color = None):
	''' This function takes in some text and displays it on the referenced surface. '''
	text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)

	text_rect.topleft = T_coords

	display_surface.blit(text_surf, text_rect)





def helper_text_objects(incoming_text, incoming_color, incoming_back_color):

	if incoming_back_color:
		Text_surface = constants.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color, incoming_back_color)
	else:
		Text_surface = constants.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color)

	return Text_surface, Text_surface.get_rect()

def helper_text_height(font):

	font_object = font.render('a', False, (0, 0, 0))
	font_rect = font_object.get_rect()

	return font_rect.height



#   ____    _    __  __ _____ 
#  / ___|  / \  |  \/  | ____|
# | |  _  / _ \ | |\/| |  _|  
# | |_| |/ ___ \| |  | | |___ 
#  \____/_/   \_\_|  |_|_____|
                             
def game_main_loop():
	''' In this function, we loop the main game '''

	game_quit = False
	# Player action definition
	player_action = "no-action"

	while not game_quit:

		# handle player input
		player_action = game_handle_keys()

		map_calculate_fov()

		if player_action == "QUIT":
			game_quit = True

		if player_action == "player-moved":
			for obj in GAME.current_objects:
				if obj.ai != None:
					obj.ai.take_turn()

		# draw the game
		draw_game()

		CLOCK.tick(constants.GAME_FPS)

	# quit the game
	pygame.quit()
	exit()

def game_initialize():
	''' This function initializes the main window and pygame '''

	global SURFACE_MAIN, GAME, PLAYER, ENEMY, FOV_CALCULATE, CLOCK

	#initialize pygame
	pygame.init()

	CLOCK = pygame.time.Clock()

	SURFACE_MAIN = pygame.display.set_mode( (constants.MAP_WIDTH*constants.CELL_WIDTH, constants.MAP_HEIGHT*constants.CELL_HEIGHT) )

	GAME = obj_Game()

	FOV_CALCULATE = True

	# TEMP SPRITES

	tempspritesheet = obj_Spritesheet("data\\spritesheet_aquatic.png")
	S_PLAYER = tempspritesheet.get_image('a', 3, 16, 16, (32, 32))
	
	creature_com1 = com_Creature("PLAYER")
	PLAYER = obj_Actor(1, 1, "Pepe", S_PLAYER, creature = creature_com1)

	creature_com2 = com_Creature("NPC", death_function = death_monster)
	ai_com = com_AI()
	ENEMY = obj_Actor(20, 5, "Nippeli", constants.S_ENEMY, creature = creature_com2, ai = ai_com)

	GAME.current_objects = [PLAYER, ENEMY]

def game_handle_keys():
	
	global FOV_CALCULATE
	# get player input
	events_list = pygame.event.get()

	# process input
	for event in events_list:
		if event.type == pygame.QUIT:
			return "QUIT"

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				PLAYER.creature.move(0, -1)
				FOV_CALCULATE = True
				return "player-moved"

			if event.key == pygame.K_DOWN:
				PLAYER.creature.move(0, 1)
				FOV_CALCULATE = True
				return "player-moved"

			if event.key == pygame.K_LEFT:
				PLAYER.creature.move(-1, 0)
				FOV_CALCULATE = True
				return "player-moved"

			if event.key == pygame.K_RIGHT:
				PLAYER.creature.move(1, 0)
				FOV_CALCULATE = True
				return "player-moved"
	return "no-action"

def game_message(game_msg, msg_color):

	GAME.message_history.append((game_msg, msg_color))




## EXECUTE GAME ##
if __name__ == '__main__':
	game_initialize()
	game_main_loop()


