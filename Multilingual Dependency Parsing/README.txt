Name: Sania Arif
Uni: sa3311

ANSWERS:

Question 1

1.a. Visualized gold dependency graphs of a sentence are present in the root folder as files as follows:
English: figure_en.png
Danish:  figure_da.png
Korean:  figure_ko.png
Sewdish: figure_sw.png

1.b. A projective dependency graph is one that does not have any crossing arcs (arcs that cross each other). On observing the graph, if there are over-lapping edges that cross over one another, the graph is not projective. If there are no overlapping or criss-crossing edges, the graph is projective.
The algorithm to check for projectivity in providedcode/transitionparser.py iterates over all arcs, and for each arc checks if the arc is from i to j. If such an arc exists, there should be a directed path (using one or more hops) to go from i to every word between i and j.

1.c. Projective Sentence: The batsman hit the ball with the bat
   Non-Projective Sentence: I carried the dress gracefully that was stitched by my grandmother.
   This sentence is non-projective since there is a dependency between "carried" and "gracefully" that is crossed by the arc between "dress" and "was".

************
Question 2

2.a. Implemented the operations left_arc, shift and reduce that are used by the Nivre dependency parser.

2.b. The parser I implemented gave the following result on running it over badfeatures.model:

UAS: 0.279305354559 
LAS: 0.178726483357

This parser has a labeled accuracy score of 17.87%, which is extremely poor.

***********
Question 3

3.a. Features to improve the accuracy of the feature extractor:

I used a number of features listed in table 3.2 in the Dependency Parsing Book by Kubler, McDonald, and Nivre, I added 2 more features that were mentioned in the succeeding paragraph. Here are the features and the change in performance for the Swedish data, measured after adding each feature:

Initial Performance:
(with STK[0]: FORM, FEATS; BUF[0]: FORM, FEATS; ldep(STK[0]); rdep(STK[0]); ldep(BUF[0]); rdep(BUF[0]))

UAS: 0.367583212735 
LAS: 0.264109985528

1. STK[0]: LEMMA, POSTAG:

Performance: By simply adding a feature to check for the LEMMA (in other words, the stem of the word), and the POSTAG (fine-grained part of speech tag) for the token present at STK[0], the labelled accuracy score rose to almost double. 

UAS: 0.575253256151 
LAS: 0.435600578871

Implementation: In the implementation, I check to see if the lemma and the postag of a token are informative (i.e. not '_'), and if that is the case, tag them appropriately.

Complexity: This takes constant time per token, thus, for N tokens will take O(N) time.

2. STK[0]: Number of left children and right children <*Extra, not in table*>

I added this feature since it would make sense for a token with multiple children (dependent tokens) to be higher up in the dependency parse tree.

Performance: By adding a feature that counts the number of left and right children of the token at STK[0], the accuracy scores increased as follows:

UAS: 0.592619392185 
LAS: 0.475397973951

Implementation: In the implementation, I iterate through all the arcs and keep a count of the arcs where the first value in the tuple of 3 is the token present at STK[0]. 

Complexity: Iterating through all arcs gives a time complexity of the order of O(N).

3. STK[1]: POSTAG <<Reduced accuracy therefore removed feature>>

Here, I checked for the POSTAG of the token present at STK[1] to see if it was informative. However, this reduced the accuracy of the parser and thus I left it out. The results after adding this feature are as follows:

UAS: 0.559334298119 
LAS: 0.442112879884

4. BUF[0]: LEMMA, POSTAG

Performance: By simply adding a feature to check for the LEMMA (in other words, the stem of the word), and the POSTAG (fine-grained part of speech tag) for the token present at BUF[0], the labelled accuracy score rose as follows:

UAS: 0.751085383502 
LAS: 0.65991316932

Implementation: In the implementation, I check to see if the lemma and the postag of a token are informative (i.e. not '_'), and if that is the case, tag them appropriately.

Complexity: This takes constant time per token, thus, for N tokens will take O(N) time.

5. BUF[1]: FORM, POSTAG

Performance: By simply adding a feature to check for the FORM (i.e. word or punctuation), and the POSTAG (fine-grained part of speech tag) for the token present at BUF[1], the labelled accuracy score rose as follows:

UAS: 0.803183791606 
LAS: 0.708393632417

