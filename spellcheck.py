import re
import collections 


def words(text):
	return re.findall('[a-z]+',text.lower())

def train(features):
	# lambda:1 is done for smoothing
	model = collections.defaultdict(lambda:1) 
	for f in features:
		model[f]+=1
	return model

nwords = train(words(a))
# print nwords['hello']
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)
def edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))
print list(edits2("hello"))	[0:10]