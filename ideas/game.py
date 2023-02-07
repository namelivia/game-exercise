import random

from constants import (
    ENTITY_TYPES,
    MAX_HEALTH,
    MAX_LEVEL,
    MAX_XP,
    NUM_ENTITIES,
    TYPE_A,
    TYPE_B,
    TYPE_C,
)


def get_precence_matrix():
    return {
        TYPE_A: [TYPE_B],
        TYPE_B: [TYPE_C],
        TYPE_C: [TYPE_A],
    }


def check_winner(entity1, entity2):
    return entity2.get_type() in get_precence_matrix()[entity1.get_type()]


def clash(entity1, entity2):
    first_wins = check_winner(entity1, entity2)
    if first_wins:
        print("Player 1 wins!!!")
        entity1.update_winner()
        entity2.update_loser(entity1.get_level())
    else:
        print("Player 2 wins!!!")
        entity2.update_winner()
        entity1.update_loser(entity2.get_level())


def create_random_entity(index):
    return Entity(
        index, random.choice(ENTITY_TYPES), random.randint(1, MAX_LEVEL), MAX_HEALTH
    )


class Entity:
    def __init__(self, index, entity_type, level, health):
        self.index = index
        self.entity_type = entity_type
        self.level = level
        self.health = MAX_HEALTH
        self.xp = 0

    def get_level(self):
        return self.level

    def get_type(self):
        return self.entity_type

    def print_entity(self):
        print(
            f"Index:{self.index} || Type:{self.entity_type} || Level:{self.level} || Health:{self.health} || XP:{self.xp}"
        )

    def update_loser(self, damage):
        print(f"The entity lost {damage} health points")
        self.health -= damage
        if self.health < 1:
            self.die()

    def update_winner(self):
        self.xp += 1
        print("The entity won 1 xp")
        if self.xp == MAX_XP:
            self.xp = 0
            if self.level < MAX_LEVEL:
                print("The entity leveled up")
                self.level += 1
            else:
                print("The entity is on max level")

    def die(self):
        print("The entity died")


class Player:
    def __init__(self, name, automatic):
        self.name = name
        self.automatic = automatic
        self.entities = []
        for index in range(NUM_ENTITIES):
            self.entities.append(create_random_entity(index))

    def make_choice(self):
        print("==================================")
        print(f"It's player {self.name} turn. Select an option")
        print("==================================")
        if self.automatic:
            selection = random.randint(0, NUM_ENTITIES - 1)
            print(f"What entity?{selection}")
            return self.entities[selection]
        option = 0
        while option != "2":
            print("1.- List entities")
            print("2.- Select entity")
            print("==================================")
            option = input()
            if option == "1":
                self.print_entities()
        entity_number = input("What entity?")
        return self.entities[int(entity_number)]

    def print_entities(self):
        for index in range(NUM_ENTITIES):
            self.entities[index].print_entity()


class Game:
    def __init__(self):
        self.player_1 = Player("Player 1", False)
        self.player_2 = Player("Player 2", True)

    def start(self):
        self.print_welcome_banner()
        while True:
            self.turn()

    def turn(self):
        player1_choice = self.player_1.make_choice()
        player2_choice = self.player_2.make_choice()
        clash(player1_choice, player2_choice)

    def print_welcome_banner(self):
        print("==================================")
        print("Welcome to the simplest game ever")
        print("==================================")
        print()


if __name__ == "__main__":
    Game().start()
