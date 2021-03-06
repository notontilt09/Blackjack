import random
import itertools
import os
import time
import sys
from colorama import Fore, Style

# initialize player bank
bank = 1000

# get the value of a single card
def card_value(card):
  rank = card[0]
  if rank in [x for x in range(2, 11)]:
    return rank
  elif rank in ['J', 'Q', 'K']:
    return 10
  elif rank == 'A':
    return 11

# get the value of an entire hand
def get_hand_value(hand):
  num_aces = 0
  total = 0
  for card in hand:
    if card[0] == 'A':
      num_aces += 1
      total += 11
    elif card[0] in ['J', 'Q', 'K']:
      total += 10
    else:
      total += card[0]
    
    # handling aces
    if total > 21 and num_aces > 0:
      total -= 10
      num_aces -= 1
  
  return total

# def handle_split(player_hand, dealer_hand, deck):
#   # setup potential hands
#   ph1 = []
#   ph2 = []
#   ph1.append(player_hand[0])
#   ph1.append(deck.pop())
#   ph2.append(player_hand[1])
#   ph2.append(deck.pop())
#   print(ph1)
#   print(ph2)

#   while get_hand_value(ph1) < 21:
#     cmd = input(f'\nYou have {get_hand_value(ph1)} vs {card_value(dealer_hand[0])}.  What would you like to do? [h] Hit [s] Stand ')
#     # hitting
#     if cmd == 'h':
#       ph1.append(deck.pop())
#       print(get_hand_value(ph1))
#       print('\nDealer: ' + Fore.RED + f'{dealer_hand[0]}..... {card_value(dealer_hand[0])} ' + Style.RESET_ALL)
#       print('\nPlayer: ' + Fore.GREEN + f'{ph1}..... {get_hand_value(ph1)} ' + Style.RESET_ALL)


