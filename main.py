import poker_deck
import poker_enums
import unittest
class Hand:
    def __init__(self,deck:poker_deck.Deck=None):
        self.deck=deck
        if deck==None:
            self.hand=[]
        else:
            deck.shuffle()
            self.hand=deck.get_cards(5)
    def get_hand_rank(self):
        sorted_cv=poker_deck.Deck.as_sorted_values(self.hand)
        is_straight=Hand.check_straight(sorted_cv)
        is_flush=Hand.check_same_suit(self.hand)
        highest_window_max,high_window,low_window=Hand.get_windows(sorted_cv)
        if is_straight and is_flush:
            if(sorted_cv!=[13,12,11,10,9]):
                rank=poker_enums.HandRank.StraightFlush
            else:
                rank=poker_enums.HandRank.RoyalFlush
            number_ranks=sorted_cv #Gets number values from highest/lowest rankings
        elif highest_window_max==4:
            rank=poker_enums.HandRank.FourOfAKind
            number_ranks=[high_window]
            number_ranks.extend([e for e in sorted_cv if e not in number_ranks])
        elif highest_window_max==3 and low_window!=None:
            rank=poker_enums.HandRank.FullHouse
            number_ranks=[high_window,low_window]
        elif is_flush:
            rank=poker_enums.HandRank.Flush
            number_ranks=sorted_cv
        elif is_straight:
            rank=poker_enums.HandRank.Straight
            number_ranks=sorted_cv
        elif highest_window_max==3:
            rank=poker_enums.HandRank.ThreeOfAKind
            number_ranks=[high_window]
            number_ranks.extend([e for e in sorted_cv if e not in number_ranks])
        elif highest_window_max==2:
            if low_window!=None:
                rank=poker_enums.HandRank.TwoPair
                number_ranks=[high_window,low_window]
                number_ranks.extend([e for e in sorted_cv if e not in number_ranks])
            else:
                rank=poker_enums.HandRank.Pair
                number_ranks=[high_window]
                number_ranks.extend([e for e in sorted_cv if e not in number_ranks])
        else:
            rank=poker_enums.HandRank.HighCard
            number_ranks=sorted_cv
        return (rank,number_ranks)
    def get_windows(sorted_cv):
        """
        Returns (highest_window_max,highest_window_card,lowest_window_card)
        The first number is the highest number of duplicates.
        The second number is the number duplicate.
        The third is the second number duplicate if there is an existing pair.
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
        return (highest_window_max,highest_window_card,lowest_window_card)
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
        hand.hand=[pgc("TD"), pgc("JD"), pgc("QD"), pgc("KD"), pgc("AD",is_ace_high=True)]
        self.assertEqual(hand.get_hand_rank()[0],poker_enums.HandRank.RoyalFlush)
deck=poker_deck.Deck()
hand=Hand(deck)