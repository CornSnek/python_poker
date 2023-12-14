import unittest
from main import *
class poker_deck_test(unittest.TestCase):
    def test_deck_check_straight(self):
        self.assertEqual(Hand.check_straight([4,3,2,1,0]),True)
    def test_deck_check_straight_not_straight(self):
        self.assertEqual(Hand.check_straight([5,4,3,2,0]),False)
    def test_deck_check_same_suit(self):
        pgc=poker_enums.generate_card
        hand=[ pgc("AS"), pgc("4S"), pgc("5S"), pgc("7S"), pgc("QS") ]
        self.assertEqual(Hand.check_same_suit(hand),True)
    def test_deck_check_same_suit_different(self):
        pgc=poker_enums.generate_card
        hand=[ pgc("AS"), pgc("4S"), pgc("5S"), pgc("7S"), pgc("QC") ]
        self.assertEqual(Hand.check_same_suit(hand),False)
    def test_is_high_card(self):
        pgc=poker_enums.generate_card
        hand=Hand()
        hand.hand=[pgc("AS"), pgc("4S"), pgc("5S"), pgc("7S"), pgc("QC")]
        self.assertEqual(hand.get_hand_rank()[0],poker_enums.HandRank.HighCard)
    def test_is_pair(self):
        pgc=poker_enums.generate_card
        hand=Hand()
        hand.hand=[pgc("AS"), pgc("4S"), pgc("5S"), pgc("QS"), pgc("QC")]
        self.assertEqual(hand.get_hand_rank()[0],poker_enums.HandRank.Pair)
    def test_is_two_pair(self):
        pgc=poker_enums.generate_card
        hand=Hand()
        hand.hand=[pgc("4H"), pgc("4S"), pgc("5S"), pgc("QS"), pgc("QC")]
        self.assertEqual(hand.get_hand_rank()[0],poker_enums.HandRank.TwoPair)
    def test_is_three_of_a_kind(self):
        pgc=poker_enums.generate_card
        hand=Hand()
        hand.hand=[pgc("4H"), pgc("4S"), pgc("4C"), pgc("AS"), pgc("QC")]
        self.assertEqual(hand.get_hand_rank()[0],poker_enums.HandRank.ThreeOfAKind)
    def test_is_straight(self):
        pgc=poker_enums.generate_card
        hand=Hand()
        hand.hand=[pgc("4H"), pgc("5H"), pgc("6H"), pgc("7H"), pgc("8C")]
        self.assertEqual(hand.get_hand_rank()[0],poker_enums.HandRank.Straight)
    def test_is_flush(self):
        pgc=poker_enums.generate_card
        hand=Hand()
        hand.hand=[pgc("4H"), pgc("5H"), pgc("6H"), pgc("7H"), pgc("9H")]
        self.assertEqual(hand.get_hand_rank()[0],poker_enums.HandRank.Flush)
    def test_is_full_house(self):
        pgc=poker_enums.generate_card
        hand=Hand()
        hand.hand=[pgc("3S"), pgc("3C"), pgc("3H"), pgc("AD"), pgc("AS")]
        self.assertEqual(hand.get_hand_rank()[0],poker_enums.HandRank.FullHouse)
    def test_is_four_of_a_kind(self):
        pgc=poker_enums.generate_card
        hand=Hand()
        hand.hand=[pgc("TS"), pgc("TC"), pgc("TH"), pgc("TD"), pgc("AD")]
        self.assertEqual(hand.get_hand_rank()[0],poker_enums.HandRank.FourOfAKind)
    def test_is_straight_flush(self):
        pgc=poker_enums.generate_card
        hand=Hand()
        hand.hand=[pgc("AD"), pgc("2D"), pgc("3D"), pgc("4D"), pgc("5D")]
        self.assertEqual(hand.get_hand_rank()[0],poker_enums.HandRank.StraightFlush)
    def test_is_royal_flush(self):
        pgc=poker_enums.generate_card
        hand=Hand()
        hand.hand=[pgc("TD"), pgc("JD"), pgc("QD"), pgc("KD"), pgc("AD")]
        self.assertEqual(hand.get_hand_rank(ace_high=True)[0],poker_enums.HandRank.RoyalFlush)