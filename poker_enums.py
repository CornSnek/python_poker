import math
import unittest
from enum import Enum
class Suit(Enum):
    Club=1,
    Heart=2,
    Spade=3,
    Diamond=4
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
    'J':Card.Jack,
    'Q':Card.Queen,
    'K':Card.King,
}
card_to_str={v:k for (k,v) in str_to_card.items()}
card_to_str[Card.AceHigh]='A'
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
hand_rank_values=[
    math.comb(13,5),
    math.comb(13,4),
    math.comb(13,3),
    math.comb(13,3),
    10, #A,2,3,4,5 to 10,J,Q,K,A
    math.comb(13,5),
    math.comb(13,2),
    math.comb(13,2),
    9, #A,2,3,4,5 to 9,10,J,Q,K (same suit)
    1,
]
def rank_num_sum(hand):
    """
    hand:List of sorted numbers descending -> Combinatorial number
    https://en.wikipedia.org/wiki/Combinatorial_number_system
    """
    sum=0
    same_number=None
    r=1
    for i in range(0,len(hand)):
        back_i=len(hand)-i-1
        if(hand[back_i]==same_number): continue
        same_number=hand[back_i]
        sum+=math.comb(hand[back_i],r)
        r+=1
    return sum
def hand_rank_accumulate(hand_rank:HandRank):
    """hand_rank:HandRank -> sum of previous hand_rank_values"""
    return sum(hand_rank_values[0:hand_rank.value])
class poker_enums_test(unittest.TestCase):
    def test_hand_rank_values_high_card(self):
        self.assertEqual(0,hand_rank_accumulate(HandRank.HighCard))
    def test_hand_rank_values_pair(self):
        self.assertEqual(hand_rank_values[HandRank.HighCard.value],hand_rank_accumulate(HandRank.Pair))
    def test_hand_rank_values_two_pair(self):
        self.assertEqual(hand_rank_values[HandRank.HighCard.value]+hand_rank_values[HandRank.Pair.value],hand_rank_accumulate(HandRank.TwoPair))
    def test_hand_rank_values_royal_flush(self):
        self.assertEqual(sum(hand_rank_values[0:HandRank.RoyalFlush.value]),hand_rank_accumulate(HandRank.RoyalFlush))