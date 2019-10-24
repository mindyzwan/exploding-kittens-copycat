
# NEXT TO DO:
# Add default computer activity
# Add nope capability
# refactor activate_card
# If card doesn't apply, error message
# 2nd turn after attack on first of two turns doesn't happen


import random
import os
import re


class Card():
    types = {
        'hairy_potato_cat': {
            'name': 'Hairy Potato Cat',
            'phrase': ['*silent stare*'],
            'type': 'pair_card',
            'start_count': 4
        },
        'tacocat': {
            'name': 'Tacocat',
            'phrase': ['I am a palindrome!'],
            'type': 'pair_card',
            'start_count': 4
        },
        'rainbow_ralphing_cat': {
            'name': 'Rainbow-Ralphing Cat',
            'phrase': ['HRNNGGGG'],
            'type': 'pair_card',
            'start_count': 4
        },
        'cattermelon': {
            'name': 'Catttermelon',
            'phrase': ['Hack thoop!'],
            'type': 'pair_card',
            'start_count': 4
        },
        'beard_cat': {
            'name': 'Beard Cat',
            'phrase': ['*rustles*'],
            'type': 'pair_card',
            'start_count': 4
        },
        'defuse': {
            'name': 'Defuse',
            'phrase': [
                'via laser pointer',
                'via catnip sandwiches',
                'via participation in kitten yoga',
                'via 3am flatulence', 'via belly rubs',
                'via kitten therapy'
                ],
            'type': 'defuse',
            'start_count': 0
        },
        'exploding_kitten': {
            'name': 'Exploding Kitten',
            'phrase': [
                '*gnaw, gnaw, gnaw* (on electrical wires)',
                '\'zzzz\' (Warp core + cat hair = BAD)',
                '*cat scampers across nuke detonation button*',
                '*cat muches on TNT*'
                ],
            'type': 'exploding_kitten',
            'start_count': 0
        },
        'skip': {
            'name': 'Skip',
            'phrase': [
                'Crab walk with some crabs',
                'Engage the hypergoat',
                'Don a portable cheetah butt',
                'Commandeer a bunnyraptor'
                ],
            'type': 'skip',
            'start_count': 4
        },
        'shuffle': {
            'name': 'Shuffle',
            'phrase': [
                'An electromagnetic pomeranian storm rolls in from the east',
                'Abracrab Lincoln is elected president',
                'A plague of bat farts descends from the sky',
                'A trandimensional litter box materializes'
                ],
            'type': 'shuffle',
            'start_count': 4
        },
        'see_the_future': {
            'name': 'See the Future',
            'phrase': [
                'Rub the belly of a pig-a-corn',
                'Summon the mantis shrimp',
                'Feast upon a unicorn enchilada and gain its enchilada powers',
                'Ask the all-seeing goat wizard',
                'Deploy the special-ops bunnies'
                ],
            'type': "see_the_future",
            'start_count': 5
        },
        'attack': {
            'name': 'Attack',
            'phrase': [
                'Fire the crab-a-pult',
                'Deploy the thousand-year back hair',
                'Awaken the bear-o-dactyl',
                'Unleash the catterwocky'
                ],
            'type': 'attack',
            'start_count': 4
        },
        'favor': {
            'name': 'Favor',
            'phrase': [
                'Rub peanut butter on your belly button & make new friends',
                'Take your friends beard-sailing on your beard boat',
                'Get enslaved by party squirrels',
                'Ask for a back hair shampoo'
                ],
            'type': 'favor',
            'start_count': 4
        }
    }

    pair_types = ['Hairy Potato Cat', 'Cattermelon', 'Rainbow-Ralphing Cat', 'Beard Cat', 'Tacocat']

    def __init__(self, value):
        self.name = self.types[value]['name']
        self.phrase = random.choice(self.types[value]['phrase'])
        self.function = self.types[value]['type']

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Deck():
    def __init__(self):
        card_types = list(Card.types.keys())
        self.deck = self.new_deck(card_types)

    def print_cards(self):
        print([card for card in self.deck])

    def new_deck(self, card_types):
        deck = []
        for card_type in card_types:
            for _ in range(Card.types[card_type]['start_count']):
                deck.append(Card(card_type))

        random.shuffle(deck)
        return deck

    def deal_starting_hand(self, hand):
        for _ in range(4):
            hand.cards.append(self.deck.pop())
        hand.cards.append(Card('defuse'))

    def insert_remaining_defuse_cards(self):
        self.deck.append(Card('defuse'))
        self.deck.append(Card('defuse'))
        random.shuffle(self.deck)

    def insert_exploding_kitten_cards(self):
        self.deck.append(Card('exploding_kitten'))
        self.deck.append(Card('exploding_kitten'))
        random.shuffle(self.deck)

    def draw_card(self, hand):
        hand.cards.append(self.deck.pop())

    def shuffle(self):
        random.shuffle(self.deck)


class Player():
    def __init__(self, hand):
        self.hand = hand


