import os
from math import log
import time
from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor
import threading 

lock = threading.Lock()

ACCURACY = 6000
path_ham = '/home/mhy/Documents/py/probability/Bayes/tsoding_filter_spam/data/train/ham'
path_spam = '/home/mhy/Documents/py/probability/Bayes/tsoding_filter_spam/data/train/spam'
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


def list_histogram(lst: list, label=''):
    y = {}
    counter = 0
    for i in lst:
        if i in y: y[i] = y[i] + 1
        else: y[i] = 1
        counter += 1
        if label=='HAM':
            global HAM
            with lock:
                HAM = counter
        else:
            global SPAM
            with lock:
                SPAM = counter
    return y    


def read_file_thread(path: str):
    try:
        with open(path, 'r',errors='ignore', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return '' 

def inits_threads(path, label):
    all_text_list = []
    files_to_read = []
    for _, _, files in os.walk(path):
        for i in range(0, ACCURACY):
            files_to_read.append(os.path.join(path, files[i]))
        break
    with ThreadPoolExecutor(max_workers=100) as excuter:
        results = list(excuter.map(read_file_thread,files_to_read))
        full_content = ''.join(results).upper().split()
        return list_histogram(full_content, label=label)



def prob(dicts, sample: int):
    x = {}
    for key, value in dicts.items():
        x[key] = value/sample
    return x        

def normal_message(message: str, P_ham: dict):
    P_normal = log(ACCURACY/(ACCURACY+ACCURACY))
    score = 0 + P_normal
    mes = message.upper().split()
    for i in mes:
        if i in P_ham:score += log(P_ham[i])
        else:score += log(1/(HAM+1))
    return score
def spam_message(message: str, P_spam):
    P_normal = log(ACCURACY/(ACCURACY+ACCURACY))
    score = 0 + P_normal
    mes = message.upper().split()
    for i in mes:
        if i in P_spam:score += log(P_spam[i])
        else:score += log(1/(SPAM+1))
    return score

def process_spam(q):
    spam = inits_threads(path_spam, 'SPAM')
    P_spam = prob(spam, SPAM)
    mes_spam = spam_message(message=MESSAGE, P_spam=P_spam)
    q.put({'spam' : mes_spam})

def process_ham(q):
    ham = inits_threads(path_ham, 'HAM')
    P_ham = prob(ham, HAM)
    mes_ham = normal_message(message=MESSAGE, P_ham=P_ham)
    q.put({'ham' : mes_ham})

def main():
    time1 = time.perf_counter()

    q = Queue()

    p_ham = Process(target=process_ham, args=(q,))
    p_spam = Process(target=process_spam, args=(q,))

    p_ham.start()
    p_spam.start()

    res1 = q.get()
    res2 = q.get()

    p_ham.join()
    p_spam.join()

    try:
        if res1['ham']>res2['spam']:print(f'spam score is {res2['spam']} \nham score is {res1['ham']} \nThe Mail is ham')
        else:print(f'spam score is {res2['spam']}\nham score is {res1['ham']}\nThe Mail is spam')

    except KeyError as err:
        if res1['spam']<res2['ham']:print(f'spam score is {res1['spam']} \nham score is {res2['ham']} \nThe Mail is ham')
        else:print(f'spam score is {res1['spam']} \nham score is {res2['ham']} \nThe Mail is spam')

    print(time.perf_counter()-time1, 'Second')

if __name__=='__main__':
    main()