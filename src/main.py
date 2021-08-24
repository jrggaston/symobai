import time
import datetime
import mailSender
import metrics
import model
import os


def main():



    # initialize the first model
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../dataset/init_data.csv')
    system_model = model.Model(filename)

    # start monitoring. Get the metrics once to initialize
    m = metrics.Metrics()

    #object to send the notification via email
    senderObj = mailSender.mailSender("mail_cfg.cfg")

    #create the file to store the system metrics
    data_file = datetime.date.today().strftime("%Y%m%d") + "_data.csv"
    filename = os.path.join(dirname, '../dataset/' + data_file)
    m.initialize_data_file(filename)

    '''
    get the start time of the program and set a period of one day.
    after one day, the data will be stored in an new file, and we will
    train the model with the new colleted data
    '''
    start_time = datetime.datetime.now()
    data_period = datetime.timedelta(days=1)
    last_notification_timestamp = start_time - datetime.timedelta(hours=2)


    #main loop
    while True:
        # get the current time
        now = datetime.datetime.now()

        # if one day has passed, create a new file to store the data and save the previous file to
        # train the model again
        if (start_time + data_period) < now:

            #save the new timestamp
            start_time = now
            #save the previous data to update the model
            prev_data_file = filename

            #create the new data_file
            data_file = datetime.date.today().strftime("%Y%m%d") + "_data.csv"
            filename = os.path.join(dirname, '../dataset/' + data_file)
            m.initialize_data_file(filename)

            if (system_model.update_model(prev_data_file) == True):
                message = """ **** INTO: System model updated **** \n\n\n"""

                try:
                    senderObj.send(dest_address=None, message=message, attachment=filename)
                except:
                    print("error sending mail")

        #get the metrics from the system
        m.get_metrics()

        #save the metrics in the file, this will let us to update the model
        m.save_metrics(filename)

        #get the array with the last read system data
        last_sample = m.return_metrics()

        print(last_sample)

        #check if the model has detected an anomaly
        anomaly = system_model.get_prediction(last_sample)
        if anomaly == True:

            #just send one notification per hour
            if (last_notification_timestamp + datetime.timedelta(hours=1)) < now:
                message = """ **** WARNING: The system has detected an anomaly **** \n\n\n""" + system_model.get_logs()

                #get the system information
                m.collect_system_information("log.txt")

                try:
                    senderObj.send(dest_address=None, message=message,attachment="log.txt")
                    last_notification_timestamp = now
                except:
                    print("error sending mail")
        #else:
        #    print("No anomaly detected")

        #wait
        time.sleep(20)



if (__name__ == '__main__'):
    main()

