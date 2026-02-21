from os import walk
from math import log

ACCURACY = 10
path_ham = '/home/mhy/Documents/py/probability/Bayes/tsoding_filter_spam/data/train/ham'
path_spam = '/home/mhy/Documents/py/probability/Bayes/tsoding_filter_spam/data/train/spam'
HAM = 0
SPAM = 0
MESSAGE = '''
Subject: she will love you for this !
worlds first dermal p ; atch technology for p * nis enlarg ; ment
a ; dd 3 + in ; ches today - loo % doc ; tor approved
the viriiity p ; atch r . x . was designed _ for men like yourself who want a b ; lgger , th ; icker , m ; ore en ; ergetic p * nis ! imagine sky _ rocketing in size 2 ' ' , 3 ' ' , even 4 ' ' in 60 _ days or l ; ess . but that ' s not _ all . viriiity p ; atch r . x .
will also super _ charge your s * xual battery effort ; lessly 24 / 7 . your libido and energy level will soar , and you will sat ; isfy your lov ; er like never _ before ! loo % p ; roven to _ work or your m ; oney bac ; k !
to _ be r 3 mov 3 d from our listr ; ight here .
i will not bribe principal skinneri will not bribe principal skinnerblhj 218 dc 8 j 92 dqfvn 5 v
3311 a 32 bggu 2 mkl 746 augs 2 wznr 303 sb 9 pqn 2 yc 55 qcci will not bribe principal skinner 5 a 6 dx 2 tvvqu 62 rs 8 o 2 b 4 brk
45 x 5 ql 6 ools 9 z 99 mud is not one of the 4 food groupshj 218 dc 8 j 92 dqfvn 5 v 3311 a 32 bggu
2 mkl 746 aui will not bribe principal skinnergs 2 wznr 303 sb 9 pqn 2 yc 55 qcc 5 a 6 dx 2 t
vvqu 62 rs 8 o 5 i 730 mud is not one of the 4 food groupshjplp 875 a 331 d 932 gmltlk 331
k 6 zz 29 c 74 emq 302 qa 8 op 4 mei 4 my 70 ff 6 cdlmud is not one of the 4 food groups
zbtpa 61 wx 75 b 99778903 i will not bribe principal skinner
5 d 4 vo 5 no 0 y 9 f 99 mifovuh 30 hjplp 8 mud is not one of the 4 food groups i will not bribe principal skinner
'''


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
    x = [['', 0]]
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
                score = score + log(j[1])
                found = True
                break
        if not found:
            score = score + log(1/(HAM + 1))
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
                score = score + log(j[1])
                found = True
                break
        if not found:
            score = score + log(1/(SPAM + 1))
    return score


def main():
    ham = inits(path_ham, 'HAM')
    P_ham = prob(ham, HAM)
    spam = inits(path_spam, 'SPAM')
    P_spam = prob(spam, SPAM)
    print(f"Total HAM words: {HAM}")
    print(f"Total SPAM words: {SPAM}")
    mes_ham = normal_message(message=MESSAGE, P_ham=P_ham)
    print(mes_ham)
    mes_spam = spam_message(message=MESSAGE, P_spam=P_spam)
    print(mes_spam)
    if mes_ham>mes_spam:print('ham')
    else:print('spam')

if __name__=='__main__':
    main()
