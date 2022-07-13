import smtplib, codecs, os, subprocess, sys, time, re
from datetime import datetime
import dotenv

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# cat-cafe Torrent Bot
# Copyright (C) 2022 Danny Vuong
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# # # # # # # # # # # # # # # # # # # # # #
# Overview: Sends the user an email once any torrent
# is completed (labeled as "Finished"). Create
# a Gmail application and save variables to a
# '.env' file in the same directory.

SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = str(dotenv.get_key('./.env', 'GMAIL_USERNAME'))
GMAIL_PASSWORD = str(dotenv.get_key('./.env', 'GMAIL_PASSWORD'))

print(GMAIL_USERNAME + "\n" + GMAIL_PASSWORD)

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
		sendTo = str(dotenv.get_key('./.env', 'SEND_TO'))
		emailSubject = 'Turing: Torrent Done! ' + passedParameter1

		try:
			torrent_list = subprocess.Popen('transmission-remote -l', stdout=subprocess.PIPE, shell=True)
		except Exception as e:
			print(e)
		else:
			current_time = datetime.now()
			torrent_list = re.sub(r"\\n", '<br>', str(torrent_list.communicate()[0]))
			torrent_list = re.sub(r"b\'", '', str(torrent_list))
			
			#email body is styled using HTML as specified in the headers at the top
			emailContent = 'Torrent \'' + str(passedParameter1) + '\' completed. Log in to verify.' + \
				"<br><br><p style=\"font-family: courier; white-space: pre-wrap; font-size: 16px;\"><b>Transmission-CLI Ubuntu - Live Report<br>Updated [" + str(current_time.strftime("%Y-%m-%d %H:%H:%S")) +\
				"]</b><br>--------------------------<br>" + str(torrent_list)[:-1] + "</p>"

			try:
				emailer.sendmail(sendTo, emailSubject, emailContent)
			except Exception as e:
				print('Email send failed. Retrying...' + "\n" + e)
				time.sleep(10)
				try:
					emailer.sendmail(sendTo, emailSubject, emailContent)
				except Exception as e:
					print('Email send failed again. Stopping.' + "\n" + e)

		
