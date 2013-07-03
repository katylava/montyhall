#!/usr/bin/env python

import random

NUM_DOORS = 3
NUM_TRIALS = 100
VERBOSE = False


class MontyHallDoors(object):
    DOOR_NUM_IDX = 0
    DOOR_STATE_IDX = 1
    DOOR_PRIZE_IDX = 2

    def __init__(self, num_doors=3):
        self.num_doors = num_doors
        self.setup()

    def setup(self):
        numbers = range(1, self.num_doors + 1) # range() leaves endpoint out of list
        states = ['closed' for i in numbers]
        prizes = ['goat' for i in numbers]
        prizes[random.randint(0, numbers[-2])] = 'car'

        self.doors = [list(z) for z in (zip(numbers, states, prizes))]
        self.door_dict = dict((d[0],d) for d in self.doors)

        self.chosen_doors = []
        self.prize = None

    @property
    def all_goat_doors(self):
        return [d for d in self.doors if d[self.DOOR_PRIZE_IDX] is 'goat']

    @property
    def unchosen_doors(self):
        return [d for d in self.doors if d not in self.chosen_doors and d[self.DOOR_STATE_IDX] is not 'open']

    @property
    def unchosen_goat_doors(self):
        return [d for d in self.unchosen_doors if d in self.all_goat_doors]

    @property
    def car_door(self):
        door = [d for d in self.doors if d[DOOR_PRIZE_IDX] is 'car']
        return door[0]

    def show_state(self):
        return {
            'opened': [d for d in self.doors if d[self.DOOR_STATE_IDX] is not 'closed'],
            'closed': [d for d in self.doors if d[self.DOOR_STATE_IDX] is 'closed'],
            'chosen': self.chosen_doors[-1],
        }

    def open_door(self, door):
        if isinstance(door, int):
            door = self.door_dict[door]
        door[self.DOOR_STATE_IDX] = 'open'
        return door[self.DOOR_PRIZE_IDX]

    def choose_door(self, choice=None):
        if not choice:
            choice = random.choice(self.unchosen_doors)
        else:
            choice = self.door_dict(choice)
            if choice not in self.unchosen_doors:
                print('Door not available')
                return
        self.chosen_doors.append(choice)
        return choice



class MontyHallGame(object):

    def __init__(self, num_doors=3):
        self.doors = MontyHallDoors(num_doors)

    def player_chooses_door(self, door=None):
        choice = self.doors.choose_door(door)
        return choice

    def host_reveals_goat(self):
        options = self.doors.unchosen_goat_doors
        door = random.choice(options)
        prize = self.doors.open_door(door[self.doors.DOOR_NUM_IDX])
        return door

    def host_reveals_prize(self):
        door = self.doors.chosen_doors[-1]
        self.doors.open_door(door)
        prize =  door[self.doors.DOOR_PRIZE_IDX]
        return door

    def player_keeps_choice(self):
        pass

    def player_switches_choice(self, door=None):
        return self.doors.choose_door(door)


    def run(self):
        self.doors.setup()

        if VERBOSE:
            print('-----------------------')

        choice = self.player_chooses_door()
        if VERBOSE:
            print("Player chooses door #{}".format(choice[self.doors.DOOR_NUM_IDX]))

        door = self.host_reveals_goat()
        if VERBOSE:
            print(
                "Host opens door #{} and reveals a {}".format(
                    door[self.doors.DOOR_NUM_IDX],
                    door[self.doors.DOOR_PRIZE_IDX]
                )
            )

        if random.choice([True, False]):
            choice = self.player_switches_choice()
            if VERBOSE:
                print(
                    "Player switches from door #{} to #{}".format(
                        self.doors.chosen_doors[-2][self.doors.DOOR_NUM_IDX],
                        choice[self.doors.DOOR_NUM_IDX]
                ))
        else:
            self.player_keeps_choice()
            if VERBOSE:
                print("Player keeps choice of door #{}".format(
                    self.doors.chosen_doors[-1][self.doors.DOOR_NUM_IDX]
                ))

        door = self.host_reveals_prize()
        if VERBOSE:
            print(
                "Host opens chosen door #{} and reveals a {}".format(
                    door[self.doors.DOOR_NUM_IDX],
                    door[self.doors.DOOR_PRIZE_IDX]
                )
            )

        prize = door[self.doors.DOOR_PRIZE_IDX]
        switched = len(self.doors.chosen_doors) > 1
        return switched, prize



class MontyHallRunner(object):

    def __init__(self, num_doors=3, num_trials=100):
        game = MontyHallGame(num_doors)

        switched_game_prizes = []
        kept_game_prizes = []
        for n in range(num_trials):
            switched, prize = game.run()
            if switched:
                switched_game_prizes.append(prize)
            else:
                kept_game_prizes.append(prize)

        switched_games = len(switched_game_prizes)
        kept_games = len(kept_game_prizes)

        switched_game_cars = switched_game_prizes.count('car')
        switched_game_goats = switched_game_prizes.count('goat')
        kept_game_cars = kept_game_prizes.count('car')
        kept_game_goats = kept_game_prizes.count('goat')

        print(
        "=================================================\n"
        "SWITCHED: {} games, {} cars, {} goats\n"
        "KEPT: {} games, {} cars, {} goats\n"
        "Switched win ratio: {:0.4f}\n"
        "Kept win ratio: {:0.4f}\n".format(
            switched_games,
            switched_game_cars,
            switched_game_goats,
            kept_games,
            kept_game_cars,
            kept_game_goats,
            float(switched_game_cars)/switched_games,
            float(kept_game_cars)/kept_games
        ))


if __name__ == '__main__':
    from optparse import OptionParser
    usage = "Usage: %prog --doors 3 --iterations 100 --verbose"
    parser = OptionParser(usage=usage)
    parser.add_option('-d', '--doors', type='int', default=NUM_DOORS,
                      help="Number of doors for game")
    parser.add_option('-i', '--iterations', type='int', default=NUM_TRIALS,
                      help="Number of iterations to trial")
    parser.add_option('-v', '--verbose', action='store_true')
    options, args = parser.parse_args()

    VERBOSE = options.verbose
    MontyHallRunner(options.doors, options.iterations)
