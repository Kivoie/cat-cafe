import smtplib, codecs, os, subprocess, sys, time, re
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
			torrent_list = re.sub(r"\\n", '<br>', str(torrent_list.communicate()[0]))
			torrent_list = re.sub(r"b\'", '', str(torrent_list))
			emailContent = 'Torrent \'' + str(passedParameter1) + '\' completed. Log in to verify.' + \
				"<br><br><p style=\"font-family: courier; white-space: pre-wrap; font-size: 16px;\"><b>Transmission-CLI Ubuntu - Live Report<br>Updated [" + str(current_time.strftime("%Y-%m-%d %H:%H:%S")) +\
				"]</b><br>--------------------------<br>" + str(torrent_list)[:-1] + "</p>"

			try:
				emailer.sendmail(sendTo, emailSubject, emailContent)
			except Exception as e:
				print('Email send failed.' + "\n" + e)
				time.sleep(10)
				try:
					emailer.sendmail(sendTo, emailSubject, emailContent)
				except Exception as e:
					print('Email send failed again' + "\n" + e)

		
