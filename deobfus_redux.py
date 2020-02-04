import sys

def parse_args(INFO):

	for i in range(1,len(sys.argv)):
		CURR = sys.argv[i]

		KEY = CURR.split("=")[0]

		if KEY in INFO.keys():
			INFO[KEY] = CURR[(len(KEY)+1):]

	return INFO


def print_dict(INFO):
	for i in INFO.keys():
		print("  "+i+" "*(10-len(i))+"		"+str(INFO[i]))


def main():

	cliArgs = { \

			"OBF":"", \
			"IF":"", \
			"OF":""

		 }

	cliArgs = parse_args(cliArgs)

	print_dict(cliArgs)

	if cliArgs["OBF"]:
		obfFile = open(cliArgs["OBF"], "r")

	if cliArgs["IF"]:
		inFile = open(cliArgs["IF"], "r")

	if cliArgs["OF"]:
		outFile = open(cliArgs["OF"], "w")


	obfStr = obfFile.readline().split("=")[1]

	obfDict = {}

	for i in obfStr[:-1].split("+"):
#		print('"'+i.strip(" ")+'"')
		obfDict[i.strip(" ")] = { \

						"VAR":"", \
						"P1":"", \
						"P2":""

					}

	for i in inFile:
		TMP = i.split("=")[0]

		VAR = TMP.strip(" ")

		STR =  i[(len(TMP)+1):-1]

		if VAR in obfDict.keys(): #and "Mid" not in STR:
			nameVar, p1, p2 = STR.replace(" ","").split("(")[1].strip(")").split(",")
			#obfDict[VAR] = STR

			obfDict[VAR]["VAR"] = nameVar
			obfDict[VAR]["P1"] = p1
			obfDict[VAR]["P2"] = p2

	print_dict(obfDict)

if __name__ == "__main__":
	main()
