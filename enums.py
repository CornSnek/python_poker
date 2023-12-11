import math
import unittest
from enum import Enum
class Card(Enum):
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
#hand_rank:HandRank -> sum of previous hand_rank_values
def hand_rank_accumulate(hand_rank):
    return sum(hand_rank_values[0:hand_rank.value])
class TestHandRankValue(unittest.TestCase):
    def test_hand_rank_values_high_card(self):
        self.assertEqual(0,hand_rank_accumulate(HandRank.HighCard))
    def test_hand_rank_values_pair(self):
        self.assertEqual(hand_rank_values[HandRank.HighCard.value],hand_rank_accumulate(HandRank.Pair))
    def test_hand_rank_values_two_pair(self):
        self.assertEqual(hand_rank_values[HandRank.HighCard.value]+hand_rank_values[HandRank.Pair.value],hand_rank_accumulate(HandRank.TwoPair))
    def test_hand_rank_values_royal_flush(self):
        self.assertEqual(sum(hand_rank_values[0:HandRank.RoyalFlush.value]),hand_rank_accumulate(HandRank.RoyalFlush))
if __name__ == '__main__':
    unittest.main()