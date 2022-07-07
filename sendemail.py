import smtplib, codecs, os, subprocess, sys, time
from datetime import datetime

SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'xkissova@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = codecs.encode('bppcnheqijorphwb', 'rot-13')

class Emailer:
	def sendmail(self, recipient, subject, content):

 		#Create Headers
		headers = [ "From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient, "MIME-Version: 1.0", "Content-Type: text/html" ]
		headers = "\r\n".join(headers)

		#Connect to Gmail Server
		session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
		session.ehlo()
		session.starttls()
		session.ehlo()

		#Login to Gmail
		session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

		#Send Email & Exit
		session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
		session.quit


if __name__ == "__main__":

	emailer = Emailer()

	try:
		passedParameter1 = str(sys.argv[1])
	except Exception as e:
		print(e)
	else:
		sendTo = 'mindarc14@gmail.com'
		emailSubject = 'Turing: Torrent Done! ' + passedParameter1

		try:
			torrent_list = subprocess.Popen('transmission-remote -l', stdout=subprocess.PIPE, shell=True)
		except Exception as e:
			print(e)
		else:
			current_time = datetime.now()
			emailContent = 'Torrent \'' + str(passedParameter1) + '\' completed. Log in to verify.' + \
				"\r\n\r\nTransmission-CLI Ubuntu - Live Report\r\nUpdated [" + str(current_time.strftime("%Y-%m-%d %H:%H:%S")) +\
				"]\r\n--------------------------\r\n" + str(torrent_list.communicate()[0])

			try:
				emailer.sendmail(sendTo, emailSubject, emailContent)
			except Exception as e:
				print('Email send failed.' + "\n" + e)
				time.sleep(10)
				try:
					emailer.sendmail(sendTo, emailSubject, emailContent)
				except Exception as e:
					print('Email send failed again' + "\n" + e)

		
