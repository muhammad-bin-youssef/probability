from pathlib import Path
class All():
    ACCURACY = 16000

    APP = 'HAM_SPAM_TEST_1.db'

    #path_ham = '/home/mhy/Documents/py/probability/Bayes/tsoding_filter_spam/data/train/ham'
    #path_spam = '/home/mhy/Documents/py/probability/Bayes/tsoding_filter_spam/data/train/spam'
    try:
        path_spam = str(Path(__file__).parent / Path('train') / Path('spam'))
    except NameError:
        path_spam = str(Path.cwd() / Path('train') / Path('spam'))

    try:
        path_ham = str(Path(__file__).parent / Path('train') / Path('ham'))
    except NameError:
        path_ham = str(Path.cwd() / Path('train') / Path('ham'))
    HAM = 0
    SPAM = 0

    MESSAGE = '''

    Subject: inexpen , sive relief meds sold here
    hi again ,
    we now have over 94 meds available online now !
    we are having specials on xanax , vlagra , soma , amblen and vallum
    free clalls with every order
    more lnfo here

    '''
