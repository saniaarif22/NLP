import sys
from providedcode.transitionparser import TransitionParser
from providedcode.evaluate import DependencyEvaluator
from providedcode.dependencygraph import DependencyGraph
from nltk.tag import mapping

if len(sys.argv) != 2:
	sys.stderr.write("No model provided.")
	sys.exit(1)

tp = TransitionParser.load(sys.argv[1])

for sentence in sys.stdin: 
    s = DependencyGraph.from_sentence(sentence) #class DependencyGraph, function from_sentence
    for node in s.nodes:
            tag = s.nodes[node]['tag']
            ctag = mapping.map_tag('wsj','universal',tag)
            s.nodes[node]['ctag'] = ctag
    x = tp.parse([s])
    print x[0].to_conll(10).encode('utf-8')

# model: sys.argv(1) - english.model
