import math
import unittest
import utils
from enum import Enum
class Suit(Enum):
    Club=0,
    Heart=1,
    Spade=2,
    Diamond=3
    def as_game_str(self):
        return suit_to_game_str[self]
str_to_suit={
    'C':Suit.Club,
    'H':Suit.Heart,
    'S':Suit.Spade,
    'D':Suit.Diamond
}
ts=utils.add_escape_seq
suit_to_game_str={
    Suit.Club:ts('30;1m','♣'),
    Suit.Heart:ts('31;1m','♥'),
    Suit.Spade:ts('30;1m','♠'),
    Suit.Diamond:ts('31;1m','♦'),
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
    def as_game_str(self):
        if self==Card.AceLow: return "A (Low)"
        elif self==Card.AceHigh: return "A (High)"
        elif self==Card.Ten: return '10'
        else: return card_to_str[self]
#card_to_game_str={k:v for k,v in Card}
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
    def as_game_str(self):
        return utils.pascal_case_with_space(self.name)
def max_hand_rank(r1:HandRank,r2:HandRank):
    return r1 if r1.value>r2.value else r2
class ActionType(Enum):
    Check=0,
    Call=1,
    Bet=2,
    Raise=3,
    Fold=4,
    def get_options(self):
        assert(self!=ActionType.Fold)
        if self==ActionType.Check:
            return [at for at in list(ActionType) if at.value>=ActionType.Check.value and at.value!=ActionType.Call.value]
        elif self==ActionType.Call:
            return [at for at in list(ActionType) if at.value>=ActionType.Call.value]
        elif self==ActionType.Bet or self==ActionType.Raise:
            return [at for at in list(ActionType) if at.value>=ActionType.Bet.value]
    def as_game_str_options(self):
        return ", ".join(["("+o.name[0]+")"+o.name[1:] for o in self.get_options()])
    def get_input_option(self,chosen:str):
        """First character"""
        options=self.get_options()
        for o in options:
            first_c=o.name[0]
            if chosen==first_c:
                return o
    def game_description(self,player_i)->str:
        if(self==ActionType.Check):
            option_str=f"Player {player_i+1} has checked their turn"
        elif(self==ActionType.Call):
            option_str=f"Player {player_i+1} has called their turn, matching the bet from other players"
        elif(self==ActionType.Bet):
            option_str=f"Player {player_i+1} has betted their turn, matching the bet from other players"
        elif(self==ActionType.Raise):
            option_str=f"Player {player_i+1} has raised the bet their turn, matching the bet from other players"
        elif(self==ActionType.Fold):
            option_str=f"Player {player_i+1} has folded their turn"
        return option_str
def as_probability_weights(list:list[int]):
    assert(len(ActionType)==5)
    return {at:p for at,p in zip(ActionType,list)}
hand_rank_choose_probability:dict[HandRank,dict[ActionType:int]]={
    #Numbers are probabilities based on ActionType
    #For Computer AI
    HandRank.HighCard:as_probability_weights([20,20,10,10,40]),
    HandRank.Pair:as_probability_weights([20,20,10,10,40]),
    HandRank.TwoPair:as_probability_weights([15,15,20,20,30]),
    HandRank.ThreeOfAKind:as_probability_weights([10,10,25,25,30]),
    HandRank.Straight:as_probability_weights([10,10,30,30,20]),
    HandRank.Flush:as_probability_weights([10,10,40,25,15]),
    HandRank.FullHouse:as_probability_weights([5,10,45,30,10]),
    HandRank.FourOfAKind:as_probability_weights([5,10,45,35,5]),
    HandRank.StraightFlush:as_probability_weights([5,10,45,35,5]),
    HandRank.RoyalFlush:as_probability_weights([5,10,45,40,0]),
}
for d in hand_rank_choose_probability.values():
    assert(sum(d.values())==100)
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