#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
from random import shuffle

def calculate_total(cards):
    total = 0
    for(suit, value) in cards:
        if value == 'A':
           total += 11
        elif value in ['J', 'Q', 'K']:
           total += 10
        else:
           total += int(value)
           
    aces = sum(card.count("A") for card in cards)

    while total > 21 and aces:
        total -= 10
        aces -= 1
        
    return total

print("Welcome to Blackjack!")

suits = ['H', 'D', 'S', 'C']
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

deck = list(itertools.product(suits,cards))
shuffle(deck)

print(deck)

player_hand = []
dealer_hand = []

player_hand.append(deck.pop())
dealer_hand.append(deck.pop())
player_hand.append(deck.pop())
dealer_hand.append(deck.pop())

dealer_total = calculate_total(dealer_hand)
player_total = calculate_total(player_hand)

print("Dealer has: Hissen and {0}". format(dealer_hand[1]))
print("You have: {0} and {1}, for a total of {2}".format(player_hand[0], player_hand[1], player_total))

if player_total == 21 and dealer_total ==21:
    print("It's a push. House wins. Sorry.")
    quit()
elif player_total == 21:
    print("Congratulations, you hit Blackjack! You win!")
    quit()
elif dealer_total == 21:
    print("Sorry, dealer hit Blackjack. You lose.")
else:
    pass

while player_total < 21:
    hit_or_stay = input("What would you like to do? 1) Hit 2) Stay ")
    
    if hit_or_stay not in ['1', '2']:
        print("error, you must enter 1 or 2")
        continue
    elif hit_or_stay == "2":
        print("You choose to stay.")
        break
    else:
        new_card = deck.pop()
        print("Dealing card to player: {0}".format(new_card))
        
        player_hand.append(new_card)
        player_total = calculate_total(player_hand)
        print("Your total is now: {0}".format(player_total))
        
        if player_total == 21:
            print("Congratulations, you hit Blackjack! You win!")
            quit()
        elif player_total > 21:
            print("Sorry, you busted.")
            quit()
        else:
            continue
        
while dealer_total <17:
    new_card = deck.pop()
    print("Dealing card to dealer: {}".format(new_card))
    
    dealer_hand.append(new_card)
    dealer_total = calculate_total(dealer_hand)
    print("Dealer's total is now: {}".format(dealer_total)
    
    if dealer_total = 21:
        print("Sorry, dealer hit Blackjack. You lose.")
        quit()
    elif dealer_total > 21:
        print("Congratulations, dealer busted! You win!")
        quit()
    else:
        continue
    
print("Dealer's cards")
for card in dealer_hand:
    print(card)
print("")

if dealer_total > player_total:
    print("Sorry, dealer wins")
elif dealer_total < player_total:
    print("Congratulations, you win!")
else:
    print("Its a tie!")
    
quit()

print
    
        
    
    
        
        
