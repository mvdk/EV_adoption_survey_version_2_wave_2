from otree.api import *

author = 'Mart van der Kam & Anne Günther'

class C(BaseConstants):
    NAME_IN_URL = 'consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if subsession.session.config['language'] == "de" and subsession.session.config['car_size_future'] == "small":
        from .lexicon_de_small import Lexicon
        subsession.session.myLangCode = "_de"
    elif subsession.session.config['language'] == "de" and subsession.session.config['car_size_future'] == "medium":
        from .lexicon_de_medium import Lexicon
        subsession.session.myLangCode = "_de"
    elif subsession.session.config['language'] == "de" and subsession.session.config['car_size_future'] == "large":
        from .lexicon_de_large import Lexicon
        subsession.session.myLangCode = "_de"
    elif subsession.session.config['language'] == "sa" and subsession.session.config['car_size_future'] == "small":
        from .lexicon_sa_small import Lexicon
        subsession.session.myLangCode = "_sa"
    elif subsession.session.config['language'] == "sa" and subsession.session.config['car_size_future'] == "medium":
        from .lexicon_sa_medium import Lexicon
        subsession.session.myLangCode = "_sa"
    elif subsession.session.config['language'] == "sa" and subsession.session.config['car_size_future'] == "large":
        from .lexicon_sa_large import Lexicon
        subsession.session.myLangCode = "_sa"
    elif subsession.session.config['language'] == "usa" and subsession.session.config['car_size_future'] == "small":
        from .lexicon_usa_small import Lexicon
        subsession.session.myLangCode = "_usa"
    elif subsession.session.config['language'] == "usa" and subsession.session.config['car_size_future'] == "medium":
        from .lexicon_usa_medium import Lexicon
        subsession.session.myLangCode = "_usa"
    else:
        from .lexicon_usa_large import Lexicon
        subsession.session.myLangCode = "_usa"
    subsession.session.introLexi = Lexicon


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Consent fields
    dataScience = models.BooleanField(initial=False)
    dataTeach = models.BooleanField(initial=False)

    is_mobile = models.BooleanField()


class introduction_consent(Page):
    form_model = 'player'
    form_fields = ['dataScience', 'dataTeach']
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Lexicon': player.session.introLexi,
            "participantlabel": player.participant.label,
        }  # add http://evstudy.otree.psychologie.unibas.ch/join/kipenere?participant_label={{%PROLIFIC_PID%}} to link on prolific


class MobileCheck(Page):
    form_model = 'player'
    form_fields = ['is_mobile']

    def vars_for_template(player: Player):
        return {
            'Lexicon': player.session.introLexi,
        }

    def error_message(player: Player, values):
        if values['is_mobile']:
            return player.session.introLexi.mobile


page_sequence = [
    MobileCheck,
    introduction_consent
]