# single hand loop
# def play_hand(bank, player_hand=None, dealer_hand=None, deck=None, bet=None):
while True:
  if bank <= 0:
    while bank <= 0:
      cmd = input(Fore.RED + f'You\'re out of cash.  Refill bank? [y] yes [n] no ' + Style.RESET_ALL)
      if cmd == 'y':
        bank = 1000
      elif cmd == 'n':
        sys.exit()
      else:
        print(Fore.RED + 'Invalid Input' + Style.RESET_ALL)
        bank = 0
      
  bet = None
  while bet is None:
    os.system('clear')
    bet = input(f'You have ${int(bank)}, how much would you like to wager. ')
    if not str.isdigit(bet):
      cmd = input(Fore.RED + '\nOnly whole numbers amigo.  Press any key to continue. ' + Style.RESET_ALL)
      bet = None
      continue
    if str.isdigit(bet) and int(bet) > bank:
      cmd = input(Fore.RED + f'\nYou only have {bank}, your credit sucks, thus you cannot bet {bet}.  Press any key to continue. ' + Style.RESET_ALL)
      bet = None


  # set up deck if it wasn't passed in to function
  ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
  suits = ['\u2664',	'\u2661',	'\u2662', '\u2667']
  deck = list(itertools.product(ranks, suits))

    # shuffle the deck
  random.shuffle(deck)

  # initialize the hands if they weren't passed in to function
  player_hand = [deck.pop(), deck.pop()]
  player_total = get_hand_value(player_hand)
  
  dealer_hand = [deck.pop(), deck.pop()]
  dealer_total = get_hand_value(dealer_hand)


  # boolean to keep track if hand ends on initital deal
  hand_over = False

  # handle initial deal
  if dealer_total != 21:
    if player_total != 21:
      print('\nDealer: ' + Fore.RED + f'{dealer_hand[0]}..... {card_value(dealer_hand[0])} ' + Style.RESET_ALL)
      print('\nPlayer: ' + Fore.GREEN + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
    else:
      print('\nDealer: ' + Fore.RED + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
      print('\nPlayer: ' + Fore.GREEN + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
      print(Fore.GREEN + f'\nBlackjack! You win ${int(int(bet) * 1.5)}. ' + Style.RESET_ALL)
      bank += int(bet) * 1.5
      hand_over = True
      
  elif dealer_total == 21:
    if player_total != 21:
      print('\nDealer: ' + Fore.RED + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
      print('\nPlayer: ' + Fore.GREEN + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
      print(Fore.RED + f'\nBlackjack for dealer.  You lose ${bet}. ' + Style.RESET_ALL)
      bank -= int(bet)
      hand_over = True
    else:
      print('\nDealer: ' + Fore.RED + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
      print('\nPlayer: ' + Fore.GREEN + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
      print(Fore.GREEN + '\n21 for both. Push. ' + Style.RESET_ALL)
      hand_over = True
  
  # if hand is over on initial deal
  if hand_over:
    cmd = input('\nWould you like to play again?  [y] Yes  [n] No ')
    
    if cmd == 'n':
      exit()
    elif cmd != 'y':
      print('Invalid input')

  # if hand doesn't end on deal, implement game logic
  else:
    # player loop
    while player_total < 21:
      # initial options of hit/stand/double/split
      if len(player_hand) == 2:
        if player_hand[0][0] == player_hand[1][0]:
          cmd = input(f'\nYou have {player_total} vs {card_value(dealer_hand[0])}.  What would you like to do? [h] Hit [s] Stand [d] Double down [p] Split: ')
        else:
          cmd = input(f'\nYou have {player_total} vs {card_value(dealer_hand[0])}.  What would you like to do? [h] Hit [s] Stand [d] Double down: ')
        # if user hits
        if cmd == 'h':
          os.system('clear')
          player_hand.append(deck.pop())
          player_total = get_hand_value(player_hand)
          print('\nDealer: ' + Fore.RED + f'{dealer_hand[0]}..... {card_value(dealer_hand[0])} ' + Style.RESET_ALL)
          print('\nPlayer: ' + Fore.GREEN + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
          
          # handle player busting
          while player_total > 21:
            cmd = input(Fore.RED + f'\nBUST!  You lost ${bet}. ' + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
            if cmd == 'n':
              exit()
            elif cmd != 'y':
              print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
            else:
              bank -= int(bet)
              os.system('clear')
              break
        
        # player doubles
        elif cmd == 'd':
          if int(bet) * 2 > bank:
            print(Fore.RED + f'\nYou do not have enough funds to double down. Press any key to continue. ' + Style.RESET_ALL)
            continue
          else:
            os.system('clear')
            bet = int(bet) * 2
            player_hand.append(deck.pop())
            player_total = get_hand_value(player_hand)
            print('\nDealer: ' + Fore.RED + f'{dealer_hand[0]}..... {card_value(dealer_hand[0])} ' + Style.RESET_ALL)
            print('\nPlayer: ' + Fore.GREEN + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
            # handle player busting
            while player_total > 21:
              cmd = input(Fore.RED + f'\nBUST!  You lost ${bet}. ' + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
              if cmd == 'n':
                exit()
              elif cmd != 'y':
                print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
              else:
                bank -= int(bet)
                os.system('clear')
                break
            break
        # if user stays, break out of player loop
        elif cmd == 's':
          break
        
        # if user splits, handle split
        # elif cmd == 'p':
        #   if int(bet) * 2 > bank:
        #     print(Fore.RED + "\nNot enough $ to split" + Style.RESET_ALL)
        #     continue
          # else:
          #   handle_split(player_hand, dealer_hand, deck)

        else:
          print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
      
      # after initial hit when player has 3 cards, need to remove options to double/split
      else:
        cmd = input(f'\nYou have {player_total} vs {card_value(dealer_hand[0])}.  What would you like to do? [h] Hit [s] Stand ')
        # if user hits
        if cmd == 'h':
          os.system('clear')
          player_hand.append(deck.pop())
          player_total = get_hand_value(player_hand)
          print('\nDealer: ' + Fore.RED + f'{dealer_hand[0]}..... {card_value(dealer_hand[0])} ' + Style.RESET_ALL)
          print('\nPlayer: ' + Fore.GREEN + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
          
          # handle player busting
          while player_total > 21:
            cmd = input(Fore.RED + f'\nBUST!  You lost ${bet}. ' + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
            if cmd == 'n':
              exit()
            elif cmd != 'y':
              print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
            else:
              bank -= int(bet)
              os.system('clear')
              break
        
        # if user stays, break out of player loop
        elif cmd == 's':
          break

        else:
          print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
    
    if player_total <= 21:
      # dealer loop
      while dealer_total <= 21:
        # dealer stays and loses to player
        if dealer_total > 16 and player_total > dealer_total:
          os.system('clear')
          print('\nDealer: ' + Fore.RED + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
          print('\nPlayer: ' + Fore.GREEN + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
          cmd = input(Fore.GREEN + f'\nYou win ${bet}! ' + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
          if cmd == 'n':
            exit()
          elif cmd != 'y':
            print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
          else:
            bank += int(bet)
            break
        
        # dealer stays and beats player
        elif dealer_total > 16 and dealer_total > player_total:
          os.system('clear')
          print('\nDealer: ' + Fore.RED + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
          print('\nPlayer: ' + Fore.GREEN + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
          cmd = input(Fore.RED + f'\nYou lose ${bet}! '  + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
          if cmd == 'n':
            exit()
          elif cmd != 'y':
            print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
          else:
            bank -= int(bet)
            break
        
        # dealer stays and ties player
        elif dealer_total > 16 and dealer_total == player_total:
          os.system('clear')
          print('\nDealer: ' + Fore.RED + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
          print('\nPlayer: ' + Fore.GREEN + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
          cmd = input(Fore.GREEN + '\nPush! ' + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
          if cmd == 'n':
            exit()
          elif cmd != 'y':
            print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
          else:
            break
        
        # dealer hits until it reaches 17
        elif dealer_total < 17:
          while dealer_total < 17:
            os.system('clear')
            dealer_hand.append(deck.pop())
            dealer_total = get_hand_value(dealer_hand)
            print('\nDealer: ' + Fore.RED + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
            print('\nPlayer: ' + Fore.GREEN + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
            
            # dealer busts
            if dealer_total > 21:
              cmd = input(Fore.GREEN + f'\nDealer busts, you win ${bet}! ' + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
              if cmd == 'n':
                exit()
              elif cmd != 'y':
                print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
              else:
                bank += int(bet)
                break








