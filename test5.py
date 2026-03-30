from math import log, pow
import time
from multiprocessing import Process, Queue
import sqlite3
from global_variables import All  

MESSAGE = All.MESSAGE
APP = All.APP

def main():
    t1 = time.perf_counter()

    q_ham = Queue()
    q_spam = Queue()
    q_mess = Queue()

    ham_data = Process(target=read_ham, args=(q_ham,))
    spam_data = Process(target=read_spam, args=(q_spam,))

    ham_data.start()
    spam_data.start()

    message = Process(target=procc_mess, args=(q_mess,))
    message.start()

    mess = q_mess.get()
    spam = q_spam.get()
    ham = q_ham.get()
    
    ham_data.join()
    spam_data.join()
    message.join()
    
    q_score_spam = Queue()
    q_score_ham = Queue()

    print(time.perf_counter()-t1)
    proc_spam = Process(target=spam_mess, args=(spam['dict'], spam['prior_ham'], spam['prior_spam'], mess['dict'], q_score_spam))
    proc_ham = Process(target=ham_mess, args=(ham['dict'], ham['prior_ham'], ham['prior_spam'], mess['dict'], q_score_ham))
    
    proc_spam.start()
    proc_ham.start()

    proc_spam.join()
    proc_ham.join()

    score_spam = q_score_spam.get()
    score_ham = q_score_ham.get()

    if score_ham['ham_score'] > score_spam['spam_score']:
        print('ham score: ', score_ham['ham_score'])
        print('spam score: ', score_spam['spam_score'])
        print(f'The mail is ham')
    else:
        print('ham score: ', score_ham['ham_score'])
        print('spam score: ', score_spam['spam_score'])
        print(f'The mail is spam')



def procc_mess(queue):
    dic = {}
    for i in MESSAGE.upper().split():
        if i in dic: dic[i] = dic[i] + 1
        else: dic[i] = 1
    queue.put({'dict':dic})
    
def ham_mess(dic:dict, prior_ham:int, prior_spam:int, dic_mess:dict, queue):
    score = log(prior_ham / (prior_ham + prior_spam))
    for key, value in dic_mess.items():
        if key in dic: score = score + log(pow(dic[key],value))
        else: score = score + log(1/(1+prior_ham))
    queue.put({'ham_score':score})

def spam_mess(dic:dict, prior_ham:int, prior_spam:int, dic_mess:dict, queue):
    score = log(prior_spam / (prior_ham + prior_spam))
    for key, value in dic_mess.items():
        if key in dic:score = score + log(pow(dic[key],value))
        else: score = score + log(1/(1+prior_spam))
    queue.put({'spam_score':score})


def read_spam(queue):
    dic = {}
    db = sqlite3.connect(APP)
    cr = db.cursor()
    cr.execute('SELECT * FROM main')
    x = cr.fetchall()

    cr.execute('SELECT * FROM spam')
    for data in cr.fetchall():
        dic[data[0]] = data[1]

    db.close()
    queue.put({'dict':dic,'prior_ham':x[0][0], 'prior_spam':x[0][1]})
        

def read_ham(queue):
    dic = {}
    db = sqlite3.connect(APP)
    cr = db.cursor()
    cr.execute('SELECT * FROM main')
    x = cr.fetchall()

    cr.execute('SELECT * FROM ham')
    for data in cr.fetchall():
        dic[data[0]] = data[1]

    db.close()
    queue.put({'dict':dic,'prior_ham':x[0][0], 'prior_spam':x[0][1]})

if __name__=='__main__':
    main()