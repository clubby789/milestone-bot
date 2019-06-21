def isConsecutive(number):
	l = list(str(number))
	l = [ int(x) for x in l ]
	if l == sorted(l):
		return True
	else:
		return False

print(isConsecutive(4321))