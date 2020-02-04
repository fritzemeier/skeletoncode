import sys

def parse_args(INFO):

	MENU = { \

			"OBF":"Obfuscated algorithm file", \
			"IF":"Path to file containing all OLEdump streams combined", \
			"OF":"Output file (Not implemented)"

		}

	for i in range(1,len(sys.argv)):
		CURR = sys.argv[i]

		if CURR[:2] == "--":
			if CURR[2:] == "help":
				print_dict(MENU)
				sys.exit()

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

	obfArr = obfStr.replace(" ","").replace("\n","").split("+")

	print(obfArr)

#	sys.exit()


	obfDict = {}
	strDict = {}

	deobfStr = ""

	for i in obfArr:
#		print('"'+i.strip(" ")+'"')
		obfDict[i.replace("\n","")] = { \

						"VAR":"", \
						"P1":"", \
						"P2":""

					}

	for i in inFile:
		TMP = i.split("=")[0]

		VAR = TMP.replace(" ","").replace("\n","")

		STR =  i[(len(TMP)+1):-1]

		if VAR in obfDict.keys() and not obfDict[VAR]["VAR"]: #and "Mid" not in STR:
			nameVar, p1, p2 = STR.replace(" ","").split("(")[1].strip(")").split(",")
			#obfDict[VAR] = STR

			obfDict[VAR]["VAR"] = nameVar
			obfDict[VAR]["P1"] = p1
			obfDict[VAR]["P2"] = p2

	print_dict(obfDict)

#	sys.exit()

	for i in obfDict.keys():
		if obfDict[i]["VAR"]:
			strDict[obfDict[i]["VAR"]] = ""

	if cliArgs["IF"]:
		inFile = open(cliArgs["IF"], "r")

	for i in inFile:
		TMP = i.split("=")[0]

		VAR = TMP.strip(" ")

		STR =  i[(len(TMP)+2):-1]

		if VAR in strDict.keys() and not strDict[VAR]:
			strDict[VAR] = STR

	print_dict(strDict)

#	sys.exit()

	for i in range(0,(len(obfArr))):
		if obfArr[i] in obfDict.keys() and obfDict[obfArr[i]]["VAR"]:
			deobfStr += strDict[obfDict[obfArr[i]]["VAR"]][(int(obfDict[obfArr[i]]["P1"])):((int(obfDict[obfArr[i]]["P1"])+int(obfDict[obfArr[i]]["P2"])))]
		elif obfArr[i][:4] == "Chr(":
			deobfStr += chr(int(obfArr[i][4:-1]))
	print(deobfStr)

if __name__ == "__main__":
	main()
