# Naive Bayes Classifier(Email Spam Filter)

In this project I wrote multiple programs to make Naive Bayes Classifier
to filter email for probability class in my university.

START by first change the "path_ham" and "path_spam" to the files dataset
so the program read them and change the global variable MESSAGE 
this is the message you want to test.

I already give you in ./tsoding_filter_spam/data/train/
the dataset to train on it from TSODING.

https://www.youtube.com/watch?v=JsfOXk7qmSM

I start dead simple program test1.py without any optimes and with the most
bad code you could ever imagen then one by one I make it better in 
test2.py by using dict instead of list which make it FAST AS .

The jump in preformence from test1 to test2 the program read 
in test1 200 file twice around (42000 thousnd words in dataset) 
in test2 6000 file twice around (1.5 milion words in dataset). 
test1 took 3.5609239149998757 second
test2 took 0.782906192000155 second.

In test3 I use MultiProcess to process the ham and spam seprately 
thats result in preformence jump from 0.8 to 0.5 second around 37.6%
preformence gain.
