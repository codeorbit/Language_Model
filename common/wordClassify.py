'''
	This is done to make the search in neo4j fast, instead of storing nodes(words) under label which will be the
	first letter of word, its better to store each node under labels based on the prefix of the word,
	as this will reduce look up time as well as overcome the problem of limited number of labels in neo4j
	database (free edition :P).

'''



prefix = {
	
	'a': ['ac', 'ad', 'af', 'ag', 'al', 'an', 'ap', 'as', 'at' ,'ab','ae','ar','au'],
	'b': ['ba', 'be', 'bi'],
	'c': ['ca', 'ce', 'ch', 'ci', 'co', 'cr', 'cu', 'cy'],
	'd': ['de', 'di', 'do', 'du', 'dy'],
	'e': ['ec', 'en', 'ep', 'eq', 'ex'],
	'f': ['fa', 'fe', 'fi', 'fl', 'fo', 'fr'],
	'g': ['ge', 'gi', 'gl', 'gr'],
	'h': ['he', 'ho', 'hu', 'hy'],
	'i': ['ig', 'il', 'im', 'in', 'ir'],
	'l': ['la', 'le', 'li', 'lo'],
	'm': ['ma', 'me', 'mi', 'mu', 'mo'],
	'n': ['na', 'no', 'nu'],
	'o': ['oc', 'op', 'ol', 'om', 'ov'],
	'p': ['pa', 'pe', 'po', 'ph', 'pi', 'pl', 'pn', 'pr', 'pu'],
	'q': ['qu'],
	'r': ['re'],
	's': ['sa', 'se', 'si', 'so', 'sp', 'st', 'su', 'sy'],
	't': ['te', 'th', 'to','tr', 'tu'],
	'u': ['ul', 'um' ,'un'],
	'v': ['va', 've', 'vi', 'vo'],
	'z': ['zo']

}


# suffix = 
# {
# 	a: ac, ge, al, an, ar, at
# 	b: be
# 	c: ce, cy, cs
# 	e: ed, en, em, er
# 	d: de
# 	f: fy
# 	g: ge
# 	i: it, ia, ic, ip
# 	l: ly,le
# 	m: me, my
# 	n: nt, ng, ne
# 	o: on
# 	p: pe
# 	r: re, rt, rd, ry
# 	s: se, ss, st, sh, sm
# 	t: te, ty
# 	v: ve
# }
