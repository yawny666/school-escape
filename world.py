from random import randint, choice
from colorama import Fore, Style, init

import enemies
import items
import npcs

init(autoreset=True)


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.description = "room"
        self.items = [] 

        # environmental hazards here
        # gas 
        global gas_placed
        self.gas = None 
        if gas_placed == 0:
            if randint(0, 30) == 1:
                self.gas = 1 
                gas_placed = 1

        # shitic
        global fartsmell_placed
        self.fartsmell = None 
        if fartsmell_placed == 0:
            if randint(0, 30) == 1:
                self.fartsmell = 1 
                fartsmell_placed = 1


        #enemy generation; only one per tile
        r = randint(0,100)
        if r < 5:
            self.enemy = enemies.Headmaster()
        elif r < 10:
            self.enemy = enemies.Chupacabra()
        elif r < 20:
            self.enemy = enemies.Administrator()
        elif r < 35:
            self.enemy = enemies.Teacher()
        elif r < 43:
            self.enemy = enemies.Bully()
        elif r < 60:
            self.enemy = enemies.Scrub()
        if self.has_enemy():
            #25% chance of automatic aggro
            self.enemy.is_aggro = 1 if (randint(0,4) == 1) else None

        #trader generation
        global trader_placed
        if trader_placed == 0:
            #uncomment these two lines to put a trader in starting tile
#            if isinstance(self, StartTile):
#                self.npc = npcs.Trader("Arthur", "wily little schemer")
            # and comment the next 8 lines to prevent trader from being placed outside starting tile
            r = randint(0,40) 
            if r == 0:
                self.npc = npcs.Trader("Arthur","wily little schemer")
                trader_placed = 1
                # for debugging only 
                # print("trader at",self.x,self.y)
            elif r == 1:
                self.npc = npcs.Trader("Tristan","twirling fairy prince with pretty lace stockings")
                trader_placed = 1

        #random NPCs 
        r = randint(0, 40)
        if r == 0:
            self.npc = npcs.Ruby("Ruby", "babbling brook of information")
        elif r == 1:
            self.npc = npcs.Rando("Oliver Howard", "shifty middle school edgelord")
 
        #powerup generation
        r = randint(0, 100)
        if r<10:
            self.items.append(items.Burrito())
        elif r < 25:
            self.items.append(items.Taco())
        elif r < 45:
            self.items.append(items.Chips())
        elif r < 55:
            self.items.append(items.GranolaBar())
        elif r < 65:
            self.items.append(items.StringCheese())

        #weapon generation
        r = randint(0, 200)
        if r < 4:
            self.items.append(items.MagicMace())
        elif r < 8:
            self.items.append(items.ClubMace())
        elif r < 13:
            self.items.append(items.Mace())
        elif r < 20:
            self.items.append(items.ButterKnife())
        elif r < 23:
            self.items.append(items.Machete())
        elif r < 27:
            self.items.append(items.Stiletto())
        elif r < 30:
            self.items.append(items.Ruler())
        elif r < 33:
            self.items.append(items.Scissors())

        #loot generation
        #loot generation
        r = randint(0,100)
        if r<1:
            self.items.append(items.Loot("Deez Nutz for President poster",1))
        if r<2:
            self.items.append(items.Loot("embroidery kit",3))
        if r<4:
            self.items.append(items.Iphone())
        elif r < 6:
            self.items.append(items.Laptop())
        elif r < 11:
            self.items.append(items.Dollar())
        elif r < 18:
            self.items.append(items.Twenty())
        elif r < 20:
            self.items.append(items.Diaper())
        elif r < 21:
            self.items.append(items.GasNeutralizer())
        elif r < 22:
            self.items.append(items.DustMask())
        elif r < 23:
            self.items.append(items.Loot("greasy yoga mat",1))
        elif r < 24:
            self.items.append(items.Loot("small boy's tutu",1))
        elif r < 28:
            self.items.append(items.Loot("beat-up chromebook",50))
        elif r < 29:
            self.items.append(items.Loot("Words We Will Not Use hardcopy",0))
        elif r < 30:
            self.items.append(items.Loot("spray bottle full of Rozzle",5))
        elif r < 31:
            self.items.append(items.Loot("Student Green Team manual",0))
        elif r < 35:
            self.items.append(items.Loot("prescription for Ritalin",100))

    def describe(self):
        string = "You're in a {}. ".format(self.description)
        if hasattr(self,'npc'):
            string += "\n{} is here, a {}. You can talk to {}.".format(self.npc.name,self.npc.description,self.npc.name)
        if self.items:
            for item in self.items:
                string +=  "\nYou see a {}.".format(item)
                if self.gas:
                    gastype = choice(["hazy","reddish","bluish","greenish","farty-smelling"])
                    string += "\nYou notice a " + gastype + " gas in the room. You feel woozy."
                if self.fartsmell:
                    string += "\nSome little monster has laid a turd in the room. You cannot breathe. If you don't have a mask, you'd better get out."
        if hasattr(self,'enemy'):
            if self.enemy.is_alive():
                if not self.enemy.is_aggro:
                    string +=  "\nThere's a {} here!".format(self.enemy.name)
            else:
                string +=  "\nA dead {} lies on the ground.".format(self.enemy.name)
        return string

    def modify_player(self,player):
        if hasattr(self,'enemy'):
            if self.enemy.is_alive() and self.enemy.is_aggro:
                dmg = randint(0,self.enemy.damage)
                player.health = max(0,player.health - dmg)
                print(Fore.GREEN + "** {} attacks, doing {} damage. **\nYou have {} HP remaining.".format(self.enemy.name, dmg, player.health))

    def has_enemy(self):
        return hasattr(self, 'enemy')

