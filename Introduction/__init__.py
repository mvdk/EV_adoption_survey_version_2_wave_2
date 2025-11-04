import random
from otree.api import *

author = 'Mart van der Kam & Anne Günther'

class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if subsession.session.config['language'] == 'de':
        from .lexicon_de import Lexicon
        subsession.session.myLangCode = "_de"
    elif subsession.session.config['language'] == 'sa':
        from .lexicon_sa import Lexicon
        subsession.session.myLangCode = "_sa"
    else:
        from .lexicon_usa import Lexicon
        subsession.session.myLangCode = "_usa"
    subsession.session.introductionLexi = Lexicon


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class introduction(Page):
    form_model = 'player'
    form_fields = []

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Lexicon': player.session.introductionLexi,
        }


# Page sequence
page_sequence = [
    introduction
]
