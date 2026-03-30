from os import walk
from math import log
import time
from global_variables import All  

from pathlib import Path
ACCURACY = All.ACCURACY
path_ham = All.path_ham
path_spam = All.path_spam
HAM = All.HAM
SPAM = All.SPAM
MESSAGE = All.MESSAGE

def list_histogram(lst: list, label=''):
    y = [['', 1]]
    for i in lst:
        if label=='HAM':
            global HAM
            HAM = HAM + 1
        else: 
            global SPAM
            SPAM = SPAM + 1
        for j in y:
            if i == j[0]:
                j[1] = j[1] + 1
                break
        else: 
            y.append([i, 1])
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

def prob(lst: list, label: int):
    x = [['', 1]]
    for i in lst:
        x.append([i[0],i[1]/label])
    return x        

def normal_message(message: str, P_ham: list):
    y = [['', 1]]
    P_normal = log(ACCURACY/(ACCURACY+ACCURACY))
    score = 0 + P_normal
    mes = message.upper().split()
    for i in mes:
        found = False
        for j in P_ham:
            if i==j[0] and not j[1]==0:
                found = True
                score = score + log(j[1])
        if not found:
            score = score + log(1/(HAM+1))
    return score

def spam_message(message: str, P_spam: list):
    y = [['', 1]]
    P_normal = log(ACCURACY/(ACCURACY+ACCURACY))
    score = 0 + P_normal
    mes = message.upper().split()
    for i in mes:
        found = False
        for j in P_spam:
            if i==j[0] and not j[1]==0:
                found = True
                score = score + log(j[1])
        if not found:
            score = score + log(1/(SPAM+1))
    return score


def main():
    x = time.perf_counter()

    ham = inits(path_ham, 'HAM')
    P_ham = prob(ham, HAM)

    spam = inits(path_spam, 'SPAM')
    P_spam = prob(spam, SPAM)
    
    mes_ham = normal_message(message=MESSAGE, P_ham=P_ham)
    print(mes_ham)

    mes_spam = spam_message(message=MESSAGE, P_spam=P_spam)
    print(mes_spam)

    place = ''
    if mes_ham>mes_spam:place = 'ham'
    else:place = 'spam'
    print(f' ham score is {mes_ham} \n spam score is {mes_spam} \nThe Mail is {place}')

    print(time.perf_counter()-x,'Seconds')
if __name__=='__main__':
    main()