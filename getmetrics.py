import os 
import psutil
import time

def get_metrics():

	p=os.popen("ps -aux | wc -l")
	process=int(p.read())
	print("Process: ",process)

	p=os.popen("lsof | wc -l")
	file_d=int(p.read())
	print("fd: ",file_d)


	p=os.popen("netstat -t -u | wc -l")
	q=p.read()
	# because the two first lines are headers
	conn = int(q) - 2 
	print("connections: ",conn)

	p=os.popen("netstat -tna | grep 'ESTABLISHED.*sshd' | wc -l")
	q=p.read()
	# because the two first lines are headers
	ssh_con = int(q) 
	print("ssh connections: ",ssh_con)


	p=os.popen("who | wc -l")
	q=p.read()
	users = int(q) 
	print("number of users connected: ",users)

	# Calling psutil.cpu_precent() for 2 seconds
	cpu_percent = psutil.cpu_percent(2)
	print('The CPU usage is: ', cpu_percent)

	# Getting loadover15 minutes
	load1, load5, load15 = psutil.getloadavg()
	  
	cpu_load = (load15/os.cpu_count()) * 100
	  
	print("The CPU usage is : ", cpu_load)
	  
	# Getting % usage of virtual_memory ( 3rd field)
	ram = psutil.virtual_memory()[2]
	print('RAM memory % used:', ram)

	  
	# Getting all memory using os.popen()
	# total_memory, used_memory, free_memory = map(
	#     int, os.popen('free -t -m').readlines()[-1].split()[1:])
	  
	# Memory usage
	# print("RAM memory % used:", round((used_memory/total_memory) * 100, 2))
	
	total = str(process) + "," + str(file_d) + "," + str(conn)+ "," + str(ssh_con) + "," + str(users) + "," + str(cpu_percent) + "," + str(cpu_load)+ "," + str(ram)
	
	return total


for i in range (1,5000):
	metrics = get_metrics()
	print (metrics)
	with open("data.csv", "a") as a_file:
	  a_file.write("\n")
	  a_file.write(metrics)
	  time.sleep(2)






