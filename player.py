import os
from colorama import Fore, Style, init
from random import randint

import world 
import items

init(autoreset=True)

class Player:

    def __init__(self,description,type):
        #self.items = []
        self.loot = []  # unusable but tradeable items
        self.objects = []  # usable objects, no value 
        self.consumables = []
        self.weapons = []
        self.consumables.append(items.CrustyBread())
        self.weapons.append(items.ButterKnife())
        self.weapon = self.weapons[0]
        self.max_health = 100
        self.health = 50
        self.strength = 12
        self.dmg_bonus = 0
        self.cash = 10
        self.level = 1
        self.xp = 0
        self.type = type
        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.description = description
        self.victory = False
        self.map = []

        # initialize player's map
        for level in world.world_map:
            row = [] 
            for cell in level:
                celltype = cell.__class__.__name__
                if celltype == "StartTile":
                    row.append('X')
                elif celltype == "GameTile" or \
                     celltype == "BasementTile" or \
                     celltype == "RoofTile": 
                    row.append('O')
                elif celltype == "EscapeTile":
                    row.append('E')
                else:
                    row.append(' ')
            self.map.append(row)
        update_map(self,self.x,self.y)
        
    def total_items(self):
    	return len(self.loot) + len(self.objects) + len(self.consumables) + len(self.weapons)

    def draw_map(self):
        print(' ----------------------------------')
        print('|                                  |')
        print('|                                  |')
        for j, level in enumerate(self.map):
            level_string = "|       "
            for i, cell in enumerate(level):
                if i == self.x and j == self.y:
                    level_string += 'X '
                elif cell == 'X':
                    level_string += '* '
                elif cell == 'e':
                    level_string += 'E '
                elif cell == 'x':
                    level_string += 'o '
                else:
                    level_string += '  '
            level_string += '       |'
            print(level_string)
        print('|                                  |')
        print('|   * = traveled  o = open path    |')
        print('|      X <-- current location      |')
        print(' ----------------------------------')

    def show_stats(self):
        print("--------------------------------- Stats")
        print("Level:\t{}".format(self.level))
        print("Strength:\t{}".format(self.strength))
        print("Dmg bonus:\t{}".format(self.dmg_bonus))
        print("XP:\t{}".format(self.xp))
        print("HP:\t{}/{}".format(self.health, self.max_health))


    def loot_value(self):
        val = 0
        for item in self.loot + self.consumables + self.weapons:
            val += item.value
        return int(val)

    def show_loot(self):
        if len(self.loot) > 0:
            val = 0
            print("---------------------------------- Loot")
            for item in self.loot:
                print(str(item) + "\t$" + str(item.value))
                val += item.value
            print("Total loot value: ${}".format(val))
        print("Cash: ${}".format(self.cash))

    def show_weapons(self):
        if len(self.weapons) > 0:
            print("------------------------------- Weapons")
            for item in self.weapons:
                if item == self.weapon:
                    print("*", end=' ')
                print(item)
 
    def show_consumables(self):
        if len(self.consumables) > 0:
            print("------------------------- Healing Items")
            for item in self.consumables:
                print(item)
 
    def show_objects(self):
        if len(self.objects) > 0:
            print("------------------------------- Objects")
            for item in self.objects:
                print(item)
 
    def bump_level(self):
        new_level = (self.xp // 1000) + 1
        if new_level > self.level:
            print("All right! You leveled up!")
            self.level = new_level
            self.strength += 2
            self.dmg_bonus += 5
 	
    def show_status(self):
        print("***************************************")
        print("       {} ({})       ".format(self.description,self.type))
        print("***************************************")
        self.show_loot()
        self.show_weapons()
        self.show_consumables()
        self.show_objects()
        self.show_stats()
        print("***************************************")
        print("")
        room = world.tile_at(self.x, self.y)
        print(Fore.CYAN + room.describe())
        #for line in self.map:
        #    print(line)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        room = world.tile_at(self.x, self.y)
        update_map(self, self.x, self.y)
        print(Fore.CYAN + room.describe())

    def go_north(self):
        self.move(0, -1)

    def go_south(self):
        self.move(0, 1)

    def go_east(self):
        self.move(1, 0)

    def go_west(self):
        self.move(-1, 0)

    def equip_weapon(self):
        print("Choose a weapon to equip (* indicates currently selected weapon):")
        for i, item in enumerate(self.weapons, 1):
            star = "*" if item == self.weapon else ""
            print(
                star + " " + str(i) + ". " 
                + item.name + " (max dmg:" + str(item.damage) 
                + "|uses left:" + str(item.condition) + ")" + star
                )

        weaponChosen = False
        while not weaponChosen:
            try:
                choice = input("Enter weapon number (0 to cancel): ")
                if choice != '0':
                    self.weapon = self.weapons[int(choice) - 1]
                print("You are wielding the {}.".format(self.weapon))
                weaponChosen = True
            except (ValueError, IndexError):
                print("That's not a valid choice!")
        room = world.tile_at(self.x, self.y)
        print(Fore.CYAN + room.describe())


    def move_to_inventory(self, item):
        if self.total_items() >= self.strength and not item.iscash:
            print(Fore.MAGENTA + "\nYou can't carry any more!\n")
            return False
        else:
            if isinstance(item, items.Consumable):
                self.consumables.append(item)
            elif isinstance(item, items.Usable):
                self.objects.append(item)
            elif isinstance(item, items.Loot):
                if item.iscash:
                    self.cash += item.value
                else:
                    self.loot.append(item)
            elif isinstance(item, items.Weapon):
                self.weapons.append(item)
            return True


    def attack(self):
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        enemy.is_aggro = 1  #enemy is now aggro'ed
        if self.weapon == None:
            dmg = randint(0,3 + self.dmg_bonus)
            self.health -= 1
            enemy.health = max(0, enemy.health - dmg)
            msg = "With no weapons equipped, you try to punch the " + enemy.name
            msg += " with your fists, doing "+ str(dmg) + " damage! **\n"
            msg += "The " + enemy.name + " has " + str(enemy.health) + " HP left."
            print(Fore.GREEN + Style.BRIGHT + msg) 
        elif self.weapon.condition <= 0:
            dmg = 0
            self.weapon.value = 0
            if self.weapon.name.count("broken") == 0:
                self.weapon.name += " (broken)"
            print("Your stupid weapon is broken! It does nothing!")
            print("If you want to fight with your fists, drop your weapon!")
        else:
            dmg = randint(0, (self.weapon.damage + self.dmg_bonus))
            enemy.health = max(0, enemy.health - dmg)
            self.weapon.condition -= 1
            self.weapon.value = self.weapon.value * self.weapon.condition / self.weapon.durability
            msg = "** You " + self.weapon.attack_verb() + " the " + enemy.name + " with your " + self.weapon.name + ","
            msg += "doing " + str(dmg) + " damage! **\n"
            msg += "The " + enemy.name + " has " + str(enemy.health) + " HP left."
            print(Fore.GREEN + Style.BRIGHT + msg) 
            if self.weapon.condition <= 0:
                if self.weapon.name.count("broken") == 0:
                    self.weapon.name += " (broken)"
                    self.weapon.value = 0
                print("Your stupid weapon broke! It's useless now!")
        if not enemy.is_alive():
            print("You killed the {}!".format(enemy.name))
            self.xp += enemy.xp
            self.bump_level()
            if enemy.items:
                print("Looks like the {} left you some schwag!".format(enemy.name))


    def loot_enemy(self):
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        if enemy.items:
            for i, item in enumerate(enemy.items, 1):
                print(str(i) + ".", item)
            itemLooted = False
            while not itemLooted:
                choice = input("Loot item ('0' to cancel, 'a' to loot all): ")
                try:
                    if choice == 'a':
                        enemyitems = [x for x in enemy.items]
                        for item in enemyitems:
                            print("You looted the {}.".format(item))
                            if self.move_to_inventory(item):
                                enemy.items.remove(item)
                    elif choice != '0':
                        print("You looted the {}!".format(item))
                        item = enemy.items[int(choice) - 1]
                        if self.move_to_inventory(item):
                            enemy.items.remove(item)
                    itemLooted = True
                except (ValueError, IndexError):
                    print("Invalid choice!")
        print(Fore.YELLOW + room.describe())


    def use_item(self):
    # usable items that counteract environmental hazards.
    # so far, only gas neutralizer and dust mask...
        room = world.tile_at(self.x, self.y)
        if len(self.objects) == 0:
            print("Got nothin' to use.")
        else:
            print("Available items:")
            for i, item in enumerate(self.objects, 1):
                print(str(i) + ".", item)
            itemChosen = False
            while not itemChosen:
                choice = input("Use item (0 to cancel): ")
                try:
                    item = self.objects[int(choice) - 1]
                    if isinstance(item,items.GasNeutralizer) and room.gas: 
                        print("The poison gas in this room has been neutralized.")
                        room.gas = 0
                        del self.objects[int(choice) - 1]
                    elif isinstance(item,items.DustMask) and room.fartsmell: 
                        print("Your dust mask successfully counteracts the suffocating shit odor in this room. You can breathe again!")
                        room.fartsmell = 0
                        del self.objects[int(choice) - 1]
                    else:
                        print("That item seems to have no effect. You don't feel so good.")
                    itemChosen = True 
                except ValueError:
                    print("That's not a valid choice!!")
        print(Fore.CYAN + room.describe())


    def heal(self):
        if len(self.consumables) == 0:
            print("Nothing to heal with.")
        else:
            print("Heal with which item?")
            for i, item in enumerate(self.consumables, 1):
                print(str(i) + ".", item)
            itemChosen = False
            while not itemChosen:
                choice = input("Enter item number from the list above ('0' to cancel, 'a' to use all): ")
                try:
                    if choice == 'a':
                        for item in self.consumables:
                            print("Yum, {}.".format(item))
                            self.health = min(self.max_health, self.health + item.healing)
                            self.consumables = [] 
                    elif choice != '0':
                        print("Yum, {}.".format(item))
                        item = self.consumables[int(choice) - 1]
                        self.health = min(self.max_health, self.health + item.healing)
                        self.consumables.remove(item)
                    itemChosen = True
                    print("Your HP is now {}.".format(self.health))
                except (ValueError, IndexError):
                    print("That's not a valid choice!")
        room = world.tile_at(self.x, self.y)
        print(Fore.CYAN + room.describe())

   
    def take_item(self):
        room = world.tile_at(self.x, self.y)
        if len(room.items) == 0:
            print("No items to take!")
        else:
            for i,item in enumerate(room.items, 1):
                print(str(i) + ".", item)
                itemChosen = False
            while not itemChosen:
                choice = input("Take item ('0' to cancel, 'a' to take all): ")
                try:
                    if choice == 'a':
                        roomitems = [x for x in room.items]
                        for item in roomitems:
                            print("Grabbing the {}...".format(item))
                            if self.move_to_inventory(item):
                                room.items.remove(item)
                    elif choice != "0":
                        item = room.items[int(choice) - 1]
                        if self.move_to_inventory(item):
                            room.items.remove(item)
                    itemChosen = True
                except (ValueError, IndexError):  
                    print("That's not a valid choice!")
        print(Fore.CYAN + room.describe())
 

    def drop_weapon(self):
        room = world.tile_at(self.x,self.y)
        for i, item in enumerate(self.weapons,1):
            print(str(i) + ".",item)
        itemDropped = False
        while not itemDropped: 
            choice = input("Drop weapon (press '0' to cancel, 'a' to drop all): ") 
            try:
                if choice == 'a':
                    for item in self.weapons:
                        room.items.append(item)
                        print("Dropping the {}...".format(item))
                    self.weapons = [] 
                    self.weapon = None 
                elif choice != '0':
                    item = self.weapons[int(choice) - 1]
                    if item == self.weapon:
                        self.weapon = None 
                    self.weapons.remove(item)
                    room.items.append(item)
                itemDropped = True
            except (ValueError, IndexError):
                print("That's not a valid choice!")
        print(Fore.CYAN + room.describe())

 
    def talk(self):
        room = world.tile_at(self.x, self.y)
        if hasattr(room, 'npc'):
            npc = room.npc
            if npc.is_trader():
                clear_screen()
                done = False
                while not done:
                    trader_offers = [] 
                    for item in self.weapons + self.loot + self.consumables:
                        trader_offers.append(item)
                    print(Fore.MAGENTA + "*****************************")
                    print(Fore.MAGENTA + "** {}'s TRADING POST **".format(npc.name))
                    print(Fore.MAGENTA + "*****************************")
                    print(Fore.GREEN + "{}".format(npc.speak()))
                    print("STORE ITEMS:")
                    for i, item in enumerate(npc.items, 1):
                        print(str(i) + '.', item,'\t$', item.value)
                    print("-----------------------------")
                    print("PAWN YR GEAR (up to ${} in total value):".format(npc.cash))
                    for i, item in enumerate(trader_offers, 1):
                        print(str(i) + '.', item, '\t$', int(trader_offers[i - 1].value * 0.6))
                    choice = input(Fore.YELLOW + "Buy or sell? (b to buy, s to sell, q to quit): ")

                    if choice == 'q':
                        done = True

                    elif choice == 'b':
                    # purchase transaction
                        if self.total_items() >= self.strength:
                            print(Fore.MAGENTA + "\nYou can't carry any more!\n")
                        else:
                            choice = int(input("Enter item to buy: ")) - 1
                            try:
                                if choice < 0:
                                    raise IndexError 
                                val = npc.items[choice].value
                                if self.cash >= val: 
                                    item = npc.items[choice]
                                    self.cash -= val 
                                    npc.cash += val 
                                    if isinstance(item, items.Consumable):
                                        self.consumables.append(item)
                                    elif isinstance(item, items.Loot):
                                        self.loot.append(item)
                                    elif isinstance(item, items.Weapon):
                                        self.weapons.append(item)
                                    npc.items.remove(item)
                                else:
                                    clear_screen()
                                    print(Fore.GREEN + "\nYou don't have enough cash bro!\n")
                            except (ValueError, IndexError):
                                print("Invalid choice!")

                    elif choice == 's':
                    # sale transaction
                        choice = int(input("Enter item to sell: ")) - 1
                        try:
                            if choice < 0 or choice == "":
                                raise IndexError 
                            val = int(trader_offers[choice].value * 0.6)
                            if npc.cash >= val:
                                self.cash += val
                                npc.cash -= val
                                item = trader_offers[choice]
                                if isinstance(item, items.Consumable):
                                    self.consumables.remove(item)
                                elif isinstance(item, items.Loot):
                                    self.loot.remove(item)
                                elif isinstance(item, items.Weapon):
                                    self.weapons.remove(item)
                                #trader_offers.remove(item)
                            else:
                                clear_screen()
                                print(Fore.GREEN + "I can't afford that shit! Buy some of my shit first!")
                        except (ValueError, IndexError):
                            print("Invalid choice!")

            else:
                print(Fore.GREEN + "{}".format(npc.speak()))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def update_map(player, i, j):
    player.map[j][i] = 'X'
    try:
        if i > 0:
            if player.map[j][i-1] == 'O':
                player.map[j][i-1] = 'x'
            if player.map[j][i-1] == 'E':
                player.map[j][i-1] = 'e'
        if i < len(player.map[j])-1:
            if player.map[j][i+1] == 'O':
                player.map[j][i+1] = 'x'
            if player.map[j][i+1] == 'E':
                player.map[j][i+1] = 'e'
        if j > 0:
            if player.map[j-1][i] == 'O':
                player.map[j-1][i] = 'x'
            if player.map[j-1][i] == 'E':
                player.map[j-1][i] = 'e'
        if j < len(player.map) -1:
            if player.map[j+1][i] == 'O':
                player.map[j+1][i] = 'x'
            if player.map[j+1][i] == 'O':
                player.map[j+1][i] = 'e'
    except IndexError:
        pass

