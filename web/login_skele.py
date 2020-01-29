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
		if DICT[i]:
			print(i+": "+DICT[i])

def print_request(REQ):
	print("HTTP/1.1 {method} {url}\n{headers}\n\n".format( #{body}".format(
		method=REQ.method,
		url=REQ.url,
		headers=REQ.headers
#		body=REQ.body
		))

def print_response(RES):
	print("HTTP/1.1 {status_code}\n{headers}\n\n{body}".format(
		status_code=RES.status_code,
		url=RES.url,
		headers='\n'.join('{}: {}'.format(i,j) for i,j in RES.headers.items()),
		body=RES.content
		))

def request_login(NAME,PASS,INFO,SPEC):
	if INFO["DATA"] and INFO["HEADERS"]:
		print(1)

		F_HEAD = {}

		for i in INFO["HEADERS"].split(","):
			print(i)
			H_KEY = i.split('=')[0]
			H_VAL = i.strip(H_KEY+'=')
			F_HEAD[H_KEY] = H_VAL

		print_dict(F_HEAD)

		REQ = requests.Request("POST",INFO["URL"], headers=F_HEAD,data=INFO["DATA"])
		print_request(REQ)

	elif INFO["DATA"]:
		print(2)
	elif INFO["HEADERS"]:
		print(3)
	else:
		print(99)

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

	requestSpecifics = {

		"UPARAM":"",
		"PPARAM":"",
		"RAND":"",
		"FAIL":""

	}

	if len(sys.argv) > 1:
		requestInfo = parse_args(requestInfo)
		userData = parse_args(userData)
		requestSpecifics = parse_args(requestSpecifics)

	if not all(VAL == "" for VAL in requestInfo.values()):
		print("Request Information")
		print_dict(requestInfo)
		print("")

	if not all(VAL == "" for VAL in userData.values()):
		print("User Data")
		print_dict(userData)
		print("")


	if userData["USER"]:

		userArr = userData["USER"].split(",")

		for NAME in userArr:
			#BEGIN PROCESSING/MAKING REQUESTS BELOW

			if userData["PASS"]:

				passArr = userData["PASS"].split(",")

				for PASS in passArr:

					RES = request_login(NAME,PASS,requestInfo,requestSpecifics)



if __name__ == "__main__":
	main()
