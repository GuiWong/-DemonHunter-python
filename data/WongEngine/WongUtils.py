

def check_class(obj,name,debug=False):

	clas= obj.__class__
	class_list = list(clas.__bases__)
	class_list.append(clas)

	result=False
	for c in class_list:

		if c.__name__==name:
			result = True

		if debug:
			print c.__name__

	return result


def get_next(liste,elem):

	a=None
	print elem
	for i in range(len(liste)):
		if liste[i]==elem:
			a=i+1
			if a>=len(liste):
				a=0
			break
	if a!=None:
		return liste[a]
	else:
		return elem

def tile_distance(pos1,pos2):

	return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def idle():
	print 'the button do nothing'
