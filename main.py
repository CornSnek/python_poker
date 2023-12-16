import poker_deck
import poker_enums
from poker_enums import HandRank,Card,ActionType
import random
CardTuple=(poker_enums.Card,poker_enums.Suit)
class RankCmp:
    def __init__(self,hand_rank:HandRank,card_rank:list[int],cards:list[CardTuple]):
        self.hand_rank=hand_rank
        self.card_rank=card_rank
        self.cards:list[CardTuple]=cards
    def other_cards(self,begin:int)->str:
        return "following the next card(s) in ranking ("+", ".join(Card(v).as_game_str() for v in self.card_rank[begin:])+")"
    def description(self)->str:
        begin_str=f"{self.hand_rank.as_game_str()}: {Card(self.card_rank[0]).as_game_str()}"
        if(self.hand_rank==HandRank.HighCard or self.hand_rank==HandRank.Straight):
            return f"{begin_str} as the highest, {self.other_cards(1)}"
        elif(self.hand_rank==HandRank.Pair):
            return f"{begin_str} as the pair, {self.other_cards(1)}"
        elif(self.hand_rank==HandRank.TwoPair):
            return f"{begin_str} as the highest pair, {Card(self.card_rank[1]).as_game_str()} as the lowest pair, {self.other_cards(2)}"
        elif(self.hand_rank==HandRank.ThreeOfAKind):
            return f"{begin_str} as the triplet, {self.other_cards(1)}"
        elif(self.hand_rank==HandRank.Flush or self.hand_rank==HandRank.StraightFlush or self.hand_rank==HandRank.RoyalFlush):
            return f"{begin_str} as the highest, {self.other_cards(1)}, all {poker_enums.suit_to_game_str[self.cards[0][1]]}"
        elif(self.hand_rank==HandRank.FullHouse):
            return f"{begin_str} as the triplet, {Card(self.card_rank[1]).as_game_str()} as the lowest pair, {self.other_cards(2)}"
        elif(self.hand_rank==HandRank.FourOfAKind):
            return f"{begin_str} as the quartet, {self.other_cards(1)}"
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
    def _set_deck_hand(self,cards:list[CardTuple]):
        """Used for testing purposes"""
        self.__deck_hand=cards
    def draw_from_deck(self,deck:poker_deck.Deck):
        assert(len(self.__deck_hand)!=5)
        self.__deck_hand=deck.get_cards(5)
    def put_back_hand(self,deck:poker_deck.Deck):
        deck.put_back_cards(self.__deck_hand)
    def replace_hand(self,deck:poker_deck.Deck,cards_to_replace:list[int]):
        for at_i in cards_to_replace:
            deck.replace_one_card(self.__deck_hand,at_i)
    def get_hand_rank(self)->RankCmp:
        return max(self.__get_hand_rank(),self.__get_hand_rank(ace_high=True)) #Check both hands for maximum if Ace is low/high.
    def __get_hand_rank(self,ace_high:bool=False)->RankCmp:
        assert(len(self.__deck_hand)==5)
        use_hand=self.__deck_hand.copy() #Dont mutate deck_hand
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
                rank=HandRank.StraightFlush
            else:
                rank=HandRank.RoyalFlush
            number_ranks=[sorted_cv[0]]
        elif highest_window_max==4:
            rank=HandRank.FourOfAKind
            number_ranks=[high_window]
            number_ranks.extend([e for e in sorted_cv if e not in number_ranks]) #Add the other numbers high/low as they're next in checking ranking
        elif highest_window_max==3 and low_window!=None:
            rank=HandRank.FullHouse
            number_ranks=[high_window,low_window]
        elif is_flush:
            rank=HandRank.Flush
            number_ranks=sorted_cv
        elif is_straight:
            rank=HandRank.Straight
            number_ranks=[sorted_cv[0]]
        elif highest_window_max==3:
            rank=HandRank.ThreeOfAKind
            number_ranks=[high_window]
            number_ranks.extend([e for e in sorted_cv if e not in number_ranks])
        elif highest_window_max==2:
            if low_window!=None:
                rank=HandRank.TwoPair
                number_ranks=[high_window,low_window]
                number_ranks.extend([e for e in sorted_cv if e not in number_ranks])
            else:
                rank=HandRank.Pair
                number_ranks=[high_window]
                number_ranks.extend([e for e in sorted_cv if e not in number_ranks])
        else:
            rank=HandRank.HighCard
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
class GameLoop:
    def __init__(self,computers_len):
        self.deck=poker_deck.Deck()
        self.players_hands=[Hand() for _ in range(computers_len+1)]
        self.num_players=computers_len+1
        self.game_loop=True
    def initialize_new_game_loop(self):
        self.players_rankings:list[RankCmp|None]=[None for _ in range(computers_len+1)]
        self.players_option:list[ActionType|None]=[None for _ in range(computers_len+1)]
        self.winning_players:list[int]=[] #list[int] as they're may be more than 1 player
        self.winning_reason:str=""
        self.last_option=ActionType.Check
        self.deck.shuffle()
        for i,hand in enumerate(self.players_hands):
            hand.draw_from_deck(self.deck)
            self.players_rankings[i]=hand.get_hand_rank()
        self.player_i=random.randint(0,computers_len)
        print(f"Player {self.player_i+1} will go first")
    def get_next_player_or_phase(self)->False:
        if self.players_option.count(ActionType.Fold)==self.num_players-1:
            self.winning_players=[p for p in range(self.num_players) if self.players_option[p]!=ActionType.Fold]
            self.winning_reason="All other players have folded."
            return False
        while True:
            self.player_i=(self.player_i+1)%self.num_players
            if(self.players_option[self.player_i]!=ActionType.Fold):
                return True
    def any_player_has_won(self)->bool:
        if len(self.winning_players)==0:
            return False
        else:
            player_won_str="Player "
            player_won_str+=", ".join(str(wp+1) for wp in self.winning_players)
            print(f"{player_won_str} won. Reason: {self.winning_reason}")
        players_no_fold=[(p,p_ranking) for p,p_ranking in enumerate(self.players_rankings) if self.players_option[p]!=ActionType.Fold]
        players_with_fold=[(p,p_ranking) for p,p_ranking in enumerate(self.players_rankings) if self.players_option[p]==ActionType.Fold]
        print("Players who did not fold:")
        for p,p_ranking in players_no_fold:
            hand_print=','.join([ f"[{c.as_game_str()}{s.as_game_str()}]" for c,s in p_ranking.cards ])
            print(f"Player {p+1}'s hand: {hand_print}\nRanking: {p_ranking.description()}")
        print("Players who folded:")
        for p,p_ranking in players_with_fold:
            hand_print=','.join([ f"[{c.as_game_str()}{s.as_game_str()}]" for c,s in p_ranking.cards ])
            print(f"Player {p+1}'s hand: {hand_print}\nRanking: {p_ranking.description()}")
        for hand in self.players_hands:
            hand.put_back_hand(self.deck)
        while True:
            if((inp:=input("Play again? Y/N or y/n >> ")).lower()=="y"):
                break
            elif(inp.lower()=="n"):
                self.game_loop=False
                break
        return True
    def put_all_cards_back_in_deck(self):
        for hand in self.players_hands:
            hand.put_back_hand(self.deck)
    def do_game_loop(self):
        while self.game_loop:
            self.deck.check_if_deck_unique()
            self.initialize_new_game_loop()
            self.do_betting_phase()
            if(self.any_player_has_won()):
                self.put_all_cards_back_in_deck()
                continue
            self.do_draw_phase()
            for p,hand in enumerate(self.players_hands): #Get new hand rankings
                self.players_rankings[p]=hand.get_hand_rank()
            self.last_option=ActionType.Check
            self.do_betting_phase()
            if len(self.winning_players)==0:
                self.winning_reason="Player(s) have the highest ranking cards and did not fold"
                possible_wins=[(p,pr) for p,pr in enumerate(self.players_rankings) if self.players_option[p]!=ActionType.Fold]
                assert(len(possible_wins)>=2)
                max_card:RankCmp=RankCmp(HandRank.MinRank,[],[])
                for i in range(len(possible_wins)):
                    pw=possible_wins[i]
                    if(pw[1]>max_card): #1 winner
                        self.winning_players=[pw[0]]
                        max_card=pw[1]
                    elif(pw[1]==max_card): #Tie may happen
                        self.winning_players.append(pw[0])
            self.any_player_has_won()
            self.put_all_cards_back_in_deck()
    def do_betting_phase(self):
        players_ok:list[bool]=[False for _ in range(self.num_players)] #See if all players has Checked, Called, or Raised/Betted with Calls
        check_state_machine:bool=False #False is if all players used Check, True is if all players used Call after a Bet/Raise
        while True:
            player_choice=None
            if(self.player_i==0):
                p_ranking=self.players_rankings[0]
                hand_print=','.join([ f"[{c.as_game_str()}{s.as_game_str()}]" for c,s in p_ranking.cards ])
                print(f"It's your turn:\nYour current hand: {hand_print}\nCurrent ranking: {p_ranking.description()}")
                while(True):
                    input_option=input(f"What will you do?\n{self.last_option.as_game_str_options()} >> ")
                    if((player_choice:=ActionType.get_input_option(self.last_option,input_option))!=None):
                        print(player_choice.game_description(self.player_i))
                        break
                    else:
                        print(f"Invalid option: '{input_option}'. Try again!")
            else:
                print(f"It's player {self.player_i+1}'s turn.")
                computer_prob=poker_enums.hand_rank_choose_probability[self.players_rankings[self.player_i].hand_rank]
                available_options=self.last_option.get_options()
                #Redistribute non-used probabilites to other options
                leftover_prob=sum(v for k,v in computer_prob.items() if k not in available_options)
                new_computer_prob=[v+leftover_prob/len(available_options) for k,v in computer_prob.items() if k in available_options]
                new_sum_prob=0
                for i,v in enumerate(new_computer_prob):
                    new_computer_prob[i]=v/100+new_sum_prob
                    new_sum_prob+=v/100
                rand0to1=random.random()
                for option,option_p in zip(available_options,new_computer_prob):
                    if rand0to1<option_p:
                        player_choice=option
                        break
                print(player_choice.game_description(self.player_i))
            assert(player_choice!=None)
            self.players_option[self.player_i]=player_choice
            if not check_state_machine:
                if player_choice==ActionType.Bet:
                    players_ok=[False for _ in range(self.num_players)]
                    check_state_machine=True
            else:
                if player_choice==ActionType.Raise:
                    players_ok=[False for _ in range(self.num_players)]
            players_ok[self.player_i]=True
            if player_choice!=ActionType.Fold:
                self.last_option=player_choice
            if(not self.get_next_player_or_phase()): break
            new_players_ok=[is_ok for po,is_ok in zip(self.players_option,players_ok) if po!=ActionType.Fold] #Check if true for non Folded players
            if(all(new_players_ok)): break 
    def do_draw_phase(self):
        while True:
            choice=input("What cards do you want to discard? Format: Comma separated values from 1 to 5. Type nothing to keep all cards. Example 1,2,4 is a valid option. >> ")
            try:
                if choice=='': break
                numbers=[int(s)-1 for s in choice.split(',')]
                assert(all(0<=n<=4 for n in numbers))
                self.players_hands[0].replace_hand(self.deck,numbers)
                break
            except:
                print(f"Invalid choice or number/range: '{choice}'. Try again!")
if __name__ == '__main__':
    while True:
        computers_str=input("You are playing a simulation of Draw Poker.\nHow many computer players will play (1-3)? 0 to exit >> ")
        if(len(computers_str)==1 and '0'<=computers_str<='3'):
            if(computers_str=='0'): exit()
            computers_len=int(computers_str)
            break
        else:
            print(f"Invalid string '{computers_str}'")
    GL=GameLoop(computers_len)
    GL.do_game_loop()