import random
import itertools
import os
import time
from colorama import Fore, Style, Back

# initialize player bank
bank = 1000

def card_value(card):
  rank = card[0]
  if rank in [x for x in range(2, 11)]:
    return rank
  elif rank in ['J', 'Q', 'K']:
    return 10
  elif rank == 'A':
    return 11

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
    
    if total > 21 and num_aces > 0:
      total -= 10
      num_aces -= 1
  
  return total


# single hand loop
while True:
  os.system('clear')
  ranks = [2, 3, 4, 5, 6, 7, 8, 9, 'J', 'Q', 'K', 'A']
  suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']

  deck = list(itertools.product(ranks, suits))
  # shuffle the deck
  random.shuffle(deck)

  # initialize the hands
  player_hand = [deck.pop(), deck.pop()]
  dealer_hand = [deck.pop(), deck.pop()]

  dealer_total = get_hand_value(dealer_hand)
  player_total = get_hand_value(player_hand)

  hand_over = False

  # handle initial deal
  if dealer_total != 21:
    if player_total != 21:
      print('\nDealer: ' + Fore.RED + Back.YELLOW + f'{dealer_hand[0]}..... {card_value(dealer_hand[0])} ' + Style.RESET_ALL)
      print('\nPlayer: ' + Fore.BLUE + Back.YELLOW + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
    else:
      print('\nDealer: ' + Fore.RED + Back.YELLOW + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
      print('\nPlayer: ' + Fore.BLUE + Back.YELLOW + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
      print(Fore.GREEN + '\nBlackjack! You win. ' + Style.RESET_ALL)
      hand_over = True
      
  elif dealer_total == 21:
    if player_total != 21:
      print('\nDealer: ' + Fore.RED + Back.YELLOW + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
      print('\nPlayer: ' + Fore.BLUE + Back.YELLOW +  f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
      print(Fore.RED + '\nBlackjack for dealer.  You lose. ' + Style.RESET_ALL)
      hand_over = True
    else:
      print('\nDealer: ' + Fore.RED + Back.YELLOW + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
      print('\nPlayer: ' + Fore.RED + Back.YELLOW + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
      print(Fore.GREEN + '\n21 for both. Push. ' + Style.RESET_ALL)
      hand_over = True
  
  # if hand is over on initial deal
  if hand_over:
    cmd = input('\nWould you like to play again?  [y] Yes  [n] No ')
    
    if cmd == 'n':
      break
    elif cmd != 'y':
      print('Invalid input')

  # implement game logic
  else:
    while player_total < 21:
      cmd = input(f'\nYou have {player_total} vs {card_value(dealer_hand[0])}.  What would you like to do? [h] Hit [s] Stand ')
      
      if cmd == 'h':
        os.system('clear')
        player_hand.append(deck.pop())
        player_total = get_hand_value(player_hand)
        print('\nDealer: ' + Fore.RED + Back.YELLOW +  f'{dealer_hand[0]}..... {card_value(dealer_hand[0])} ' + Style.RESET_ALL)
        print('\nPlayer: ' + Fore.BLUE + Back.YELLOW +  f'{player_hand}..... {player_total} ' + Style.RESET_ALL)

        # if player_total == 21:
        #   print(Fore.GREEN + Back.WHITE + '\n21.  Let\'s see what the dealer has... ' + Style.RESET_ALL)
        #   break
        
        while player_total > 21:
          cmd = input(Fore.RED + '\nYou busted. ' + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
          if cmd == 'n':
            exit()
          elif cmd != 'y':
            print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
          else:
            os.system('clear')
            break
      
      elif cmd == 's':
        break

      else:
        print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
    
    if player_total <= 21:
      while dealer_total <= 21:
        # dealer stays and loses to player
        if dealer_total > 16 and player_total > dealer_total:
          os.system('clear')
          print('\nDealer: ' + Fore.RED + Back.YELLOW + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
          print('\nPlayer: ' + Fore.BLUE + Back.YELLOW + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
          cmd = input(Fore.GREEN + '\nYou win! ' + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
          if cmd == 'n':
            exit()
          elif cmd != 'y':
            print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
          else:
            break
        
        # dealer stays and beats player
        elif dealer_total > 16 and dealer_total > player_total:
          os.system('clear')
          print('\nDealer: ' + Fore.RED + Back.YELLOW + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
          print('\nPlayer: ' + Fore.BLUE + Back.YELLOW + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
          cmd = input(Fore.RED + '\nYou lose. '  + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
          if cmd == 'n':
            exit()
          elif cmd != 'y':
            print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
          else:
            break
        
        # dealer stays and ties player
        elif dealer_total > 16 and dealer_total == player_total:
          os.system('clear')
          print('\nDealer: ' + Fore.RED + Back.YELLOW + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
          print('\nPlayer: ' + Fore.BLUE + Back.YELLOW + f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
          cmd = input(Fore.GREEN + '\nPush! ' + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
          if cmd == 'n':
            exit()
          elif cmd != 'y':
            print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
          else:
            break
        
        elif dealer_total < 17:
          while dealer_total < 17:
            os.system('clear')
            dealer_hand.append(deck.pop())
            dealer_total = get_hand_value(dealer_hand)
            print('\nDealer: ' + Fore.RED + Back.YELLOW + f'{dealer_hand}..... {dealer_total} ' + Style.RESET_ALL)
            print('\nPlayer: ' + Fore.BLUE + Back.YELLOW +  f'{player_hand}..... {player_total} ' + Style.RESET_ALL)
            
            if dealer_total > 21:
              cmd = input(Fore.GREEN + '\nDealer busts, you win! ' + Fore.WHITE + 'Would you like to play again? [y] yes [n] no ' + Style.RESET_ALL)
              if cmd == 'n':
                exit()
              elif cmd != 'y':
                print(Fore.RED + '\nInvalid Input' + Style.RESET_ALL)
              else:
                break
    
    






