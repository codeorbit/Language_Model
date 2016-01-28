import retrievalmain as rm
import probability as p
def autoMain(x):
	# x=raw_input("Enter the string : ")
	s = x.strip().split(" ",3)
	if len(s)>3:
		pw ,rel = rm.fourth_word(s[0],s[1],s[2],s[3])

		probable_word_list = p.probability_fourth_word(pw)
		return probable_word_list
	if len(s)==3:
		fc,sc,rft,rst,pw,rel = rm.third_word(s[0],s[1],s[2])
		# print "calling autocomplete"
		probable_word_list =  p.probability_third_word(fc,sc,rft,rst,pw)
		
		return probable_word_list

	if len(s)==2:
		pw ,fwcount,rel=rm.second_word(s[0],s[1])
	
		# print "calling autocomplete"
		probable_word_list = p.probability_second_word(s[0],s[1],pw,fwcount)
		
		return probable_word_list
	if len(s)==1 :
		probable_words = rm.first_word(s[0])
	
		#print "calling autocomplete"
		probable_word_list = p.probability_first_word(s[0],probable_words)

		return probable_word_list
