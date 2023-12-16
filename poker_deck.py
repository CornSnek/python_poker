import poker_enums
import random
import unittest
class DeckException(Exception):
    pass
class Deck:
    def __init__(self):
        self.deck:(poker_enums.Card,poker_enums.Suit)=[]
        for s in poker_enums.Suit:
            for c in list(poker_enums.Card)[0:-1]: #Exclude Card.AceHigh
                self.deck.append((c,s))
    def shuffle(self):
        random.shuffle(self.deck)
    def get_cards(self,much:int):
        if(much>len(self.deck)): raise DeckException("Too many cards drawn")
        return_cards=self.deck[-much:]
        del self.deck[-much:]
        return return_cards
    def put_back_cards(self,hand):
        self.deck=hand+self.deck
        del hand[:]
    def replace_one_card(self,hand,at_i):
        self.deck.insert(0,hand[at_i])
        hand[at_i]=self.deck.pop()
    def as_sorted_values(hand):
        return sorted([h[0].value for h in hand],reverse=True)
    def check_if_deck_unique(self):
        """This is mostly for error-checking if duplcate cards have accidentally been added back"""
        check_set=set()
        return not any(i in check_set or check_set.add(i) for i in self.deck) and len(self.deck)==52
class poker_deck_test(unittest.TestCase):
    def test_no_cards_from_get_cards(self):
        deck=Deck()
        hand=deck.get_cards(5)
        for d in deck.deck:
            for h in hand:
                self.assertNotEqual(d,h)
    def test_cards_whole_deck_should_be_unique(self):
        deck=Deck()
        self.assertEqual(deck.check_if_deck_unique(),True)
    def test_cards_duplicates_should_not_be_unique(self):
        deck=Deck()
        deck.deck.append((poker_enums.Card.AceLow,poker_enums.Suit.Diamond))
        self.assertEqual(deck.check_if_deck_unique(),False)