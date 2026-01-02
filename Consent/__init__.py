from otree.api import *

author = 'Mart van der Kam & Anne Günther'

class C(BaseConstants):
    NAME_IN_URL = 'consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if subsession.session.config['language'] == "de":
        from .lexicon_de import Lexicon
        subsession.session.myLangCode = "_de"
    elif subsession.session.config['language'] == "sa":
        from .lexicon_sa import Lexicon
        subsession.session.myLangCode = "_sa"
    else:
        from .lexicon_usa import Lexicon
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