class Human(Player):
    def __init__(self, hand):
        super().__init__(hand)
        self.name = 'Mindy'
        self.species = 'Human'
        # self.name = input('What\'s your name? ')


class Computer(Player):
    def __init__(self, hand):
        super().__init__(hand)
        self.name = random.choice(
            ['R2D2', 'C-3PO', 'HAL', 'GWB-666', 'Alexa', 'Siri', 'Cortana']
            )
        print(f'You\'ll be playing against {self.name}.')
        self.species = 'Computer'


class Hand():
    def __init__(self, deck):
        self.deck = deck
        self.cards = []
        self.get_starting_hand()

    def get_starting_hand(self):
        self.deck.deal_starting_hand(self)

    def sort_hand(self):
        self.cards = sorted(self.cards, key=lambda x: x.name)

    def show_cards(self):
        self.sort_hand()
        print('\nYour Hand:')
        card_number = 1
        for card in self.cards:
            print(f'{card_number} : {card}')
            card_number += 1
        print('')

    def draw_new_card(self):
        self.deck.draw_card(self)

    def play_card(self, card_index):
        self.cards.pop(card_index)

    def steal_card(self, stolen_card):
        self.cards.append(stolen_card)

    def get_card_stolen(self, card_index):
        return self.cards.pop(card_index)

    # def return_index_action_tuple_array(self):
    #   tuple_array = []
    #   index = 0

    #   for card in self.cards:
    #     tuple_array.append((card.function, index))
    #     index += 1

    #   return tuple_array


class Turn():
    def __init__(self, player, opponent, game):
        self.skip_turn = False
        self.player = player
        self.game = game
        self.opponent = opponent
        self.extra_opponent_turn = 0
        print(f'\n\n\n\n***  {player.name.upper()}\'S TURN  ***')

    def activate_card(self, card_index):
        card = self.player.hand.cards[card_index]
        hand = self.player.hand

        print(f'\n\n{self.player.name} played {card.name} ({card.phrase})')

        if card.function == 'skip':
            self.skip_turn = True
            hand.play_card(card_index)
        elif card.function == 'pair_card':
            if self.check_pair_exist(card):
                self.play_pair(card_index)
            else:
                print('No matching pair found! Card goes back into your hand')
        elif card.function == 'shuffle':
            self.game.deck.shuffle()
            hand.play_card(card_index)
        elif card.function == 'see_the_future':
            self.play_future(self.game)
            hand.play_card(card_index)
        elif card.function == 'attack':
            self.play_attack(self.game)
            hand.play_card(card_index)
        elif card.function == 'favor':
            random_index = random.randint(0, len(self.opponent.hand.cards) - 1)
            self.play_favor(random_index)
            hand.play_card(card_index)
        else:
            print('\nThat card can\'t be used right now!')

    def play_attack(self, game):
        self.skip_turn = True
        self.extra_opponent_turn += 1
        print('\n\nYou do not need to draw this turn!')
        print(f'{self.opponent.name} now has to take an extra turn\n\n')

    def play_future(self, game):
        next_three = game.deck.deck[-1:-4:-1]

        if self.player.species == 'Human':
            print('\nThe next three cards are:')
            for card in next_three:
                print(f'\t - {card.name}')
        # else:
        #   if next_three[0].function == 'exploding_kitten'
        #     self.play_attack

    def check_pair_exist(self, first_card):
        pair_count = 0
        for card in self.player.hand.cards:
            if card.name == first_card.name:
                pair_count += 1
            if pair_count >= 2:
                return True
        return False

    def play_pair(self, first_card_index):
        hand = self.player.hand
        hand.play_card(first_card_index)
        first_card = hand.cards[first_card_index]

        second_card_index = 0
        for card in hand.cards:
            if card.name == first_card.name:
                break
            second_card_index += 1

        hand.play_card(second_card_index)
        print(
            f'\nA pair has been found! {self.player.name} steals a card.')
        random_card = random.randint(0, len(self.opponent.hand.cards) - 1)
        self.steal_card(random_card)

    def play_favor(self, card_index):
        self.steal_card(card_index)

    def steal_card(self, card_index):
        stolen_card = self.opponent.hand.get_card_stolen(card_index)
        print(f'Card received: {stolen_card}')
        self.player.hand.steal_card(stolen_card)

    def return_defuse_card_index(self, game):
        card_index = 0

        for card in self.player.hand.cards:
            if card.name == 'Defuse':
                return card_index
            card_index += 1

        return None

    def defuse(self, card_index):
        self.game.exploded = False
        card_phrase = self.player.hand.cards[card_index].phrase
        self.player.hand.play_card(card_index)
        self.player.hand.play_card(-1)
        print(f'\t{self.player.name} DEFUSED THE KITTEN, {card_phrase}\n\n')

    def attack_end(self):
        for _ in range(self.extra_opponent_turn):
            
            self.game.take_turn(self.opponent)

    def end_turn(self):
        self.player.hand.draw_new_card()
        if self.player.hand.cards[-1].name == 'Exploding Kitten':
            self.game.exploded = True
            defuse_card_index = self.return_defuse_card_index(self.game)
            if defuse_card_index is not None:
                self.defuse(defuse_card_index)


