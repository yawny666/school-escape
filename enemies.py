# need more enemies
from random import randint

import items

class Enemy:

    def __init__(self):
        self.is_aggro = 0
        self.items = []

    def is_alive(self):
        return self.health > 0


class Administrator(Enemy):

    def __init__(self):
        self.name = "Administrator"
        self.health = 20
        self.damage = 10
        self.xp = 200
        super().__init__()
        if randint(0, 10) < 3:
            self.items.append(items.Philz())
        if randint(0, 10) < 5:
            self.items.append(items.Hundo())
        if randint(0, 10) < 5:
            self.items.append(items.Chips())
        if randint(0, 10) < 2:
            self.items.append(items.Knife("letter opener", "an awkward but pointed implement", 5, 15, 10))
        if randint(0, 10) < 2:
            self.items.append(items.Implement("ball point pen", "you could poke somebody's eye out", 3, 25, 10))


class Scrub(Enemy):

    def __init__(self):
        self.name = "Scrub"
        self.health = 5
        self.damage = 3
        self.xp = 100
        super().__init__()
        if randint(0, 1) < 1:
            self.items.append(items.Dollar())
        if randint(0, 3) < 1:
            self.items.append(items.Ruler())


class Chupacabra(Enemy):

    def __init__(self):
        self.name = "Chupacabra"
        self.health = 10
        self.damage = 10
        self.xp = 100
        super().__init__()
        if randint(0, 1) < 1:
            self.items.append(items.Dollar())
        elif randint(0, 3) < 1:
            self.items.append(items.ButterKnife())


class Teacher(Enemy):

    def __init__(self):
        self.name = "Teacher"
        self.health = 20
        self.damage = 10
        self.xp = 200
        super().__init__()
        if randint(0, 4) < 1:
            self.items.append(items.Diaper())
        if randint(0, 4) < 1:
            self.items.append(items.Dollar())
        if randint(0, 5) < 1:
            self.items.append(items.Implement("ball point pen", "you could poke somebody's eye out", 3, 25, 10))
        if randint(0, 4) < 1:
            self.items.append(items.Twenty())
        if randint(0, 5) < 1:
            self.items.append(items.Ruler())


class Janitor(Enemy):

    def __init__(self):
        self.name = "Janitor"
        self.health = 50
        self.damage = 15
        self.xp = 350
        super().__init__()
        if randint(0, 1) < 1:
            self.items.append(items.Dollar())
        if randint(0, 1) < 1:
            self.items.append(items.Loot("rat trap",15))
        if randint(0, 1) < 1:
            self.items.append(items.Loot("pack of cigarettes",25))
        if randint(0, 1) < 1:
            self.items.append(items.Loot("kratom pills",50))
        if randint(0, 1) < 1:
            self.items.append(items.Implement("string mop","a stinky, sloppy, damp mess", 5, 5, 10))


class Bully(Enemy):

    def __init__(self):
        self.name = "Bully"
        self.health = 100
        self.damage = 20
        self.xp = 750
        super().__init__()
        if randint(0, 1) < 1:
            self.items.append(items.Twenty())
        if randint(0, 2) < 1:
            self.items.append(items.Iphone())


class Headmaster(Enemy):

    def __init__(self):
        self.name = "Headmaster"
        self.health = 350
        self.damage = 40
        self.xp = 2000
        super().__init__()
        if randint(0, 10) < 7:
            self.items.append(items.Iphone())
        if randint(0, 10) < 5:
            self.items.append(items.Laptop())
        if randint(0, 10) < 5:
            self.items.append(items.Hundo())
        if randint(0, 10) < 5:
            self.items.append(items.Hundo())
        if randint(0, 10) < 5:
            self.items.append(items.Hundo())
        if randint(0, 10) < 5:
            self.items.append(items.Hundo())
        if randint(0, 10) < 5:
            self.items.append(items.Hundo())
        if randint(0, 10) < 5:
            self.items.append(items.Hundo())
        if randint(0, 10) < 5:
            self.items.append(items.Iwatch())
