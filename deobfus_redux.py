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
		print("  "+i+" "*(10-len(i))+"		"+INFO[i])


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
		obfDict[i.strip(" ")] = "NONE"

	print_dict(obfDict)

	for i in inFile:
		if i.split("=") in obfArr.keys():


if __name__ == "__main__":
	main()
