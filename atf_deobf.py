import sys
#import collections
from collections import OrderedDict

def parse_args(INFO):

	MENU = { \

			"OBF":"Obfuscated algorithm file", \
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

	files = {}

	cliArgs = { \

			"IF":"", \
			"OF":""

		 }

	cliArgs = parse_args(cliArgs)

	print_dict(cliArgs)

	if cliArgs["IF"]:
		obfFile = open(cliArgs["IF"], "r")

	if cliArgs["OF"]:
		outFile = open(cliArgs["OF"], "w")

	obfStrs = OrderedDict()

	for i in obfFile:
		SFILE = i.split(":")[0]
		LO = i[(len(SFILE)+1):]
		FUNC = LO.replace(" ","").split("=")[0]
		PCS = LO.replace(" ","").replace("\n","").split("=")[1].split("+")

		obfStrs[FUNC] = { \
					"SFILE":SFILE, \
					"PCS":PCS, \
					"ALG": OrderedDict(), \
					"FULLSTR":""
				}

	deobfStrs = {}

	for KEY in obfStrs.keys():

		curr_file = open(obfStrs[KEY]["SFILE"],"r")

		files[obfStrs[KEY]["SFILE"]] = ""

		for LINE in curr_file:

			files[obfStrs[KEY]["SFILE"]] += LINE

			BEGIN = LINE.replace(" ","").split("=")[0]

			if BEGIN in obfStrs[KEY]["PCS"]:

				OSTR = LINE.replace(" ","").replace("\n","").replace(")","").split("(")[1].split(",")[0]
				ENTRY = int(LINE.replace(" ","").replace("\n","").replace(")","").split("(")[1].split(",")[1])
				LEN = int(LINE.replace(" ","").replace("\n","").replace(")","").split("(")[1].split(",")[2])

#				print("OSTR: "+OSTR+"\nENTRY: "+str(ENTRY)+"\nLEN: "+str(LEN))

				obfStrs[KEY]["ALG"][BEGIN] = { \
								"OSTR":OSTR, \
								"ENTRY":ENTRY, \
								"LEN":LEN, \
								"STR":""
								}

	for KEY in obfStrs.keys():

		for PC1 in obfStrs[KEY]["ALG"].keys():

			PC2 = obfStrs[KEY]["ALG"][PC1]["OSTR"]

			for CHUNK in files[obfStrs[KEY]["SFILE"]].split("\n"):

				if PC2 in CHUNK.replace(" ","").split("=")[0]:

					ENTRY = obfStrs[KEY]["ALG"][PC1]["ENTRY"]
					LEN = obfStrs[KEY]["ALG"][PC1]["LEN"]

					FOUND_STR = CHUNK.replace('"','').split("=")[1][ENTRY:(ENTRY+LEN+1)]
					obfStrs[KEY]["ALG"][PC1]["STR"] = FOUND_STR
					obfStrs[KEY]["FULLSTR"] += FOUND_STR

	for KEY in obfStrs.keys():
		print("============================="+KEY)

		for PC in obfStrs[KEY]["ALG"].keys():
			print("++++++++++++++++++++++"+PC)

			print(obfStrs[KEY]["ALG"][PC]["STR"])
#		print(obfStrs[KEY]["FULLSTR"])

	sys.exit()

	for KEY in obfStrs.keys():

		print("KEY: "+KEY)

		for SPLIT in files[obfStrs[KEY]["SFILE"]].split("\n"):
			if obfStrs[KEY]["OSTR"] in SPLIT:
				print(SPLIT)

#	print(str(files))



# ----------------------------------------------------------------------------------------------------
#	obfStr = obfFile.readline().split("=")[1]
#	obfArr = obfStr.replace(" ","").replace("\n","").split("+")

#	print(obfArr)

#	sys.exit()


	obfDict = {}
	strDict = {}

	deobfStr = ""

	for i in obfArr:
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
