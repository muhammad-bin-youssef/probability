import time
import os
from multiprocessing import Process, Queue
import sqlite3

APP = 'HAM_SPAM_TEST.db'
PATH_HAM = r'/home/mhy/Documents/py/probability/Bayes/tsoding_filter_spam/data/train/ham'
HAM_COUNTER_FILES = 0
PATH_SPAM = r'/home/mhy/Documents/py/probability/Bayes/tsoding_filter_spam/data/train/spam'
SPAM_COUNTER_FILES = 0


def main():#FINISHED
    if os.path.isfile(APP):
        print(f'File {APP} already exists')
        return 0

    q_ham = Queue()
    q_spam = Queue()

    for _, _, file1 in os.walk(PATH_HAM):
        global HAM_COUNTER_FILES
        HAM_COUNTER_FILES = len(file1)
        break

    for _, _, file2 in os.walk(PATH_SPAM):
        global SPAM_COUNTER_FILES
        SPAM_COUNTER_FILES = len(file2)
        break

    proc_ham = Process(target=main_ham,args=(HAM_COUNTER_FILES,SPAM_COUNTER_FILES, q_ham))
    proc_spam = Process(target=main_spam, args=(HAM_COUNTER_FILES,SPAM_COUNTER_FILES, q_spam))

    proc_ham.start()
    proc_spam.start()

    spam = q_spam.get()
    ham = q_ham.get()

    proc_ham.join()
    proc_spam.join()
    
    write_data(spam=spam['dict'], ham=ham['dict'], prior_ham=ham['prior'],
               prior_spam=spam['prior'], words_ham=ham['words'],
               words_spam=spam['words'])
        

def init_data(lst: list):
    place_holder = {}
    words = len(lst)

    for element in lst:
        if element in place_holder.keys():
            place_holder[element] = place_holder[element] + 1
        else:
            place_holder[element] = 1
    
    for key, value in place_holder.items():
        place_holder[key] = value/words
    
    return place_holder, words
         
         
def write_data(ham:dict, spam:dict, prior_ham:float, prior_spam:float,
               words_ham:int, words_spam:int):
    db = sqlite3.connect(APP) 
    cr = db.cursor()

    db.execute(f'CREATE TABLE if not exists main (Prior_ham INT DEFAULT {words_ham},Prior_spam INT DEFAULT {words_spam})')
    try:
        cr.execute(r'INSERT INTO main(prior_ham, prior_spam) VALUES(?, ?)',(words_ham, words_spam))
        db.commit()
    except Exception as err:print(err)
    db.execute('CREATE TABLE if not exists ham (name TEXT PRIMARY KEY, probability DECIMAL)')
    db.execute('CREATE TABLE if not exists spam (name TEXT PRIMARY KEY, probability DECIMAL)')

    for key, value in ham.items():
        try:
            cr.execute(r'INSERT INTO ham(name, probability) VALUES(?, ?)',(key, value))
        except Exception as err: print(err)
    db.commit()

    for key, value in spam.items():
        try:
            cr.execute(r'INSERT INTO spam(name, probability) VALUES(?, ?)',(key, value))
        except Exception as err: print(err)
        
    
    db.commit()
    db.close()

def main_ham(HAM_COUNTER_FILES, SPAM_COUNTER_FILES, q_ham):
    ham_dict = read_files(PATH_HAM)
    prior_ham = HAM_COUNTER_FILES / (HAM_COUNTER_FILES + SPAM_COUNTER_FILES)
    y, words = init_data(ham_dict)
    x = {'dict': y, 'prior':prior_ham, 'words': words} 
    q_ham.put(x)

    

def main_spam(HAM_COUNTER_FILES, SPAM_COUNTER_FILES, q_spam):
    dict_spam = read_files(PATH_SPAM)
    prior_spam = SPAM_COUNTER_FILES / (HAM_COUNTER_FILES + SPAM_COUNTER_FILES)
    y, words = init_data(dict_spam)
    x = {'dict': y, 'prior':prior_spam, 'words': words} 
    q_spam.put(x)

def read_files(path):
    file_texts = ''
    try:
        for _, _, files in os.walk(path):
                for file in files:
                    with open(os.path.join(path, file), 'r', encoding='utf-8',errors='ignore') as f: #,errors='ignore'
                        file_texts = file_texts + f.read()
                break
    except Exception as err:
        print(err)
        
    return file_texts.upper().split()





if __name__=='__main__':
    time1 = time.perf_counter()
    main()
    print(time.perf_counter()-time1, 'seconds')