import numpy as np
from enum import IntEnum
from random import shuffle
from rlcard.games.keezen.player import Player


class Card:
    """Card type. Has an id, suit and card value."""

    def __init__(self, suit, card_value, id_):
        self.suit = suit
        self.card_value = card_value
        self.id_ = id_

    def __str__(self):
        return "Card[{0}]: {1} {2}".format(self.id_, self.suit.name, self. card_value.name)


class CardState:
    """Helps to manage the positions of all cards."""

    @staticmethod
    def get_initial_card_state(cards: [Card], players):
        stock_cards: [Card] = cards.copy()
        player_cards: {Player: [Card]} = {}
        for player in players:
            player_cards[player] = []
        played_cards: [Card] = []
        shuffle(stock_cards)
        return stock_cards, player_cards, played_cards

    @staticmethod
    def reset(stock_cards, player_cards, played_cards):
        """Resets the stock and shuffles."""
        stock_cards.extend(played_cards)
        played_cards.clear()
        for player in player_cards.keys():
            cards = player_cards[player]
            stock_cards.extend(cards)
            player_cards[player] = []
        shuffle(stock_cards)

    @staticmethod
    def deal_card(player, stock_cards, player_cards) -> Card:
        """Deal a card to a player."""
        card: Card = stock_cards.pop()
        player_cards[player].append(card)
        return card

    @staticmethod
    def play_cards(player, cards, player_cards, played_cards):
        """Play multiple cards (throw all)."""
        played_cards.extend(cards)
        if len(cards) == 1:
            player_cards[player].remove(cards[0])
        else:
            player_cards[player].clear()

    @staticmethod
    def get_card_state_as_matrix(cards: [Card]):
        """Returns the cards in a 5x13 matrix."""
        indices = [0]*13
        for card in cards:
            card_index = card.card_value.value - 1
            indices[card_index] = indices[card_index] + 1
        card_state = np.zeros((5, 13), dtype=np.int8)
        for i, index in enumerate(indices):
            if index == 1:
                card_state[index][i] = 1
        flat = card_state.flatten('F')
        return flat  # card_state


class Suit(IntEnum):
    DIAMONDS = 0
    HEARTS = 1
    CLUBS = 2
    SPADES = 3


class CardValue(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