class StartTile(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y) 
        self.description = "Science lab full of brain-dead zombies"
        self.gas = 0
        self.fartsmell = 0
		
class GameTile(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)
        r = randint(0,33)
        if r <2:
            self.description = "meditation/lactation room"
        elif r < 3:
            self.description = "dirty faculty lounge. Food-stained silverware and coffee cups fill the sink"
        elif r < 5:
            self.description = "gigantic, rarely used all-gender bathroom"
        elif r < 9:
            self.description = "useless administrator's office"
        elif r < 10:
            self.description = "dark room lit by candles arranged in a pentagram"
        elif r < 20:
            self.description = "chaotic classroom. Inane lists written on chart paper are taped up everywhere"
        elif r < 21:
            self.description = "art room filled with broken stools"
        elif r < 26:
            self.description = "learning specialist's office. Old dolls and yarn projects are piled in the corner"
        elif r < 31:
            self.description = "depressing hallway"
        else:
            self.description = "run-down student lounge. Garbage is littered across the floor"

class BasementTile(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y) 
        self.description = "damp, smelly basement"

class RoofTile(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y) 
        self.description = "children's rooftop playground. Broken toys are everywhere"

class EscapeTile(MapTile):
    def modify_player(self,player):
        player.victory = True

    def describe(self):
        return """
You made it out! You are free! Run as fast as you can!
        """

# READ IN MAP FROM EXTERNAL FILE

world_dsl = ""
world_num = randint(1,5)
file = open("map" + str(world_num) + ".txt", "r") 
for line in file: 
	world_dsl += line
	world_dsl += "\n"
	
#rudimentary DSL syntax checker
def is_valid_dsl(dsl):
	if dsl.count("|ST|") != 1:
		return False
	if dsl.count("|ET|") == 0:
		return False
	lines = dsl.splitlines()
	lines = [l for l in lines if l]
	pipe_counts = [line.count("|") for line in lines]
	for count in pipe_counts:
		if count != pipe_counts[0]:
			return False
	return True

tile_type_dict = {
	"ET": EscapeTile,
	"GT": GameTile,
	"ST": StartTile,
	"RT": RoofTile,
	"BT": BasementTile,
	"  ": None
	}

world_map = []
start_tile_location = None
gas_placed = 0
fartsmell_placed = 0
trader_placed = 0

def parse_world_dsl():
	if not is_valid_dsl(world_dsl):
		raise SyntaxError("Invalid DSL!")
	dsl_lines = world_dsl.splitlines()
	dsl_lines = [x for x in dsl_lines if x]
	for y, dsl_row in enumerate(dsl_lines):
		row = []
		dsl_cells = dsl_row.split("|")
		dsl_cells = [c for c in dsl_cells if c]
		for x, dsl_cell in enumerate(dsl_cells):
			tile_type = tile_type_dict[dsl_cell]
			if tile_type == StartTile:
				global start_tile_location
				start_tile_location = x,y
			row.append(tile_type(x,y) if tile_type else None)
		world_map.append(row)
					   
def tile_at(x,y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None

player_types = {
    "a":"disgruntled employee",
    "b":"kool-aid drinker",
    "c":"rotten kid",
    "d":"thief"
    }
