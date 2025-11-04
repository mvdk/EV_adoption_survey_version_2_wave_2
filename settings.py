from os import environ

author = 'Mart van der Kam & Anne Günther'


SESSION_CONFIGS = [
    dict(
       name='USA_small',
       display_name="USA_Intervention_Study_small",
       num_demo_participants=5,
       language="usa",
       car_size_future="small",
       app_sequence=['Consent',
                     'Introduction',
                     'Task',
                     'End',]
     ),
    dict(
       name='Germany_small',
       display_name="Germany_Intervention_Study_small",
       num_demo_participants=5,
       language="de",
       car_size_future="small",
       app_sequence=['Consent',
                     'Introduction',
                     'Task',
                     'End',]
     ),
    dict(
        name='SouthAfrica_small',
        display_name="SA_Intervention_Study_small",
        num_demo_participants=5,
        language="sa",
        car_size_future="small",
        app_sequence=['Consent',
                      'Introduction',
                      'Task',
                      'End',]
    ),
        dict(
       name='USA_medium',
       display_name="USA_Intervention_Study_medium",
       num_demo_participants=5,
       language="usa",
       car_size_future="medium",
       app_sequence=['Consent',
                     'Introduction',
                     'Task',
                     'End',]
     ),
    dict(
       name='Germany_medium',
       display_name="Germany_Intervention_Study_medium",
       num_demo_participants=5,
       language="de",
       car_size_future="medium",
       app_sequence=['Consent',
                     'Introduction',
                     'Task',
                     'End',]
     ),
    dict(
        name='SouthAfrica_medium',
        display_name="SA_Intervention_Study_medium",
        num_demo_participants=5,
        language="sa",
        car_size_future="medium",
        app_sequence=['Consent',
                      'Introduction',
                      'Task',
                      'End',]
    ),
        dict(
       name='USA_large',
       display_name="USA_Intervention_Study_large",
       num_demo_participants=5,
       language="usa",
       car_size_future="large",
       app_sequence=['Consent',
                     'Introduction',
                     'Task',
                     'End',]
     ),
    dict(
       name='Germany_large',
       display_name="Germany_Intervention_Study_large",
       num_demo_participants=5,
       language="de",
       car_size_future="large",
       app_sequence=['Consent',
                     'Introduction',
                     'Task',
                     'End',]
     ),
    dict(
        name='SouthAfrica_large',
        display_name="SA_Intervention_Study_large",
        num_demo_participants=5,
        language="sa",
        car_size_future="large",
        app_sequence=['Consent',
                      'Introduction',
                      'Task',
                      'End',]
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'task_rounds',
]


SESSION_FIELDS = [
    'introLexi',

    'introductionLexi',

    'taskLexi',

    'endLexi',

    'myLangCode'
]

# ISO-639 code

LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '3153268574945'

INSTALLED_APPS = ['otree', 'django_extensions']
