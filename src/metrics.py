import psutil
import datetime
import time
import os
import pandas as pd

class Metrics:

    def __init__(self):
        self.timestamp = 0
        self.num_process = 0
        self.num_fds = 0
        self.num_conn = 0
        self.num_ssh = 0
        self.num_active_users = 0
        self.cpu_usage = 0
        self.cpu_load = 0
        self.ram = 0
        self.tx_bytes = 0
        self.rx_bytes = 0
        self.failed_logins = 0
        self._last_failed_login_time = -1
        self._last_tx_bytes = -1
        self._last_rx_bytes = -1

        #get metrics once, to initialize previous variables
        self.get_metrics()

        self.header = "timestamp,num_process,num_fds,num_conn,num_ssh,num_active_users,cpu_usage,cpu_load,ram,tx_bytes,rx_bytes,failed_logins"
        self.columns = self.header.split(',')

        self.file = None

    def _get_timestamp(self):

        now = datetime.datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

        seconds = (now - midnight).seconds
        self.timestamp = seconds


    def _get_num_process(self):
        p = os.popen("ps aux | wc -l")
        self.num_process = int(p.read())

    def _get_num_fds(self):
        p = os.popen("lsof | wc -l")
        self.num_fds = int(p.read())
        #print ("fds: " + str(self.num_fds))

    def _get_num_conn(self):
        p = os.popen("netstat -t -u | wc -l")
        q = p.read()
        # because the two first lines are headers
        self.num_conn = int(q) - 2

    def _get_num_ssh(self):
        p = os.popen("netstat -tna | grep 'ESTABLISHED.*sshd' | wc -l")
        q = p.read()
        # because the two first lines are headers
        self.num_ssh = int(q)

    def _get_num_active_users(self):
        p = os.popen("who | wc -l")
        q = p.read()
        self.num_active_users = int(q)

    def _get_cpu_usage(self):
        # Calling psutil.cpu_precent() for 2 seconds
        self.cpu_usage = psutil.cpu_percent(2)

    def _get_cpu_load(self):
        load1, load5, load15 = psutil.getloadavg()
        self.cpu_load = (load15 / os.cpu_count()) * 100

    def _get_ram(self):
        self.ram = psutil.virtual_memory()[2]

    def _get_tx_bytes(self):
        with open("/sys/class/net/eth0/statistics/tx_bytes", "r") as a_file:

            tx_bytes = int(a_file.read())
            self.tx_bytes = 0
            if (self._last_tx_bytes != -1):
                if (tx_bytes > self._last_tx_bytes):
                    self.tx_bytes = tx_bytes - self._last_tx_bytes

            self._last_tx_bytes = tx_bytes

        #print("tx bytes = " + str(self.tx_bytes))

    def _get_rx_bytes(self):
        with open("/sys/class/net/eth0/statistics/rx_bytes", "r") as a_file:

            rx_bytes = int(a_file.read())
            self.rx_bytes = 0
            if (self._last_rx_bytes != -1):
                if (rx_bytes > self._last_rx_bytes):
                    self.tx_bytes = rx_bytes - self._last_rx_bytes

            self._last_rx_bytes = rx_bytes

        #print("rx bytes = " + str(self.rx_bytes))


    def _get_date_from_log(self, log):
        '''
        function to get the timestamp from the date of the log line
        TODO: The log does not return the year. This function assumes that
        the year of the log is the same than the year that return the time library.
        This can led to a wrong behavior when the year changes. Lets assume the happy path by now.
        '''

        words = log.split()
        # Considering date is in dd/mm/yyyy format
        date = str(datetime.datetime.now().year) + " " + words[0] + " " + words[1] + " " + words[2]
        dt_object1 = datetime.datetime.strptime(date, "%Y %b %d %H:%M:%S")

        seconds = time.mktime(dt_object1.timetuple())

        return seconds

    def _get_failed_logins(self):
        #read all logs due to a failed login
        p = os.popen("cat /var/log/auth.log | grep 'Failed password'")
        q = p.readlines()
        failed_logins = 0
        for line in q:
           # print(line)
            timestamp = self._get_date_from_log(line)
            if self._last_failed_login_time == -1 or \
               self._last_failed_login_time < timestamp:
                failed_logins += 1
                self._last_failed_login_time = timestamp

        self.failed_logins = failed_logins

        pass

    def get_metrics(self):
        self._get_timestamp()
        self._get_num_process()
        self._get_num_fds()
        self._get_num_conn()
        self._get_num_ssh()
        self._get_num_active_users()
        self._get_cpu_usage()
        self._get_cpu_load()
        self._get_ram()
        self._get_tx_bytes()
        self._get_rx_bytes()
        self._get_failed_logins()

    def save_metrics(self, file = None):

        ''' Save metrics in a file '''
        if file == None:
            save_file = self.file
        else:
            save_file = file

        with open(save_file, "a") as a_file:

            metrics = str(self.timestamp) + "," + str(self.num_process) + "," + str(self.num_fds) + "," + str(self.num_conn) + "," + str(self.num_ssh) + "," +\
                      str(self.num_active_users) + "," + str(self.cpu_usage) + "," + str(self.cpu_load) + "," + str(self.ram) + "," +\
                      str(self.tx_bytes) + "," + str(self.rx_bytes) + "," + str(self.failed_logins)

            a_file.write(metrics)
            a_file.write("\n")


    def print_metrics(self):

        ''' debug function '''
        metrics = str(self.timestamp) + "," + str(self.num_process) + "," + str(self.num_fds) + "," + str(self.num_conn) + "," + str(self.num_ssh) +\
                  "," + str(self.num_active_users) + "," + str(self.cpu_usage) + "," + str(self.cpu_load) + "," + str(self.ram) + \
                  "," + str(self.tx_bytes) + "," + str(self.rx_bytes) + "," + str(self.failed_logins)

        print (metrics)

    def collect_system_information(self, log_file):

        '''
        This method should retreive the system information and store it in a file when
        an anomaly is detected. The file with the data may be attached to the email notification
        '''
        with open(log_file, "a") as a_file:
            a_file.write("System information should be here")



    def initialize_data_file(self, data_file):


        #if file exists we should not replace it. Otherwise, we can create it
        if os.path.isfile(data_file) == False:
            with open(data_file, "a") as a_file:
                a_file.write(self.header)
                a_file.write("\n")
                self.file = data_file


    def return_metrics(self):



        data = [[ self.timestamp, self.num_process, self.num_fds, self.num_conn, self.num_ssh, self.num_active_users, self.cpu_usage, \
                self.cpu_load, self.ram, self.tx_bytes, self.rx_bytes, self.failed_logins ]]

        dframe = pd.DataFrame(data, columns=self.columns)

        return dframe



if (__name__ == '__main__'):
    metrics = Metrics()

    data_file = "collected_data.csv"

#    with open(data_file, "a") as a_file:
 #       a_file.write(metrics.header)
    print(metrics.header)
    print(metrics.return_metrics())
    #get data each 20 seconds, during one day
    #num_samples = 24 * 60 * 60 // 20

    #for i in range(0, num_samples):
    #    metrics.get_metrics()
    #    metrics.save_metrics(data_file)
    #    time.sleep(20)
