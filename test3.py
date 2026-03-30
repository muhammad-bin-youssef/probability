from os import walk
from math import log
import time
from multiprocessing import Process, Queue
from global_variables import All  

ACCURACY = All.ACCURACY
path_ham = All.path_ham
path_spam = All.path_spam
HAM = All.HAM
SPAM = All.SPAM
MESSAGE = All.MESSAGE

def list_histogram(lst: list, label=''):
    y = {}
    counter = 0
    for i in lst:
        if i in y: y[i] = y[i] + 1
        else: y[i] = 1
        counter += 1
        if label=='HAM':
            global HAM
            HAM = counter
        else:
            global SPAM
            SPAM = counter
    return y    

def read_file(path: str):
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError as err:
        ...
    except FileExistsError as err:
        ...
    except UnicodeDecodeError as err:
        ...

def inits(path, label=''):
    texts = ''
    for _, _, files in walk(path):
        for i in range(0, ACCURACY):
            file = files[i]
            y = str(read_file(str(path+'/'+file)))
            texts = texts + y
        break
    text = texts.upper().split()
    return list_histogram(text, label)

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
    spam = inits(path_spam, 'SPAM')
    P_spam = prob(spam, SPAM)
    mes_spam = spam_message(message=MESSAGE, P_spam=P_spam)
    q.put({'spam' : mes_spam})

def process_ham(q):
    ham = inits(path_ham, 'HAM')
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
        if res1['ham']>res2['spam']:
            print(f'ham score is {res1['ham']}\n spam score is {res2['spam']} \nThe Mail is ham')
        else:
            print(f'ham score is {res1['ham']}\n spam score is {res2['spam']} \nThe Mail is ham')

    except KeyError as err:
        if res1['spam']<res2['ham']:
            print(f'spam score is {res1['spam']} \nham score is {res2['ham']} \nThe Mail is ham')
        else:
            print(f'spam score is {res1['spam']} \nham score is {res2['ham']} \nThe Mail is spam')

    print(time.perf_counter()-time1, 'Second')

if __name__=='__main__':
    main()