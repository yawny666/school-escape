'''SchoolEscape RPG
By John Berliner
PARTIAL TO DO:
- make starting classes of players
- XP for killing/fighting
- str points for inventory
'''

import os
import time
import pickle
from collections import OrderedDict
from colorama import Fore, Style, init

import world
import items
from player import Player

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')


def intro():
        clear_screen()
        print()
        print(f"{Fore.GREEN}#######################################")
        print("#####                             #####")
        print("#####        SCHOOL ESCAPE        #####")
        print("#####                             #####")
        print(f"{Fore.GREEN}#######################################")
        print()


def get_available_actions(room, player):
    actions = OrderedDict()
    print("\nChoose an action: ")
    if len(room.items)>0:
        action_adder(actions,'t',player.take_item, "Take (item)")
    if player.objects:
        action_adder(actions,'u',player.use_item, "Use (Item)")
    if player.health < 100 and player.consumables:
        action_adder(actions, 'h', player.heal, "Heal")
    if hasattr(room,'enemy') and not room.enemy.is_alive() and room.enemy.items:
        action_adder(actions, 'l', player.loot_enemy, "Loot (enemy)")
    if player.weapons:
        action_adder(actions,'p',player.equip_weapon, "Equip (weapon)")
        action_adder(actions, 'd', player.drop_weapon, "Drop (weapon)")
    if hasattr(room,'npc'):
        action_adder(actions,'/',player.talk, "Talk")
    if hasattr(room,'enemy') and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack,"Attack")
    action_adder(actions,'','',"----------")
    if world.tile_at(room.x, room.y - 1):
        action_adder(actions, 'n', player.go_north, "go North")
    if world.tile_at(room.x, room.y + 1):
        action_adder(actions, 's', player.go_south,"go South")
    if world.tile_at(room.x + 1, room.y):
        action_adder(actions, 'e', player.go_east,"go East")
    if world.tile_at(room.x - 1, room.y):
        action_adder(actions, 'w', player.go_west,"go West")
    action_adder(actions,'','',"----------")
    action_adder(actions,'m',player.draw_map, "Map")
    action_adder(actions,'z',player.show_status, "Status")
    return actions


def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    print(Fore.YELLOW + "{}: {}".format(hotkey, name))


def choose_action(room, player):
        action = None
        while not action:
                available_actions = get_available_actions(room,player)
                print(Style.RESET_ALL)
                action_input = input("Action: ")
                action = available_actions.get(action_input)
                print(Style.RESET_ALL)
                if action:
                        action()
                else:
                        if action_input in ['n','s','e','w']:
                                print("You can't go that way!")
                        else:
                                print("Invalid action!")
                if room.gas:
                        player.health -= 3


def update_high_scores(player,score):
    try:
        with open('hs.txt','rb') as f:
            high_scores = pickle.load(f)
    except:
        high_scores = []

    high_scores.append((score,player))
    high_scores = sorted(high_scores,reverse = True)[:10]
    with open('hs.txt','wb') as f:
        pickle.dump(high_scores, f)

    print(f'{Fore.GREEN}****************************')
    print('*****    HIGH SCORES   *****')
    print(f'{Fore.GREEN}****************************')
    for num,name in high_scores:
        displayname = name.upper() + "                "
        print(displayname[:18] + '\t' + str(num))


def play():
    world.parse_world_dsl()
    print("You are awakening as if from a dream.")
    print("Where are you? What is this place?")
    player_name = input("You barely remember your name...type it here: ")
    time.sleep(0.5)
    print()
    print("What sort of person are you, anyway?")
    type_chosen = False
    while not type_chosen:
        try:
            for key in world.player_types.keys():
                print("(" + key +") " + world.player_types[key])
            player_type = input("Your choice? ")
            if player_type in ['a','b','c','d']:
                type_chosen = True
                player_type = world.player_types[player_type] 
        except (ValueError, IndexError):
            print("That's not a valid choice!")      
    time.sleep(0.5)
    print("Slowly, your vision begins to come into focus...\n ")
    time.sleep(1)
    player = Player(player_name,player_type)
    dead = False
    room = world.tile_at(player.x,player.y)
    print(room.describe())

    while not dead and not player.victory:
        room = world.tile_at(player.x,player.y)
        room.modify_player(player)
        if player.health <= 0:
            dead = True
            print("xXx YOU DIED xXx")
        elif not player.victory:
            choose_action(room,player)
    if isinstance(room, world.EscapeTile):
        print ("You escaped the school with cash and prizes valued at ${}!".format(player.loot_value()))
        update_high_scores(player_name,player.loot_value())

intro()
play()
