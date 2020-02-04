import sys
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
					"PCS":OrderedDict(), \
					"ALG": OrderedDict(), \
					"FULLSTR":""
				}

		for z in LO.replace(" ","").replace("\n","").split("=")[1].split("+"):
			obfStrs[FUNC]["PCS"][z] = z

	deobfStrs = {}

	for KEY in obfStrs.keys():

		curr_file = open(obfStrs[KEY]["SFILE"],"r")

		files[obfStrs[KEY]["SFILE"]] = ""

		for LINE in curr_file:

			files[obfStrs[KEY]["SFILE"]] += LINE

			BEGIN = LINE.replace(" ","").split("=")[0]

			if BEGIN in obfStrs[KEY]["PCS"].keys():

				OSTR = LINE.replace(" ","").replace("\n","").replace(")","").split("(")[1].split(",")[0]
				ENTRY = int(LINE.replace(" ","").replace("\n","").replace(")","").split("(")[1].split(",")[1])
				LEN = int(LINE.replace(" ","").replace("\n","").replace(")","").split("(")[1].split(",")[2])

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

					FOUND_STR = CHUNK.replace('"','').split("=")[1][ENTRY:(ENTRY+LEN)]
					obfStrs[KEY]["ALG"][PC1]["STR"] = FOUND_STR

	for KEY in obfStrs.keys():

		print("Obfuscated Variable: "+KEY)
		print("Source File: "+obfStrs[KEY]["SFILE"])
		print("De-obfuscated String\n------------------------------------------------")

		for PC in obfStrs[KEY]["PCS"].keys():

			if PC in obfStrs.keys() or PC[:4] == "Chr(":
				obfStrs[KEY]["FULLSTR"] += "<<"+PC+">>    "
				continue
			obfStrs[KEY]["FULLSTR"] += obfStrs[KEY]["ALG"][PC]["STR"]

		print(obfStrs[KEY]["FULLSTR"])
		print("\n\n")

if __name__ == "__main__":
	main()
