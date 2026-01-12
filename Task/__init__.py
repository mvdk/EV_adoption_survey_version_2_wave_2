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

       # Conditionally choose the attributes lists based on their chosen car size future catagory of the previous wave (participant_id) and block
        participant_id = player.participant.label
        car_size_future_small_IDs = ['test-small','FFE1DC0E-FF7D-479D-B4BB-A1E14E4AEA88','870AA1DF-A1AD-45DA-9B67-4CF31F25079F','34ED9041-1CE5-4DFE-B7BC-297DFE86B56C',
                                     '8B942464-02A1-422B-B22E-C4E5E5860A09','216B73FC-61DB-4F6F-BACA-75F032B0E4B0','34CF9468-107A-43F2-B190-DBFB56ADE0EB','074CB595-AE70-470A-956A-07762ECCC76C',
                                     '2975A3C5-D127-4A63-8689-31D21711327B','6FCE484B-76B4-4A42-99E1-44B06C51E16F','1E7DC7C1-9536-4A21-A7B7-96B27AD5B071','B4E8E7A8-332B-4270-8EE2-104021D0CE21',
                                     '7523913E-0279-45CA-A3C1-00D373D7ECC8','7BACA641-B33A-40C1-9E2B-E7B1B5C6666E','8A1DFC02-4919-4767-AC46-95588D890D4C','91673D75-F0BD-483D-B7BF-8F265AF960AE',
                                     '6E567B10-06D1-4539-A751-04725893107E','939C07EA-402A-4C9F-8C24-07D3EEC1BA89','434E9370-CB62-4B61-94BE-68A7A17DAAAA','8263D59C-C425-46D1-9542-79F5CF4C6951',
                                     '82534EF4-A62B-40AF-AA76-59A21114A5B8','04F09368-2961-48B2-A8C1-04A57CAA1DC5','5F5CD2BD-B4D8-407E-9CBA-4B79248C087D','71CB6266-254E-4D80-B36D-66972EA6A650',
                                     'E7D73AA3-4B37-495E-BDB2-AA98BC2F3D8B','30B025A2-06FB-4E97-9D58-B16E496F6319','386772F2-CD5E-4A22-AC32-C8381F108B82','FE226C61-1B82-43DD-81FC-281E7A4E3CC2',
                                     '0A5BC568-7E8B-4FB2-BACC-40EC8639A2A3','3D810C1A-FA57-4FE7-BADB-18CAFA40A857','1EF90921-D60B-4721-818C-7B6E20763F6D','96FCAEF1-B8EE-4D48-A0F2-C8EFA972109D',
                                     '17FF3C5B-ECF5-4042-9918-318A5B824F92','16B95450-4BC0-4FF6-B99D-683F2F8E3A6C','ACC5BE15-9472-468A-AB83-76EA28C7DC5D','95840B7C-B315-480E-8A70-A52EF5A41E8C',
                                     '3EF01F95-9268-4826-B5DF-6A6CC74AA42A','F4E13708-A966-467F-8FAE-1D991B808F71','E6131ABA-97DD-4EDF-905F-0462EF5E82EE','3ADBAF6C-94A7-4E19-A51F-D2A474F5F653',
                                     '55AAA980-7926-4F52-AD9B-1E7EAB0B829C','8A79371E-0969-4A42-8E34-9A8DD6B404A9','0F1BCCCB-BDC8-4E4D-8760-EF56C2C1899C','34F84E21-EF61-447D-8C2B-8B20D6D0F0DF',
                                     'FA6EE98C-6084-45EE-ACB3-B5678EADBDFA','6D8A4C12-A14B-4EA5-B06A-86887ECE6266','749FA92D-2381-4ACA-90AC-81EBB109E634','11A346D4-C8E1-4AA1-BE36-135D43E8593C',
                                     'E5A3FCA2-02C0-45D4-9C68-F6AFE387DDB4','BDE0FDFC-A9D5-4F74-B17B-188901C26431','2C1E2E40-DB68-4090-AC02-F520CC24557B','C7E6970B-71B1-4F0C-8FD2-DD79375A9DD0',
                                     '93E9406B-7697-4A76-B283-4FA56379E174','14A4D37C-81E2-4B29-9D4B-8CD159F9D6A0','1D64CA52-FD9F-4A5F-AC72-E9248CD65A30','53BC3C19-8089-43E3-A7F8-651C660E2331',
                                     '77020AB7-DB1A-45B2-84B7-C37B51A4D6C7','D9FC824F-DB5B-4224-9AAA-CE3D069A5F28','EA7DA69F-CD98-45C7-8131-540818246DE4','269BFA8B-DA54-4113-99D7-2D61B73D754D',
                                     '1ACF0987-01FC-49A9-B72A-393B6B27D47D','089E1512-9844-41F5-A934-8FC4472251DE','4294D65C-2C1D-47A3-A22C-DCE18C51799D','F9F9117A-CB0B-402C-83BA-291E9749A140',
                                     'E87CA4AF-6C82-4137-87D3-92165D2D2CF7','73C46EF9-04CF-494F-BA57-AC12B54102EC','90E0DE8D-A30D-4C0F-87A4-6CF805DBC987','EA62164B-CD72-4249-9F65-1E95EC0F652E',
                                     '1D3C19D0-A132-4744-A37E-B2F9767D5E6E','384D446D-8E4B-485B-92B0-451F1C9481CB','E7CD8760-C5D7-484B-87C0-5EF433A1321A','956CC396-3B34-4BD3-85AA-1D343E5D7C75',
                                     'EE30050D-6B15-4FFA-847C-78F0D9650707','BD4B184A-72EB-4ABD-AC1B-505CD277198A','BD06ADDF-A5B4-452B-ACBA-CC6886D89113','46BC10E2-46F3-4F1A-8CDE-15F959E86C41',
                                     '26B3CB20-8B54-4F00-BF8D-79B790E442B6','9D142DA9-FD6B-46F5-8EBD-52BE489B340C','E9C721ED-66E9-4B72-A3E1-00A72B1981BE','BEF223FA-8478-43C6-B406-88F35351B587',
                                     'BBCB67B1-9891-418F-8847-2AA262EA3C14','7D09C196-BE2C-4C46-BCDB-E8AAF27B4394','0DC6BF60-88AA-4D10-B034-E7D86A3143F6','48A63182-32AF-491A-88F9-B9929797D0A9',
                                     'A73B4D11-082D-4693-B398-CD840EB85D54','E506473E-7C1C-4106-8195-550E2F6AC710','813AFE93-2FF4-4363-BCEA-7C1C8F2D0A1D','56CD06F4-E43C-430D-911F-F58C5FE1CB3A']
        car_size_future_large_IDs = ['test-large',
                                     '439E86A2-670E-48B5-9D59-C05219B27168','50A2C349-E6DE-4A93-B270-3F37EAA74939','4F1BCEA1-5515-45DB-8E46-AFE47CD10D10','A779D184-D7E4-4224-A967-0D8805F6C9EA',
                                     'E40A0BE9-EB1D-4C73-9247-D97B0D4AB216','CAB1D1E8-8D7E-46AF-92A8-4AA3DE855DBD','EC3D0F20-07BD-4C5D-8891-4C1C4F27B2BA','C7230D14-5EF0-4D55-9BCA-3E61758420A2',
                                     'FD030F08-E68A-44DB-ADA6-0D86F55FF937','DAFA3AAD-F9E3-413C-BE37-FDF8E39318E9','B1898C75-C53D-4766-BC8F-8767B8356CCD','2BA8435F-6124-436D-BD8A-5B9083D48CF2',
                                     '61EE5860-7A7E-4D38-9153-9346DB4CC6E5','DC50A36F-5B8F-429C-A12F-E5030FC91A3C','B050D159-ED52-4851-868F-1E5B9B9AE21F','F8B31890-0EAD-4B94-AC4E-9F41FD95F731',
                                     '032F6E9B-BCB2-40C1-9E1E-67E3948F152B','2C282D48-1034-4998-970F-DD5B51EBC27A','C533581C-125E-45F7-BA1D-AAD09115BDEC','2E0A3C55-4089-4380-9791-5CBEBA2B69F7',
                                     '12C2FD3C-22A9-48D9-9CAA-A48081908E76','C157D2DE-AB05-477C-9725-069B1079745E','8B07A91C-8034-4129-A7B3-DDEFF674E2EB','7D871014-E167-494E-B4F8-A04DE7C21A25']

        if participant_id in car_size_future_small_IDs:
            attributes_list = {
                'product_v3': attributes_version_3_small,
                'product_v4': attributes_version_4_small,
            }
        elif participant_id in car_size_future_large_IDs:
            attributes_list = {
                'product_v3': attributes_version_3_large,
                'product_v4': attributes_version_4_large,
            }
        else:
            attributes_list = {
                'product_v3': attributes_version_3_medium,
                'product_v4': attributes_version_4_medium,
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
