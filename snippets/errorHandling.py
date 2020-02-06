def do(bar):
	if(bar < 7):
		return "Twenty"
	else:
		return False

thing = 2

if(a := do(thing)):
	print("Yay")
else:
	print("Boo")