class ComputerTurn(Turn):
    def __init__(self, player, opponent, game):
        super().__init__(player, opponent, game)
        self.play_cards()
        self.end_turn()
        self.next_three_cards = []

    def end_turn(self):
        super().end_turn()
        print(f'\n- {self.player.name} drew a card -\n')
        print('\n---------------------------\n')

    def play_cards(self):
        self.player.hand.show_cards()
        while self.get_playable_card() is not None:
            print('There is a playable card')
            card_index = self.get_playable_card()
            self.activate_card(card_index)
            input('Press enter to continue ')

    def get_playable_card(self):
        functions = [card.function for card in self.player.hand.cards]

        # conditional_1 = 'see_the_future' in functions and
        # ('attack' in functions or 'skip' in functions or 'shuffle'
        # in functions)
        play_2 = self.check_pair()								
        play_3 = 'favor' in functions
        play_4 = 'attack' in functions

        if play_3:
            return functions.index('favor')
        elif play_2:
            return self.get_pair_index() 
        elif play_4:
            return functions.index('attack')

        # def play_future_sequence(self, functions_list):
        #       see_the_future_index = functions.index('see_the_future')
        #       attack_index = functions.index('attack')
        #       skip_index = functions.index('skip')
        #       shuffle_index = functions.index('shuffle')
    def check_pair(self):
        pair_cards_in_hand = [card.name for card in self.player.hand.cards if card.function == 'pair_card']

        for card_template in Card.pair_types:
            if pair_cards_in_hand.count(card_template) >= 2:
                return True 
        return False

    def get_pair_index(self):
        pair_cards_in_hand = [card.name for card in self.player.hand.cards if card.function == 'pair_card']
        names = [card.name for card in self.player.hand.cards]

        for card_template in Card.pair_types:
            if pair_cards_in_hand.count(card_template) >= 2: 
                return names.index(card_template)

				




class HumanTurn(Turn):
    def __init__(self, player, opponent, game):
        super().__init__(player, opponent, game)
        self.player = player
        self.game = game

        self.play_cards()
        if not self.skip_turn:
            self.end_turn()
        self.attack_end()

    def play_cards(self):
        play_card = True
        num_cards = len(self.player.hand.cards)
        playable_cards = list(range(1, num_cards + 1))

        while play_card:
            response = self.get_input()

            if response == 'q':
                self.game.quit = True
                print('Quitting...')
                break
            elif re.match(r'[\d]', response) and int(response) in playable_cards:
                self.activate_card(int(response) - 1)
                input('\nPress enter to continue ')
            else:
                break

        

    def get_input(self):
        self.player.hand.show_cards()
        print(f'To play a card, enter the corresponding digit above')
        print(f'To end your turn by drawing a card, press enter')
        print(f'Enter \'q\' to quit')
        response = input('\n\tEnter response > ')
        return response

    def end_turn(self):
        if self.game.quit:
            return
        super().end_turn()
        print(f'\n- You drew: {self.player.hand.cards[-1]} -\n\n\n')

        for _ in range(self.extra_opponent_turn):
            ComputerTurn(self.opponent, self.player, self.game)
            if self.game.exploded:
                self.game.explode(self.opponent)


class Game():
    def __init__(self):
        self.deck = Deck()
        
        print('Welcome to Exploding Kittens!')

        self.human_hand = Hand(self.deck)
        self.computer_hand = Hand(self.deck)

        self.human = Human(self.human_hand)
        self.computer = Computer(self.computer_hand)

        self.exploded = False
        self.quit = False
        input(f'\n\nPress enter to continue  ')
        

    def list_rules(self):
        pass

    def explode(self, player):
        print('\n\n')
        print(player.hand.cards[-1].phrase)
        print('BOOOOOOOOOOMMMMMMM!!!!!\n\n')
        print(f'{player.name} drew an Exploding Kitten and lost!\n\n')

    def take_turn(self, player):
        if player.species == 'Human':
            HumanTurn(player, self.computer, self)
        else:
            ComputerTurn(player, self.human, self)
        if self.exploded:
            self.explode(player)

    def play(self):
        for _ in range(5):
            self.deck.insert_exploding_kitten_cards()

        while not self.exploded:
            for player in [self.human, self.computer]:
                self.take_turn(player)
                if self.exploded:
                    break
                if self.quit:
                    return

            input(f'Press enter to continue ')
            


new_game = Game()
new_game.play()
# print('')
# new_game.human_hand.show_cards()
# print('')
# new_game.computer_hand.show_cards()
# print('')
# new_game.deck.print_cards()
# print('')
# new_game.play()
# new_game.deck.print_cards()
