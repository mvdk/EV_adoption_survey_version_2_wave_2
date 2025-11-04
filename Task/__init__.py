from otree.api import *
import random

author = 'Mart van der Kam & Anne Günther'

doc = """
Choice experiment task
"""


# Constants
class Constants(BaseConstants):
    name_in_url = 'Task'
    players_per_group = None
    blocks = ['product_v3', 'product_v4']
    trials_per_block = 18
    num_rounds = 18
    possible_orders = [
        ['product_v3'],
        ['product_v4'],
    ]

    from .attributes_usa import (
        attributes_version_3_small as attributes_version_3_small_usa,
        attributes_version_4_small  as attributes_version_4_small_usa,
        attributes_version_3_medium  as attributes_version_3_medium_usa,
        attributes_version_4_medium  as attributes_version_4_medium_usa,
        attributes_version_3_large  as attributes_version_3_large_usa,
        attributes_version_4_large  as attributes_version_4_large_usa,
        attributes_version_3_small  as attributes_version_3_listA_none_usa,
        attributes_version_4_small  as attributes_version_4_listB_none_usa,
    )

    from .attributes_de import (
        attributes_version_3_small as attributes_version_3_small_de,
        attributes_version_4_small  as attributes_version_4_small_de,
        attributes_version_3_medium  as attributes_version_3_medium_de,
        attributes_version_4_medium  as attributes_version_4_medium_de,
        attributes_version_3_large  as attributes_version_3_large_de,
        attributes_version_4_large  as attributes_version_4_large_de,
        attributes_version_3_small  as attributes_version_3_listA_none_de,
        attributes_version_4_small  as attributes_version_4_listB_none_de,
    )
    
    from .attributes_sa import (
        attributes_version_3_small as attributes_version_3_small_sa,
        attributes_version_4_small  as attributes_version_4_small_sa,
        attributes_version_3_medium  as attributes_version_3_medium_sa,
        attributes_version_4_medium  as attributes_version_4_medium_sa,
        attributes_version_3_large  as attributes_version_3_large_sa,
        attributes_version_4_large  as attributes_version_4_large_sa,
        attributes_version_3_small  as attributes_version_3_listA_none_sa,
        attributes_version_4_small  as attributes_version_4_listB_none_sa,
    )

# Subsession
class Subsession(BaseSubsession):
    pass


# Group
class Group(BaseGroup):
    pass


# Player
class Player(BasePlayer):


    # Add a field to store the radio button decision
    choice = models.StringField(
        choices=["Yes", "No"],
        widget=widgets.RadioSelectHorizontal,
    )

    current_task = models.IntegerField(initial=0)
    block = models.StringField()
    current_task_pol = models.IntegerField(initial=0)



def creating_session(subsession: Subsession):
    if subsession.session.config['language'] == 'de':
        from .lexicon_de import Lexicon
        subsession.session.myLangCode = "_de"
    elif subsession.session.config['language'] == "sa":
        from .lexicon_sa import Lexicon
        subsession.session.myLangCode = "_sa"
    else:
        from .lexicon_usa import Lexicon
        subsession.session.myLangCode = "_usa"
    subsession.session.taskLexi = Lexicon
    

    if subsession.round_number == 1:
        for p in subsession.get_players():
            tasks = ['TaskPage'] * Constants.num_rounds
            random.shuffle(tasks)
            task_rounds = dict(zip(tasks, range(1, len(tasks) + 1)))
            p.participant.task_rounds = task_rounds

    if subsession.round_number <= Constants.num_rounds:
        trials_per_block = Constants.trials_per_block

        for p in subsession.get_players():
            possible_orders = Constants.possible_orders.copy()

            block_order = random.choice(possible_orders)

            randomized_sequence = []

            # Generate a sequence that completes all trials for each block before moving on to the next block
            for block in block_order:
                block_sequence = [(block, trial_number) for trial_number in range(1, trials_per_block + 1)]
                random.shuffle(block_sequence)
                randomized_sequence.extend(block_sequence)

            p.participant.task_rounds = randomized_sequence
            p.participant.vars['randomized_sequence'] = randomized_sequence


