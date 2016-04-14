Name: Sania Arif	Uni: sa3311
Homework 1:
A1:
UNIGRAM near -12.4560686964
BIGRAM near the -1.56187888761
TRIGRAM near the ecliptic -5.39231742278

A2:
Uni: The perplexity is 1052.4865859
Bi: The perplexity is 53.8984761198
Tri: The perplexity is 5.7106793082

A3:
The perplexity is 12.5516094886

A4:
The perplexity of the trigram model without interpolation has a value lesser than the model with linear interpolation, this is because the odel with linear interpolation gives an equal weight to unigram, bigram and trigram models, which causes it to perform worse than the pure trigram model.
Similarly, the performance of the model with linear interpolation is much better than the unigram and bigram models, since it gives equal weight to the unigram, bigram and trigram as opposed to purely unigram and purely bigram which perform much worse.

A5:
Sample1_scored: The perplexity is 11.1670289158
Sample2_scored: The perplexity is 1611316939.17
Thus, Sample1 contains sentences from the Brown dataset, since the perplexity value for this sample is much less compared to Sample2, which means Sample2 contains of sentences that the model has never seen before, and is very perplexed about it, as opposed to Sample1, which are seen and have a low perplexity value.

B2:
Trigram CONJ ADV NOUN -4.46650366731
Trigram DET NUM NOUN -0.713200128516
Trigram NOUN PRT CONJ -6.38503274104

B4:
Emission * * 0.0
Emission midnight NOUN -13.1814628813
Emission Place VERB -15.4538814891

B5:
Percent correct tags: 93.3226493638

B6:
Percent correct tags: 91.3944534563 (without unigram tagger and with changes to zip)
Percent correct tags: 87.9985146677 (without unigram tagger)
Percent correct tags: 94.2498094475 (with unigram tagger)

