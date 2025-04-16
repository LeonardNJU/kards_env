from card import Card


class Deck:
    def __init__(self,cards:list[Card]):
        assert len(cards)==40
        self.cards = cards
        self.shuffle()
        
    def draw(self)->Card:
        '''
        draw a card from the deck
        will raise an IndexError if the deck is empty
        '''
        return self.cards.pop()
    def shuffle(self):
        '''
        shuffle the deck
        '''
        import random
        random.shuffle(self.cards)
    def __len__(self)->int:
        '''
        return the number of cards in the deck
        '''
        return len(self.cards)
    def random_add(self,card:Card):
        '''
        add a card to the deck at a random position
        '''
        import random
        self.cards.insert(random.randint(0,len(self.cards)),card)