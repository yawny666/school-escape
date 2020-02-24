from random import choice

import items


class NPC:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return(self.name)

    def is_trader(self):
        return False

    def speak(self):
        return self.name + " says: " + choice(self.dialogue)

class Ruby(NPC):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.dialogue = [
            "I'm sorry I'm sorry I'm sorry!",
            "I'm just a little, you know, I guess I'm just a little cuckoo.",
            "I don't know why I'm getting all upset.",
            "I'm sorry, I'm just a little screwed up I guess."
            "You know what? I'm so done."
        ]

class Rando(NPC):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.dialogue = [
            "My mom pays your salary.",
            "Have you filled out your Folio goals yet?",
            "Would you mind shining a Folio spotlight on me?",
            "DAFUQ?",
            "Get with the program or get out.",
            "What are your plans for DEI PD?",
            "I'm redefining my relationship with time.",
            "The process is the journey is the learning.",
            "I scaffolded your mother.",
            "Play is work.",
            "U mad bro?"
        ]

class Trader(NPC):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.cash = 100
        self.items = [
            items.CrustyBread(), 
            items.CrustyBread(), 
            items.Chips(), 
            items.Chips(), 
            items.Chips(), 
            items.Chips(), 
            items.Implement("hot glue gun", "stolen from the art room", 5, 35, 50),
            items.Knife("steak knife", "a pointy serrated knife", 10, 15, 25),
            items.Knife("potato peeler", "a dull fruit peeler", 5, 5, 5)
        ]
        self.dialogue = [
            "I got guns, knives, and candy.",
            "Diddd you brinnnnng me my precioussss?",
            "How much you got?",
            "Yo Richie Rich.",
            "Hey kid, you need a cigar?",
            "Tryna make some money out here."
        ]

    def is_trader(self):
        return True
