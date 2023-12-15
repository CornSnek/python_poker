import poker_deck
import poker_enums
CardTuple=(poker_enums.Card,poker_enums.Suit)
class RankCmp:
    def __init__(self,hand_rank:poker_enums.HandRank,card_rank:list[int],cards:list[CardTuple]):
        self.hand_rank=hand_rank
        self.card_rank=card_rank
        self.cards=cards
    def as_tuple(self):
        return (self.hand_rank,self.card_rank,self.cards)
    def __eq__(self,other):
        return self.hand_rank.value==other.hand_rank.value and self.card_rank==other.card_rank
    def __gt__(self,other):
        if(self.hand_rank.value>other.hand_rank.value): return True
        elif(self.hand_rank.value<other.hand_rank.value): return False
        else: return self.card_rank>other.card_rank
    def __lt__(self,other):
        if(self.hand_rank.value<other.hand_rank.value): return True
        elif(self.hand_rank.value>other.hand_rank.value): return False
        else: return self.card_rank<other.card_rank
class Hand:
    def __init__(self):
        self.hand:list[CardTuple]=[]
    def draw_from_deck(self,deck:poker_deck.Deck):
        assert(len(self.hand)!=5)
        self.hand=deck.get_cards(5)
    def put_back_hand(self,deck:poker_deck.Deck):
        deck.put_back_cards(self.hand)
    def get_hand_rank(self,ace_high:bool=False)->RankCmp:
        assert(len(self.hand)==5)
        use_hand=self.hand.copy() #Dont mutate hand
        if ace_high:
            for i in range(len(use_hand)):
                if use_hand[i][0]==poker_enums.Card.AceLow:
                    use_hand[i]=(poker_enums.Card.AceHigh,use_hand[i][1])
        sorted_cv=poker_deck.Deck.as_sorted_values(use_hand)
        is_straight=Hand.check_straight(sorted_cv)
        is_flush=Hand.check_same_suit(use_hand)
        highest_window_max,high_window,low_window=Hand.get_windows(sorted_cv)
        if is_straight and is_flush:
            if(sorted_cv!=[13,12,11,10,9]):
                rank=poker_enums.HandRank.StraightFlush
            else:
                rank=poker_enums.HandRank.RoyalFlush
            number_ranks=[sorted_cv[0]] #Gets number values from highest/lowest rankings
        elif highest_window_max==4:
            rank=poker_enums.HandRank.FourOfAKind
            number_ranks=[high_window]
            number_ranks.extend([e for e in sorted_cv if e not in number_ranks]) #Add the other numbers high/low as they're next in checking ranking
        elif highest_window_max==3 and low_window!=None:
            rank=poker_enums.HandRank.FullHouse
            number_ranks=[high_window,low_window]
        elif is_flush:
            rank=poker_enums.HandRank.Flush
            number_ranks=sorted_cv
        elif is_straight:
            rank=poker_enums.HandRank.Straight
            number_ranks=[sorted_cv[0]]
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
        return RankCmp(rank,number_ranks,use_hand)
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
hand1=Hand()
hand2=Hand()
deck=poker_deck.Deck()
deck.shuffle()
hand1.draw_from_deck(deck)
hand2.draw_from_deck(deck)
rc1=hand1.get_hand_rank()
rc2=hand2.get_hand_rank()
print("rc1",rc1.as_tuple())
print("rc2",rc2.as_tuple())
print("rc1==rc1?",rc1==rc1)
print("rc1==rc2?",rc1==rc2)
print("rc1>rc2?",rc1>rc2)
print("rc1<rc2?",rc1<rc2)
print("Highest rank",max(rc1,rc2).as_tuple())