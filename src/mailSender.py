import smtplib, ssl, getpass
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication




class mailSender:
    def __init__(self, config_file):

        with open(config_file, "r") as cfg_file:
            lines = cfg_file.readlines()
            for line in lines:
                if line.find("port") != -1:
                    result = line.split(":")
                    self.port = int(result[1].strip("\n"))
                    #print(self.port)

                if line.find("smtp_server") != -1:
                    result = line.split(":")
                    self.smtp_server = result[1].lstrip().strip("\n")
                    #print(self.smtp_server)

                if line.find("sender") != -1:
                    result = line.split(":")
                    self.sender_email = result[1].lstrip().strip("\n")
                    #print(self.sender_email)

                if line.find("password") != -1:
                    result = line.split(":")
                    self.password = result[1].lstrip().strip("\n")
                    #print (self.password)

                if line.find("defaultDest") != -1:
                    result = line.split(":")
                    self.dest_address = result[1].lstrip().strip("\n")
                    #print (self.password)

    def send(self, dest_address, message, attachment):

        msg = MIMEMultipart()

        if (dest_address == None):
            dest_address = self.dest_address

        msg['Subject'] = 'Symobai ALERT!'
        msg['From'] = self.sender_email
        msg['To'] = ", ".join(dest_address)

        if attachment != None:
            with open(attachment, 'r') as f:
                part = MIMEApplication(f.read(), Name=basename(attachment))

            part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(attachment))
            msg.attach(part)

        msg.attach(MIMEText(message, 'plain'))

        #msg = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}\r\n".format(self.sender_email, dest_address, "Hi there", message)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            try:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, dest_address, msg.as_string())
                result = True
            except:
                print("Error sending mail.")
                result = False

        return result

#message = """This message is sent from Python."""

##senderObj = mailSender("mail_cfg.cfg")
##senderObj.send(dest_address= ["jorgeandelos@protonmail.com", "gastonpuig@gmail.com"], message=message,attachment="mailSender.py")
#senderObj.send(dest_address="jorgeandelos@protonmail.com", message=message, attachment="mailSender.py")