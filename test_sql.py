import sqlite3
import math
from collections import Counter
import time

APP = 'HAM_SPAM_TEST.db'
MESSAGE = '''

Subject: inexpen , sive relief meds sold here
hi again ,
we now have over 94 meds available online now !
we are having specials on xanax , vlagra , soma , amblen and vallum
free clalls with every order
more lnfo here

'''

def main():
    t1 = time.perf_counter()
    db = sqlite3.connect(APP)
    db.create_function('LOG', 1, math.log)
    cr = db.cursor()

    cr.execute('SELECT * FROM main LIMIT 1')
    result = cr.fetchone()
    if not result:
        assert('DB Error: Main table empty')
    total_ham_words, total_spam_words = result

    prior_spam = math.log(total_spam_words / (total_ham_words + total_spam_words))
    prior_ham = math.log(total_ham_words / (total_ham_words + total_spam_words))
    
    words_list = MESSAGE.upper().split()
    if not words_list:
        return "HAM" 
    
    place_holder = ','.join(['(?)'] * len(words_list))

    smooth_ham = 1 / (1 + total_ham_words)
    smooth_spam = 1 / (1 + total_spam_words)
    
    query = f'''
    WITH raw_mess(word) AS 
    (
        Values {place_holder}
    ),
    counted_mess AS(
    SELECT word, COUNT(*) as n FROM raw_mess GROUP BY word
    ),

    ham_score AS(
    SELECT {prior_ham} + SUM(counted_mess.n * 
    LOG(COALESCE(ham.probability, {smooth_ham}))) as score
    FROM counted_mess 
    LEFT JOIN ham on counted_mess.word = ham.name
    ),

    spam_score AS(
    SELECT {prior_spam} + SUM(counted_mess.n * 
    LOG(COALESCE(spam.probability, {smooth_spam}))) as score
    FROM counted_mess
    LEFT JOIN spam on counted_mess.word = spam.name
    )
    SELECT 
        (SELECT score FROM ham_score),
        (SELECT score FROM spam_score);
    '''

    cr.execute(query, words_list)
    ham_score, spam_score = cr.fetchone()
    db.close()

    print(time.perf_counter()-t1)
    print(ham_score, spam_score)
    print('ham' if (ham_score > spam_score)else 'spam')


if __name__=='__main__':
    main()