# Naive Bayes Classifier(Email Spam Filter)

In this project I wrote multiple programs to make Naive Bayes Classifier
to filter email for probability class in my university.

START by first change the "path_ham" and "path_spam" to the files dataset
so the program read them and change the global variable MESSAGE 
this is the message you want to test.

I already give you in ./tsoding_filter_spam/data/train/
the dataset to train on it from TSODING.

https://www.youtube.com/watch?v=JsfOXk7qmSM

I start dead simple program test.py without any optimzing and with the most
bad code you could ever imagen then one by one. 
I make it better in test2.py by using dict instead of list which make it FAST AS .

The jump in preformence from test1 to test2 the program read 
in test1 6000 file twice around (42000 thousnd words in dataset).
in test2 6000 file twice around (1.5 milion words in dataset). 
test1 took 445 second. cpython=> 187 second. pypy
test2 took 0.782 second. cpython=> 11 second. I think the reason for that the way I wrote code. pypy

"""
texts = texts + y
"""

In test3 I use MultiProcess to process the ham and spam seprately 
thats result in preformence jump from 0.8 to 0.5 second around 37.6%
preformence gain.

I taked a step back I use the "pypy" python intepreter 
but it does not like MultiProcess so I could try more 
with it but I don't have time and I want to use 
c-extension libraries and I doesn't work will with it.
c-extension like pandas and NumPy.
Cpython optimize it, but pypy make new copy of the variable which slow the program by 100 magnitude
as shown in the block:

In test5 I use preprocessed data in "HAM_SPAM_TEST.db"
and read the whole train data so don't focous on the 
time focous on the percent of the improvement.
