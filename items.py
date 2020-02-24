from random import choice

class Weapon:

    iscash = False
    
    def __init__(self,name,description,durability,damage,value):
        self.name = name
        self.description = description
        self.durability = durability
        self.condition = durability
        self.damage = damage
        self.value = value
        self.verbs = ['attack']

    def __str__(self):
        return(self.name)

    def attack_verb(self):
        return choice(self.verbs)
   

class Implement(Weapon):

    verbs = ['smack','whack','pwn','slap','doink']
    def __init__(self,name,description,durability,damage,value):
        super().__init__(name,description,durability,damage,value)

class Ruler(Implement):

    def __init__(self):
        self.name = "Ruler"
        self.description = "An ordinary classroom ruler useful for rapping young knuckles."
        self.durability = 5 
        self.condition = self.durability
        self.damage = 10
        self.value = 9 


class Scissors(Implement):

    def __init__(self):
        self.name = "Kids' Scissors"
        self.description = "Those stupid kids' scissors with the rounded tips."
        self.durability = 15 
        self.condition = self.durability
        self.damage = 5 
        self.value = 5 


class Knife(Weapon):
    verbs = ['stab','slice','doink','pierce']
    def __init__(self,name,description,durability,damage,value):
        super().__init__(name,description,durability,damage,value)


class ButterKnife(Knife):
    def __init__(self):
        self.name = "Butter Knife"
        self.description = "A dull, lame knife useful for spreading ointments." 
        self.durability = 6
        self.condition = self.durability
        self.damage = 10
        self.value = 10 


class Stiletto(Knife):
    def __init__(self):
        self.name = "Stiletto"
        self.description = "A small but extremely sharp blade."
        self.durability = 5 
        self.condition = self.durability
        self.damage = 50 
        self.value = 75 

class Machete(Knife):
    def __init__(self):
        self.name = "Machete"
        self.description = "A large blade designed for hacking coconuts"
        self.durability = 5 
        self.condition = self.durability
        self.damage = 90 
        self.value = 100 

class Hammer(Weapon):
    verbs = ['whap','smash','bludgeon','pound']
    def __init__(self,name,description,durability,damage,value):
        super().__init__(name,description,durability,damage,value)

class Mace(Hammer):
    def __init__(self):
        self.name = "Kitchen Mace"
        self.description = "An ordinary but sturdy butcher's mace."
        self.durability = 7 
        self.condition = self.durability
        self.damage = 75 
        self.value = 100 

class ClubMace(Mace):
    def __init__(self):
        self.name = "Old Club Mace"
        self.description = "A stout, brain-crushing hammer. The handle looks broken."
        self.durability = 3 
        self.condition = self.durability
        self.damage = 150 
        self.value = 100 

class MagicMace(Mace):
    def __init__(self):
        self.name = "Magic Mace"
        self.description = "A heavy mace lined with magic jewels."
        self.durability = 8 
        self.condition = self.durability
        self.damage = 200 
        self.value = 1000 


class Usable:

    iscash = False

    def __init__(self,name,value):
        self.name = name
        self.value = value

    def __str__(self):
        return "{}".format(self.name)


class GasNeutralizer(Usable):

    def __init__(self):
        self.name = "poison gas antidote"

    def __str__(self):
        return "{}".format(self.name)
 
class DustMask(Usable):

    def __init__(self):
        self.name = "Particulate matter mask"
    def __str__(self):
        return "{}".format(self.name)
 

#### CONSUMABLES ####
class Consumable:

    iscash = False

    def __init__(self,name,value):
        self.name = name
        self.value = value

    def __str__(self):
        return "{} (+{} HP)".format(self.name,self.healing)

class CrustyBread(Consumable):
    def __init__(self):
        self.name = "Crusty Bread"
        self.healing = 5
        self.value = 5 

class StringCheese(Consumable):
    def __init__(self):
        self.name = "String Cheese"
        self.healing = 5
        self.value = 5 

class Chips(Consumable):
    def __init__(self):
        self.name = "Bag of Chips"
        self.healing = 10
        self.value = 10

class GranolaBar(Consumable):
    def __init__(self):
        self.name = "Granola Bar"
        self.healing = 12
        self.value = 15

class Taco(Consumable):
    def __init__(self):
        self.name = "Taco"
        self.healing = 15
        self.value = 20

class Burrito(Consumable):
    def __init__(self):
        self.name = "Burrito"
        self.healing = 25
        self.value = 35

#### LOOT ITEMS ####
class Loot:

    iscash = False

    def __init__(self,name,value):
        self.name = name
        self.value = value

    def __str__(self):
        return "{}".format(self.name)

class Dollar(Loot):
    def __init__(self):
        self.name = "Dollar Bill"
        self.value = 1
        self.iscash = True

class Twenty(Loot):
    def __init__(self):
        self.name = "Twenty Dollar Bill"
        self.value = 20 
        self.iscash = True

class Hundo(Loot):
    def __init__(self):
        self.name = "Hundred Dollar Bill"
        self.value = 100 
        self.iscash = True

class Philz(Loot):
    def __init__(self):
        self.name = "Phil'Z Gift Card"
        self.value = 10 

class Diaper(Loot):
    def __init__(self):
        self.name = "Jumbo Pack of Depends"
        self.value = 5 

class Laptop(Loot):
    def __init__(self):
        self.name = "MacBook Air"
        self.value = 200

class Iphone(Loot):
    def __init__(self):
        self.name = "iPhone"
        self.value = 500

class Iwatch(Loot):
    def __init__(self):
        self.name = "iWatch"
        self.value = 800
