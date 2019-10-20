
# NEXT TO DO:

# Stop explosion if have defuse
# Add shuffle capability
# Add see the future capability
# Add attack capability
# Add default computer activity
# Add nope capability


import random

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
      'phrase': ['*gnaw, gnaw, gnaw* (on electrical wires)', 'zzzz (warp core + cat hair = BAD)', '*scampers across nuke detonation button*', '*crunch munch* on TNT'],
      'type': 'exploding_kitten',
      'start_count': 0
    },
    'skip': {
      'name': 'Skip',
      'phrase': ['Crab walk with some crabs', 'Engage the hypergoat', 'Don a portable cheetah butt', 'Commandeer a bunnyraptor'],
      'type': ['skip'],
      'start_count': 4
    }
  }
  
  def __init__(self, value):
    self.name = self.types[value]['name']
    self.phrase = random.choice(self.types[value]['phrase'])
    self.function = self.types[value]['type']

  def __str__(self):
    return f'{self.name} \"{self.phrase}\"'

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
    self.name = random.choice(['R2D2', 'C-3PO', 'HAL', 'GWB-666', 'Alexa', 'Siri', 'Computer', 'Cortana'])
    print(f'You\'ll be playing against {self.name}.')
    self.species = 'Computer'
  
class Hand():
  def __init__(self, deck):
    self.deck = deck
    self.cards = []
    self.get_starting_hand()

  def get_starting_hand(self):
    self.deck.deal_starting_hand(self)

  def show_cards(self):
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

class Turn():
  def __init__(self, player, game):
    self.skip_turn = False
    self.player = player
    self.game = game

  def end_turn(self, game):
    self.player.hand.draw_new_card()
    if self.player.species == 'Human':
      print(f'You drew: {self.player.hand.cards[-1]}')
    else:
      print(f'- {self.player.name} drew a card -')
    if self.player.hand.cards[-1].name == 'Exploding Kitten':
      game.exploded = True
    print('')

class ComputerTurn(Turn):
  def __init__(self, player, game):
    super().__init__(player, game)
    self.end_turn(game)


class HumanTurn(Turn):
  def __init__(self, player, game):
    super().__init__(player, game)
    self.player = player
    self.game = game

    self.play_cards()
    if not self.skip_turn: self.end_turn(game)

  def play_cards(self):
    self.player.hand.show_cards()

    answer = input(f'Would you like to play a card? (y/n) ')
    play_card = (answer == 'y')

    while play_card:
      card_choice = self.choose_card()
      self.activate_card(self.player.hand.cards[card_choice])
      self.player.hand.play_card(card_choice)
      answer = input(f'Would you like to play another card? (y/n) ')
      play_card = (answer == 'y')


  def choose_card(self):
    choice = -1
    hand_size = len(self.player.hand.cards)
    while not choice in range(0, hand_size):
      choice = int(input('Choose a card: ' )) - 1

    return choice

  def activate_card(self, card):
    self.skip_turn = ('skip' in card.function)


class Game():
  def __init__(self):
    self.deck = Deck()
    print('Welcome to Exploding Kittens!')

    self.human_hand = Hand(self.deck)
    self.computer_hand = Hand(self.deck)

    self.human = Human(self.human_hand)
    self.computer = Computer(self.computer_hand)

    self.exploded = False

  def list_rules(self):
    pass

  def play(self):
    self.deck.insert_exploding_kitten_cards()
    self.deck.insert_remaining_defuse_cards()

    while not self.exploded:
      for player in [self.human, self.computer]:
        if player.species == 'Human':
          HumanTurn(player, self)
        else:
          ComputerTurn(player, self)

        if self.exploded: 
          print(f'{player.name} lost!')
          break


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