Implementation: In the implementation, I check to see if the form and the postag of a token are informative (i.e. not '_'), and if that is the case, tag them appropriately.

Complexity: This takes constant time per token, thus, for N tokens will take O(N) time.

6. Adding BUF[2]: POSTAG

Performance: By simply adding a feature to check for the POSTAG (fine-grained part of speech tag) for the token present at BUF[2], the labelled accuracy score rose as follows:

UAS: 0.816208393632 
LAS: 0.72503617945 

Implementation: In the implementation, I check to see if the form of a token is informative (i.e. not '_'), and if that is the case, tag them appropriately.

Complexity: This takes constant time per token, thus, for N tokens will take O(N) time.

7. BUF[3]: POSTAG <<Reduced accuracy therefore removed feature>>

Here, I checked for the POSTAG of the token present at BUF[1] to see if it was informative. However, this reduced the accuracy of the parser and thus I left it out. The results after adding this feature are as follows:

UAS: 0.801013024602 
LAS: 0.706946454414

8. BUF[0]: Number of left children and right children <*Extra, not in table*> <<Reduced accuracy therefore removed feature>>

I added this feature since it would make sense for a token with multiple children (dependent tokens) to be higher up in the dependency parse tree. However, by adding a feature that counts the number of left and right children of the token at BUF[0], the accuracy scores decreased and thus I chose to leave out this feature. The accuracy decreased as follows:

UAS: 0.813314037627 
LAS: 0.723589001447

9. Counting the distance (number of words) between STK[0] and BUF[0] <*Extra, not in table*>

I added this feature as if 2 words are very far away from each other, they are not likely to be related.

Performance: I calculated the distance between the token on top of the stack and the first token in the input buffer. The accuracy results are as follows:

UAS: 0.814037626628 
LAS: 0.72503617945

Implementation: I simply calculated the absolute value of the difference in address of STK[0] and BUF[0].

Complexity: It takes constant time.

10. Counting the number of verbs between STK[0] and BUF[0] <*Extra, not in table*>

I added this feature, as if more verbs exist between 2 words, the more far apart they are, and they are most likely to be related to the intermittent verbs as opposed to each other.

Performance: By adding this feature, the performance improved by ~1%. The scores are as follows:

UAS: 0.81476121563 
LAS: 0.726483357453

Implementation: I iterate through all the tokens that exist between STK[0] and BUF[0] and if they are tagged as 'VERB', I increment the counter.

Complexity: The complexity of this is O(N) in the worst case.

3.b. Generated trained models for English, Danish and Swedish as follows:

	English: english.model
	Danish: danish.model
	Swedish: swedish.model

3.c. Results obtained after scoring models against test data:

Swedish:

	UAS: 0.81476121563 
	LAS: 0.726483357453

English:

	UAS: 0.788753056235 
	LAS: 0.758435207824

Danish:

	UAS: 0.796507723304 
	LAS: 0.70920080591

3.d. Complexity of the arc-eager shift-reduce parser:

	The time complexity of the arc-eager shift-reduce parser largely depends upon the SVM that is given to us as a black box. The feature extraction, however, takes time of the order of O(N^2), where N is the number of tokens. This is because, for each of the N tokens, we apply all of the features, out of which the feature that counts the number of left and right children as well as the feature that counts the number of verbs between STK[0] and BUF[0] can take upto O(N) time. 
															
	Parsing a sentence is of the order of space complexity O(N), because the buffer is of a fixed lenth = N, which is the length of the sentence and the buffer size keeps decreasing. Thus, parsing takes a single pass. In the worst case, however, there may be a dependency arc between all tokens, thus the upper bound on space complexity is O(N^2)

Tradeoffs:

-An advantage of the parser is that machine learning technique (that we treated as a black box) can be replaced by any other technique, for a specific application.

-A disadvantage of the parser is that it cannot parse non-projective sentences.

***********
Question 4

4.a. Created a file "parse.py" that can be called like this:
cat englishfile | python parse.py english.model > englishfile.conll

4.b. Program is present in parse.py that takes standard input as sentences to be parsed and the output is in CoNLL-format.

4.c. The CoNLL output is valid and contains a projective dependency graph for each sentence. It is present as "englishfile.conll".
