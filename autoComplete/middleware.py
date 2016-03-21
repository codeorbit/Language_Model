import retrievalMain as rm
import probability as p

def autoMain(x):
	
	s = x.strip().split(" ",3)

	if len(s)>3:

		pw ,rel = rm.fourthWord(s[0],s[1],s[2],s[3])
		probable_word_list = p.probabilityFourthWord(pw)
		return probable_word_list,rel

	if len(s)==3:

		fc,sc,rft,rst,pw,rel = rm.thirdWord(s[0],s[1],s[2])
		probable_word_list =  p.probabilityThirdWord(fc,sc,rft,rst,pw)
		return probable_word_list,rel

	if len(s)==2:

		pw ,fwcount,rel=rm.secondWord(s[0],s[1])
		probable_word_list = p.probabilitySecondWord(s[0],s[1],pw,fwcount)
		return probable_word_list,rel

	if len(s)==1 :

		probable_words ,rel = rm.firstWord(s[0])		
		probable_word_list = p.probabilityFirstWord(s[0],probable_words)
		return probable_word_list,rel
