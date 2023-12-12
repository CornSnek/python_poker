import poker_deck
import poker_enums
import unittest
class Hand:
    def __init__(self,deck:poker_deck.Deck):
        self.deck=deck
        deck.shuffle()
        self.hand=deck.get_cards(5)
    def rank_hand(self):
        """TODO"""
        pass
    def get_windows(sorted_cv):
        """
        Returns the highest number duplicate (highest_window_card).
        Optionally returns the second highest number duplicate (lowest_window_card)
        if there is an existing pair.
        """
        highest_window_card=None
        highest_window_max=0
        window_i=0
        while(window_i+highest_window_max<=5):
            while(window_i+highest_window_max!=5 and sorted_cv[window_i]==sorted_cv[window_i+highest_window_max]):
                highest_window_card=sorted_cv[window_i]
                highest_window_max+=1
            window_i+=1
        window_i=0
        lowest_window_card=None
        for i in range(4):
            if(sorted_cv[i]!=highest_window_card and sorted_cv[i]==sorted_cv[i+1]):
                lowest_window_card=sorted_cv[i]
                break
        return (highest_window_card,lowest_window_card)
    def check_straight(sorted_cv):
        first_value=sorted_cv[0]
        return all(c[0]+c[1]==first_value for c in enumerate(sorted_cv))
    def check_same_suit(hand):
        first_suit=hand[1][1]
        return all(c[1]==first_suit for c in hand)

class poker_deck_test(unittest.TestCase):
    def test_deck_check_straight(self):
        self.assertEqual(Hand.check_straight([4,3,2,1,0]),True)
    def test_deck_check_straight_not_straight(self):
        self.assertEqual(Hand.check_straight([5,4,3,2,0]),False)
    def test_deck_check_same_suit(self):
        hand=[
            poker_enums.generate_card("AS"),
            poker_enums.generate_card("4S"),
            poker_enums.generate_card("5S"),
            poker_enums.generate_card("7S"),
            poker_enums.generate_card("QS")
        ]
        self.assertEqual(Hand.check_same_suit(hand),True)
    def test_deck_check_same_suit_different(self):
        hand=[
            poker_enums.generate_card("AS"),
            poker_enums.generate_card("4S"),
            poker_enums.generate_card("5S"),
            poker_enums.generate_card("7S"),
            poker_enums.generate_card("QC")
        ]
        self.assertEqual(Hand.check_same_suit(hand),False)
deck=poker_deck.Deck()
hand=Hand(deck)
hand.rank_hand()