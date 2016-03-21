import re,collections

def wordsToSmall(text): 

	return re.findall('[a-z]+', text.lower()) 
def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

def NWORDS():
	return train(wordsToSmall(file('big.txt').read()))
