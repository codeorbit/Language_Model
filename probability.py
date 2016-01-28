from __future__ import division
from collections import Counter
#import models
import operator # for sorted function
import math 
import retrievalmain as rm
from collections import OrderedDict
FINAL_WORDS_order_dic = OrderedDict()

FINAL_WORDS={}



def probability_first_word(word,probable_words,top_n=10):
	
	total=0
	for i in probable_words.values():
		total+=(i)
	# print total
	try:
		for k , v in probable_words.items():
			if k.startswith(word):
				v= int(v)
				score=v/total
				FINAL_WORDS.update({k:score})
		
		return (sorted(FINAL_WORDS.items(),key=operator.itemgetter(1),reverse=True)[:top_n])		
		
	except Exception as e:
		# print e
		pass

	

def probability_second_word(first_word,second_word,pw,fwcount,top_n=10):
	
	# print pw
	# print fwcount	

	
 	global FINAL_WORDS 
 	FINAL_WORDS = {}

	for p_word,count in pw.items():
								 
		score_num=count[0]
		score_den=fwcount
		score=score_num/score_den
		FINAL_WORDS.update({p_word:score})					
	return Counter(FINAL_WORDS).most_common(top_n)


def probability_third_word(fc,sc,rft,rst,pw,top_n=5):
	# print fc
	# print sc
	# print rft
	# print rst
	# print pw
	global FINAL_WORDS 
	FINAL_WORDS = {}
	total=0
	for i in pw.values():
		total+=(i)
	#print total
	total_rst=0
	for i in rst.values():
		total_rst+=(i[0])
	#print total_rst
	total_rft=0
	for i in rft.values():
		total_rft+=(i[0])
	#print total_rft

	for p_word, count in pw.items():
		score = count/total
		# print score
		if p_word in rft.keys():
			score_rft = rft[p_word][0]+rft[p_word][1]/total_rft       # adding score and selfcount and then dividing by total rel will 
			# print score_rft                                           # solve the problem of conflict of nodes having same score
			score = score +score_rft                                  # i.e the probability of occurence of word after first word 
		if p_word in rst.keys():
			score_rst = rst[p_word][0]+rst[p_word][1]/total_rst
			# print score_rst
			score = score+score_rst
		FINAL_WORDS.update({p_word:(score)})
		#print "******************************"
	# print "------------------"
	# print Counter(FINAL_WORDS).most_common(top_n)
	'''
	boundry condition when nothing is found
	'''


	if  len(FINAL_WORDS)<6:
		
		FINAL_WORDS_order_dic.update(Counter(FINAL_WORDS).most_common(top_n))
		
		# FINAL_WORDS={}
		for p_word ,count_li in rst.items():
			if p_word not in FINAL_WORDS_order_dic.keys():
				score = count_li[0]+count_li[1]/(total_rst)
				FINAL_WORDS.update({p_word:(score)})
		
		
		FINAL_WORDS_order_dic.update(Counter(FINAL_WORDS).most_common(top_n))
		
		#print FINAL_WORDS_order_dic
	if len(FINAL_WORDS_order_dic)<6:
		# print "inside"
		# FINAL_WORDS={}
		for p_word ,count_li in rft.items():
			if p_word not in FINAL_WORDS_order_dic.keys():

				score = count_li[0]+count_li[1]/(total_rft)
				FINAL_WORDS.update({p_word:(score)})
		FINAL_WORDS_order_dic.update(Counter(FINAL_WORDS).most_common(top_n))
		#print FINAL_WORDS_order_dic
	
	# print Counter(FINAL_WORDS).most_common(top_n)
	return Counter(FINAL_WORDS).most_common(top_n)


def probability_fourth_word(pw,top_n=10):
	# print pw
	global FINAL_WORDS
	FINAL_WORDS = {}
	total=0
 	for trav in pw.values():
 		total+=trav
 	# print total
							
	for p_word,count in pw.items():
	
		score=count/total
		FINAL_WORDS.update({p_word:score})	

	return Counter(FINAL_WORDS).most_common(top_n)
	
								
