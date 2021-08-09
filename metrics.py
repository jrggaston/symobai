import os
import psutil

class Metrics:

    def __init__(self):
        self.num_process = 0
        self.num_fds = 0
        self.num_conn = 0
        self.num_ssh = 0
        self.num_active_users = 0
        self.cpu_usage = 0
        self.cpu_load = 0
        self.ram = 0


    def _get_num_process(self):
        p = os.popen("ps aux | wc -l")
        self.num_process = int(p.read())

    def _get_num_fds(self):
        p = os.popen("lsof | wc -l")
        self.num_fds = int(p.read())

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

    def get_metrics(self):
        self._get_num_process()
        self._get_num_fds()
        self._get_num_conn()
        self._get_num_ssh()
        self._get_num_active_users()
        self._get_cpu_usage()
        self._get_cpu_load()
        self._get_ram()

    def save_metrics(self, file):

        ''' Save metrics in a file '''

        with open(file, "a") as a_file:
            a_file.write("\n")

            metrics = str(self.num_process) + "," + str(self.num_fds) + "," + str(self.num_conn) + "," + str(self.num_ssh) + "," +\
                      str(self.num_active_users) + "," + str(self.cpu_usage) + "," + str(self.cpu_load) + "," + str(self.ram)

            a_file.write(metrics)


    def print_metrics(self):

        ''' debug function '''
        metrics = str(self.num_process) + "," + str(self.num_fds) + "," + str(self.num_conn) + "," + str(self.num_ssh) +\
                  "," + str(self.num_active_users) + "," + str(self.cpu_usage) + "," + str(self.cpu_load) + "," + str(self.ram)
        print (metrics)

    def collect_system_information(self, file):

        '''
        This method should retreive the system information and store it in a file when
        an anomaly is detected. The file with the data may be attached to the email notification
        '''

        pass




#metrics = Metrics()
#metrics.get_metrics()
#metrics.print_metrics()