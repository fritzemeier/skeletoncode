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

def main():
	requestInfo = {
		"URL":"",
		"HEADERS":"",
		"DATA":"",
	}

	if len(sys.argv) > 1:
		requestInfo = parse_args(requestInfo)

	for i in requestInfo.keys():
		print(i+": "+requestInfo[i])

if __name__ == "__main__":
	main()
