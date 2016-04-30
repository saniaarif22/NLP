Name: Sania Arif
Uni: sa3311

Part A:

Running Time: 167 secs

Q3.

Using 10 iterations of EM, output for IBM Models 1 and 2 is:

IBM Model 1
---------------------------
Average AER: 0.665

IBM Model 2
---------------------------
Average AER: 0.650

Time taken by part A: 167 secs


Sentence pair:
1. ( Das Parlament erhebt sich zu einer Schweigeminute . )
2. ( The House rose and observed a minute ' s silence )

Output for IBMModel1:

[u'(', u'Das', u'Parlament', u'erhebt', u'sich', u'zu', u'einer', u'Schweigeminute', u'.', u')']
[u'(', u'The', u'House', u'rose', u'and', u'observed', u'a', u'minute', u"'", u's', u'silence', u')']
0-11 1-5 2-5 3-5 4-10 5-10 6-10 7-10 9-11

AER = 0.75

Output for IBMModel2:

[u'(', u'Das', u'Parlament', u'erhebt', u'sich', u'zu', u'einer', u'Schweigeminute', u'.', u')']
[u'(', u'The', u'House', u'rose', u'and', u'observed', u'a', u'minute', u"'", u's', u'silence', u')']
0-0 1-5 2-3 3-5 4-10 5-9 6-10 7-7 9-11

AER = 0.666666666667

Performance of the models:

The difference between the two models is that IBM Model 1 sets all alignment parameters to be 1/(l+1)^m while IBM Model 2 introduces and calculates alignment probabilities which leads to higher accuracy in this sentence example.

****************************************************************************************************

Q4.

The results obtained for different iterations are:

1

IBM Model 1
---------------------------
Average AER: 0.873

IBM Model 2
---------------------------
Average AER: 0.646

2

IBM Model 1
---------------------------
Average AER: 0.684

IBM Model 2
---------------------------
Average AER: 0.644

3

IBM Model 1
---------------------------
Average AER: 0.641

IBM Model 2
---------------------------
Average AER: 0.644

4

IBM Model 1
---------------------------
Average AER: 0.630

IBM Model 2
---------------------------
Average AER: 0.642

5

IBM Model 1
---------------------------
Average AER: 0.627

IBM Model 2
---------------------------
Average AER: 0.644

6

IBM Model 1
---------------------------
Average AER: 0.626

IBM Model 2
---------------------------
Average AER: 0.647

7

IBM Model 1
---------------------------
Average AER: 0.629

IBM Model 2
---------------------------
Average AER: 0.646

8

IBM Model 1
---------------------------
Average AER: 0.631

IBM Model 2
---------------------------
Average AER: 0.649

9

IBM Model 1
---------------------------
Average AER: 0.628

IBM Model 2
---------------------------
Average AER: 0.649

10

IBM Model 1
---------------------------
Average AER: 0.665

IBM Model 2
---------------------------
Average AER: 0.650

11

IBM Model 1
---------------------------
Average AER: 0.666

IBM Model 2
---------------------------
Average AER: 0.649

12

IBM Model 1
---------------------------
Average AER: 0.666

IBM Model 2
---------------------------
Average AER: 0.650

13

IBM Model 1
---------------------------
Average AER: 0.666

IBM Model 2
---------------------------
Average AER: 0.652

14

IBM Model 1
---------------------------
Average AER: 0.665

IBM Model 2
---------------------------
Average AER: 0.652

15

IBM Model 1
---------------------------
Average AER: 0.665

IBM Model 2
---------------------------
Average AER: 0.650

16

IBM Model 1
---------------------------
Average AER: 0.665

IBM Model 2
---------------------------
Average AER: 0.650

17

IBM Model 1
---------------------------
Average AER: 0.662

IBM Model 2
---------------------------
Average AER: 0.651

18

IBM Model 1
---------------------------
Average AER: 0.661

IBM Model 2
---------------------------
Average AER: 0.651

19

IBM Model 1
---------------------------
Average AER: 0.661

IBM Model 2
---------------------------
Average AER: 0.649

20

IBM Model 1
---------------------------
Average AER: 0.66

IBM Model 2
---------------------------
Average AER: 0.648

40

IBM Model 1
---------------------------
Average AER: 0.658

IBM Model 2
---------------------------
Average AER: 0.65

60

IBM Model 1
---------------------------
Average AER: 0.66

IBM Model 2
---------------------------
Average AER: 0.657

80

IBM Model 1
---------------------------
Average AER: 0.661

IBM Model 2
---------------------------
Average AER: 0.657

Thus,

The lower bound on the AER for IBMModel1 is achieved at:

Number of iterations = 6
AER = 0.626

The lower bound on the AER for IBMModel2 is achieved at:

Number of iterations = 4
AER = 0.642


Relation between number of iterations and AER:

When the number of iterations is small, the AER changes with the change of the number of itertions. The lower
bound for IBMmodel1 and IBMmodel2 may be reached because:

1. The AER is calculated over only a tiny subset of all of the sentences
2. The parameters did not converge

As the number of iterations increases, the AER of the models should converge. As seen in my results above, the AER  sort-of converges as such: 

number of iterations >= 18, the AER of IBMmodel1 seems to reach convergence at around 0.66 
number of iterations >= 60, the AER of IBMmodel2 seems to reach convergence at 0.657


****************************************************************************************************


Part B

Running Time: 373 sec

Q4


The output for average AER for the first 50 sentences is :

Berkeley Aligner
---------------------------
Average AER: 0.543 

Tome taken by part B: 373 secs

The average AER for IBM Models 1 and 2 were:
IBMModel 1 : 0.665
IBMModel 2 : 0.650

Thus, we can see that the Berkeley Aligner has a much lesser error rate as compared to IBM Models 1 and 2.


Q5


Sentence pair:
1. ( Ich bitte Sie , sich zu einer Schweigeminute zu erheben .  )
2. ( Please rise , then , for this minute ' s silence .  )

Output for IBMModel1:

0-1 1-1 2-1 3-4 4-10 5-10 6-10 7-10 8-10 9-1

AER = 0.75

Output for IBMModel2:

0-0 1-1 2-0 3-2 4-10 5-10 6-10 7-7 8-10 9-0

AER = 0.666666666667

Output for Berkeley Aligner: 

0-0 1-1 2-0 3-2 4-6 5-10 6-10 7-7 8-10 9-0 10-11

AER = 0.6


Performance of the models:


Thus, we observe that, the Berkeley Aligner performs the best among the three models, with the lowest AER. The reason for this is the Berkeley Aligner considers the intersection of the prediction of the English to German and the German to English models (two directions) to reach the agreement. 
Additionally, the Berkeley Aligner makes predictions of the models agreement at test time, in addition to the agreement during training. The joint training of the two directional models, at opposite direction to give better performance.


