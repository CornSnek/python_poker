import poker_deck
import poker_enums
import random
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
        self.__deck_hand:list[CardTuple]=[]
    def set_deck_hand(self,cards:list[CardTuple]):
        self.__deck_hand=cards
    def draw_from_deck(self,deck:poker_deck.Deck):
        assert(len(self.__deck_hand)!=5)
        self.__deck_hand=deck.get_cards(5)
    def put_back_hand(self,deck:poker_deck.Deck):
        deck.put_back_cards(self.__deck_hand)
    def get_hand_rank(self)->RankCmp:
        return max(self.__get_hand_rank(),self.__get_hand_rank(ace_high=True)) #Check both hands for maximum if Ace is low/high.
    def __get_hand_rank(self,ace_high:bool=False)->RankCmp:
        assert(len(self.__deck_hand)==5)
        use_hand=self.__deck_hand.copy() #Dont mutate hand
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

if __name__ == '__main__':
    while True:
        computers_str=input("You are playing a simulation of Draw Poker.\nHow many computer players will play (1-3)? 0 to exit >> ")
        if(len(computers_str)==1 and '0'<=computers_str<='3'):
            if(computers_str=='0'): exit()
            computers_len=int(computers_str)
            break
        else:
            print(f"Invalid string '{computers_str}'")
    players_hands=[Hand() for _ in range(computers_len+1)]
    players_rankings:list[RankCmp|None]=[None for _ in range(computers_len+1)]
    num_players=computers_len+1

    game_loop=True
    def next_player(player_i:int)->int:
        return (player_i+1)%num_players
    while game_loop:
        all_bets_placed=False
        deck=poker_deck.Deck()
        deck.shuffle()
        for i,hand in enumerate(players_hands):
            hand.draw_from_deck(deck)
            players_rankings[i]=hand.get_hand_rank()
        player_i=random.randint(0,computers_len)
        print(f"Player {player_i+1} will go first")
        while(True):
            if(player_i==0):
                p_ranking=players_rankings[0]
                hand_print=','.join([ f"[{c.as_game_str()}{s.as_game_str()}]" for c,s in p_ranking.cards ])
                print(f"It's your turn:\nYour current hand: {hand_print}\nCurrent Hand Ranking: {p_ranking.hand_rank.as_str_name()}\n")
                input("What will you do?\nTODO >> ")
            else:
                print(f"Player {player_i+1}'s turn: ")
            player_i=next_player(player_i)