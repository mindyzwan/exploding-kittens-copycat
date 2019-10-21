
# NEXT TO DO:
# Add see the future capability
# Add attack capability
# Add default computer activity
# Add nope capability


import random
import os

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
      'phrase': ['via laser pointer', 'via catnip sandwiches', 'via participation in kitten yoga', 'via 3am flatulence', 'via belly rubs', 'via kitten therapy'],
      'type': 'defuse',
      'start_count': 0
    },
    'exploding_kitten': {
      'name': 'Exploding Kitten',
      'phrase': ['*gnaw, gnaw, gnaw* (on electrical wires, subsequently blowing up the house)', '\'zzzz\' (cat fell asleep on the warp core! Warp core + cat hair = BAD)', '*cat scampers across nuke detonation button*', '*cat muches on TNT*'],
      'type': 'exploding_kitten',
      'start_count': 0
    },
    'skip': {
      'name': 'Skip',
      'phrase': ['Crab walk with some crabs', 'Engage the hypergoat', 'Don a portable cheetah butt', 'Commandeer a bunnyraptor'],
      'type': 'skip',
      'start_count': 4
    },
    'shuffle': {
      'name': 'Shuffle',
      'phrase': ['An electromagnetic pomeranian storm rolls in from the east', 'Abracrab Lincoln is elected president', 'A plague of bat farts descends from the sky', 'A trandimensional litter box materializes'],
      'type': 'shuffle',
      'start_count': 4
    },
    'see_the_future': {
      'name': 'See the Future',
      'phrase': ['Rub the belly of a pig-a-corn', 'Summon the mantis shrimp', 'Feast upon a unicorn enchilada and gain its enchilada powers', 'Ask the all-seeing goat wizard', 'Deploy the special-ops bunnies'],
      'type': "see_the_future",
      'start_count': 5
    }
  }
  
  def __init__(self, value):
    self.name = self.types[value]['name']
    self.phrase = random.choice(self.types[value]['phrase'])
    self.function = self.types[value]['type']

  def __str__(self):
    return f'{self.name}'

  def __repr__(self):
    return f'{self.name}'

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
    self.name = random.choice(['R2D2', 'C-3PO', 'HAL', 'GWB-666', 'Alexa', 'Siri', 'Cortana'])
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
    print('---------------------------')
    print('Your Hand:')
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

class Turn():
  def __init__(self, player, opponent, game):
    self.skip_turn = False
    self.player = player
    self.game = game
    self.opponent = opponent
    print(f'{player.name.upper()}\'S TURN\n')

  def activate_card(self, card_index):
    card = self.player.hand.cards[card_index]
    hand = self.player.hand
    
    print(f'\n\n{self.player.name} played {card.name}.')
    print(f'{card.phrase}')
    if card.function == 'skip':
      self.skip_turn = True
      hand.play_card(card_index)
    elif card.function == 'pair_card':
      if self.check_pair_exist(card): self.play_pair(card_index)
    elif card.function == 'shuffle':
      self.game.deck.shuffle()
      hand.play_card(card_index)
    elif card.function == 'see_the_future':
      self.play_future(self.game)
      hand.play_card(card_index)


  def play_future(self, game):
    next_three = game.deck.deck[-1:-4:-1]

    if self.player.species == 'Human':
      print('\nThe next three cards are:')
      for card in next_three:
        print(card.name)
    
    input('\n\nPress enter to continue ')
        
    
  def check_pair_exist(self, first_card):
    pair_count = 0
    for card in self.player.hand.cards:
      if card.name == first_card.name: pair_count += 1
      if pair_count >= 2: return True
    return False

  def play_pair(self, first_card_index):
    hand = self.player.hand
    hand.play_card(first_card_index)
    first_card = hand.cards[first_card_index]

    second_card_index = 0
    for card in hand.cards:
      if card.name == first_card.name: break
      second_card_index += 1

    hand.play_card(second_card_index)
    print(f'\nA pair has been found! {self.player.name} gets to steal a card.')
    self.steal_card()

  def steal_card(self):
    opponent_hand = self.opponent.hand
    card_index = random.randint(0, len(opponent_hand.cards) - 1)
    stolen_card = opponent_hand.get_card_stolen(card_index)
    print(f'Stolen card: {stolen_card}')
    self.player.hand.steal_card(stolen_card)

  def check_for_defuse_card(self, game):
    card_index = 0

    for card in self.player.hand.cards:
      if card.name == 'Defuse':
        game.exploded = False
        card_phrase = self.player.hand.cards[card_index].phrase
        self.player.hand.play_card(card_index)
        print(f'\t{self.player.name} DEFUSED THE KITTEN, {card_phrase}\n\n')
      card_index += 1

  def end_turn(self, game):
    self.player.hand.draw_new_card()
    if self.player.species == 'Human':
      input(f'\nPress enter to finish your turn by drawing a card. ')
      print(f'\n\t> You drew: {self.player.hand.cards[-1]}\n\n\n')
    else:
      print(f'- {self.player.name} drew a card -\n')
    if self.player.hand.cards[-1].name == 'Exploding Kitten':
      game.exploded = True
    if game.exploded:
      self.check_for_defuse_card(game)


class ComputerTurn(Turn):
  def __init__(self, player, opponent, game):
    super().__init__(player, opponent, game)
    self.end_turn(game)


class HumanTurn(Turn):
  def __init__(self, player, opponent, game):
    super().__init__(player, opponent, game)
    self.player = player
    self.game = game

    self.play_cards()
    if not self.skip_turn: self.end_turn(game)

  def play_cards(self):
    self.player.hand.show_cards()
    answer = input(f'Would you like to play a card? (y/n) ')
    play_card = (answer == 'y')

    while play_card:
      card_index = self.choose_card()
      self.activate_card(card_index)
      os.system('cls||clear')
      self.player.hand.show_cards()

      answer = input(f'Would you like to play another card? (y/n) ')
      play_card = (answer == 'y')
      


  def choose_card(self):
    choice = -1
    hand_size = len(self.player.hand.cards)
    while not choice in range(0, hand_size):
      choice = int(input('Choose a card: ' )) - 1

    return choice

class Game():
  def __init__(self):
    self.deck = Deck()
    os.system('cls||clear')
    print('Welcome to Exploding Kittens!')

    self.human_hand = Hand(self.deck)
    self.computer_hand = Hand(self.deck)

    self.human = Human(self.human_hand)
    self.computer = Computer(self.computer_hand)

    self.exploded = False
    input(f'\n\nPress enter to continue  ')
    os.system('cls||clear')


  def list_rules(self):
    pass

  def play(self):
    for _ in range(5):
      self.deck.insert_exploding_kitten_cards()

    while not self.exploded:
      for player in [self.human, self.computer]:
        if player.species == 'Human':
          HumanTurn(player, self.computer, self)
        else:
          ComputerTurn(player, self.computer, self)

        if self.exploded: 
          print(player.hand.cards[-1].phrase)
          print('\n\nBOOOOOOOOOOMMMMMMM!!!!!\n\n')
          print(f'{player.name} lost!\n\n')
          break
        
        input(f'Press enter to continue')
        os.system('cls||clear')


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