# Page with Blocks A, B, C, D, E
class TaskPage(Page):
    form_model = 'player'
    form_fields = ['choice']

    def is_displayed(player):
        print(f"[DEBUG] Round: {player.round_number}, Constants.num_rounds = {Constants.num_rounds}")
        return player.round_number <= Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        # Ensure that randomized_sequence is set before trying to access it
        if player.session.config['language'] == "de":
            attributes_version_3_small = Constants.attributes_version_3_small_de
            attributes_version_4_small = Constants.attributes_version_4_small_de
            attributes_version_3_medium = Constants.attributes_version_3_medium_de
            attributes_version_4_medium = Constants.attributes_version_4_medium_de
            attributes_version_3_large = Constants.attributes_version_3_large_de
            attributes_version_4_large = Constants.attributes_version_4_large_de
        elif player.session.config['language'] == "sa":
            attributes_version_3_small = Constants.attributes_version_3_small_sa
            attributes_version_4_small = Constants.attributes_version_4_small_sa
            attributes_version_3_medium = Constants.attributes_version_3_medium_sa
            attributes_version_4_medium = Constants.attributes_version_4_medium_sa
            attributes_version_3_large = Constants.attributes_version_3_large_sa
            attributes_version_4_large = Constants.attributes_version_4_large_sa
        else:
            attributes_version_3_small = Constants.attributes_version_3_small_usa
            attributes_version_4_small = Constants.attributes_version_4_small_usa
            attributes_version_3_medium = Constants.attributes_version_3_medium_usa
            attributes_version_4_medium = Constants.attributes_version_4_medium_usa
            attributes_version_3_large = Constants.attributes_version_3_large_usa
            attributes_version_4_large = Constants.attributes_version_4_large_usa
        Lexicon = player.session.taskLexi

        if 'randomized_sequence' not in player.participant.vars:
            print("DEBUG: 'randomized_sequence' not found in participant.vars. Calling creating_session.")

        print(player.round_number)
        current_task_tuple = player.participant.task_rounds[player.round_number - 1]

        if not isinstance(current_task_tuple, tuple) or len(current_task_tuple) != 2:
            # Handle the case where current_task_tuple is not a tuple of length 2
            current_task_tuple = ('', 0)

        block, trial_number = current_task_tuple
        print(f"DEBUG: current_task_tuple: {current_task_tuple}, block: {block}, trial_number: {trial_number}")

        player.block = block
        player.current_task = trial_number

        # Define which blocks are product choice and which is the policy block
        disruption_block = player.block in ['product_v3', 'product_v4']

        round_number = player.round_number

        # Specify the rounds where the message is supposed to be visually attractive -> first trials of each block
        attractive_rounds = {1, 19, 37}
        # Check if trial_number is in attractive_rounds = first trial of the block
        is_first_trial_of_block = player.round_number in attractive_rounds

        # Well done rounds
        well_done = {19, 37}
        completed_block = player.round_number in well_done

        # Conditionally choose the attributes lists based on the "car_size_future" value and block
        if player.session.config['car_size_future'] == 'small':
            attributes_list = {
                'product_v3': attributes_version_3_small,
                'product_v4': attributes_version_4_small,
            }
        elif player.session.config['car_size_future'] == 'medium':
            attributes_list = {
                'product_v3': attributes_version_3_medium,
                'product_v4': attributes_version_4_medium,
            }
        else:
            attributes_list = {
                'product_v3': attributes_version_3_large,
                'product_v4': attributes_version_4_large,
            }

        try:
            if block == 'product_v3' or block == 'product_v4':
            # Retrieve the attributes_list for the given block
                current_attributes_list = attributes_list[block]
                if not current_attributes_list:
                    print("DEBUG: current_attributes_list is empty. Available blocks:", attributes_list.keys())
                    raise KeyError(f"Block {block} not found in attributes_list")
                # Retrieve the attributes for the given trial_number
                attributes = current_attributes_list[trial_number - 1]
                if 'shuffled_attributes_disruption' not in player.participant.vars:
                    keys_list = list(attributes.keys())
                # UNCOMMENT FUNCTION BELOW TO RANDOMIZE ATTRIBUTE ORDER
                    #random.shuffle(keys_list)
                    player.participant.vars['keys_list'] = keys_list
                    shuffled_attributes = {key: attributes[key] for key in keys_list}
                    player.participant.vars['shuffled_attributes_disruption'] = shuffled_attributes
                else:
                    shuffled_attributes = {key: attributes[key] for key in player.participant.vars['keys_list']}
        except KeyError:
            print("DEBUG: KeyError occurred. Available blocks:", attributes_list.keys())
            raise

        return {
            "attributes": shuffled_attributes,
            "current_task": trial_number,  # Set current_task to the extracted trial_number
            "block": block,  # Include the block information
            "round_number": round_number,
            "is_first_trial_of_block": is_first_trial_of_block,
            "completed_block": completed_block,
            "disruption_block": disruption_block,
            "Lexicon": Lexicon,
        }

# Page sequence
page_sequence = [TaskPage]