import sys,os
import requests

def parse_args(INFO):

	for i in range(1,len(sys.argv)):

		CURR = sys.argv[i]
		KEY = CURR.split("=")[0]
		VAL = CURR.strip(KEY+"=")

		if KEY in INFO.keys():
			INFO[KEY] = VAL

	return INFO

def print_dict(DICT):
	for i in DICT.keys():
		print(i+": "+DICT[i])

def main():
	requestInfo = {
		"URL":"",
		"HEADERS":"",
		"DATA":""
	}

	userData = {

		"USER":"",
		"PASS":"",
		"USERFILE":"",
		"PASSFILE":""

	}

	if len(sys.argv) > 1:
		requestInfo = parse_args(requestInfo)
		userData = parse_args(userData)

	if not all(VAL == "" for VAL in requestInfo.values()):
		print("Request Information")
		print_dict(requestInfo)
		print()

	if not all(VAL == "" for VAL in userData.values()):
		print("User Data")
		print_dict(userData)
		print()

if __name__ == "__main__":
	main()
