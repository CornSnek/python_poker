import math
import unittest
from enum import Enum
class Suit(Enum):
    Club=1,
    Heart=2,
    Spade=3,
    Diamond=4
    def __repr__(self):
        return suit_to_str[self]
str_to_suit={
    'C':Suit.Club,
    'H':Suit.Heart,
    'S':Suit.Spade,
    'D':Suit.Diamond
}
suit_to_str={v:k for (k,v) in str_to_suit.items()}
class Card(Enum):
    """Card Ranks"""
    AceLow=0
    Two=1
    Three=2
    Four=3
    Five=4
    Six=5
    Seven=6
    Eight=7
    Nine=8
    Ten=9
    Jack=10
    Queen=11
    King=12
    AceHigh=13
    def __repr__(self):
        return card_to_str[self]
#A is AceLow initially
str_to_card={
    'A':Card.AceLow,
    '2':Card.Two,
    '3':Card.Three,
    '4':Card.Four,
    '5':Card.Five,
    '6':Card.Six,
    '7':Card.Seven,
    '8':Card.Eight,
    '9':Card.Nine,
    'T':Card.Ten,
    'J':Card.Jack,
    'Q':Card.Queen,
    'K':Card.King,
}
card_to_str={v:k for (k,v) in str_to_card.items()}
card_to_str[Card.AceHigh]='A'
def generate_card(string:str,is_ace_high=False) -> (Card,Suit):
    """
    Format (Card)(Suit) using str_to_suit and str_to_card dictionaries
    Example: TC outputs (Card.Ten,Suit.Club)
    
    This is used for testing purposes.
    """
    card=str_to_card[string[0]]
    if is_ace_high and card==Card.AceLow:
        card=Card.AceHigh
    return (card,str_to_suit[string[1]])
def pascal_case_with_space(str:str):
    """Get slices of capital words to then place spaces between them"""
    slices:[(int,int)]=[]
    slice_begin:int=0
    for i,ch in enumerate(str):
        if ch.isupper():
            slices.append((slice_begin,i))
            slice_begin=i
    if len(slices)==0 or slices[-1][0]!=len(str)-1:
        slices.append((slice_begin,len(str)))
    return " ".join([str[sl[0]:sl[1]] for sl in slices]).strip()
class HandRank(Enum):
    HighCard=0
    Pair=1
    TwoPair=2
    ThreeOfAKind=3
    Straight=4
    Flush=5
    FullHouse=6
    FourOfAKind=7
    StraightFlush=8
    RoyalFlush=9
    def __repr__(self):
        return pascal_case_with_space(self.name)
def max_hand_rank(r1:HandRank,r2:HandRank):
    return r1 if r1.value>r2.value else r2
class poker_enums_test(unittest.TestCase):
    def test_generate_card(self):
        self.assertEqual(generate_card("9S"),(Card.Nine,Suit.Spade))
    def test_generate_card_ace_low(self):
        self.assertEqual(generate_card("AH"),(Card.AceLow,Suit.Heart))
    def test_generate_card_ace_high(self):
        self.assertEqual(generate_card("AC",True),(Card.AceHigh,Suit.Club))
    def test_max_hand_rank(self):
        self.assertEqual(max_hand_rank(HandRank.HighCard,HandRank.Pair),HandRank.Pair)
        self.assertEqual(max_hand_rank(HandRank.RoyalFlush,HandRank.StraightFlush),HandRank.RoyalFlush)