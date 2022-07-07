import urllib.request, requests, os, time, re, subprocess, sys
from bs4 import BeautifulSoup

downloads_dir = '/home/ubuntu/Downloads/'


if __name__ == "__main__":

	try:
		url = str(sys.argv[1])
	except Exception as e:
		print("An error has ocurred. Received an invalid argument.\n")
		print(e)
		quit()

	try:
		#url = 'https://nyaa.si/?f=0&c=1_0&q=%5BSubsPlease%5D+Heroine+Tarumono%21+720p'			#url to query
		print(url)
		client = urllib.request.urlopen(url)							#(attempt to) open a tcp stream. May fail for servers guarded by Cloudflare
	
	except Exception as e:
		print("Unable to open remote url.\n")
		print(e)
	
	else:

		html_page = client.read()								#read the entire html page, save to variable
		client.close()										#close tcp stream


	try:
                page_soup = BeautifulSoup(html_page, "html.parser")					#use beautifulsoup parser
	
	except Exception as e:
		print("Error: BeautifulSoup failed to parse\n")
		print(e)
	
	else:
		anchor = ''										#variable to store all anchor <a> tags
		tor_titles = ''
		tor_list = ''										#variable to store all magnets from the anchors
		tor_array = []

		hits = page_soup.findAll("tr" , {"class" : "success"})					#find all table rows with the class "success"

		hit_count = len(hits)									#find the amount of results. this should be equal to the number of rows returned

		for i in range (0,hit_count):
			titles = hits[i].text
			for title in titles.splitlines():
				if title.endswith('.mkv') or title.endswith('.mp4') and ('[batch]' or '(batch)') in str(title.lower()):
					tor_titles = title + "\n"
					break

		#for i in range (0,hit_count):								#iterate through all rows and find all anchor <a> tags
		for link in hits[i].find_all('a', href=True):
			anchor += link['href'] + "\n"							#save all anchors to a variable

		for line in anchor.splitlines():							#iterate through all anchors and find all lines ending in ".torrent"
			if line.endswith('.torrent'):
				tor_list = line + "\n"								#save all torrent URLs to a variable

		tor_titles = list(tor_titles.splitlines())
		tor_list = list(tor_list.splitlines())

		print(tor_titles)
		print(tor_list)

		#for i in range (0,hit_count):
		#	try:
		#		tor_array += [[(hit_count-i),tor_titles[i],tor_list[i]]]
		#	except Exception as e:
		#		print("Error: could not populate array\n")
		#		print(e)

		#print(*tor_array, sep = "\n")
		
		#for i in range (0,hit_count):
		cur_tor = downloads_dir + str(tor_titles[-i])

		if cur_tor.endswith('.mkv'):
			cur_tor = re.sub(r"].mkv", '].torrent', cur_tor)
		elif cur_tor.endswith('.mp4'):
			cur_tor = re.sub(r"].mp4", '].torrent', cur_tor)

		cur_tor_url = 'https://nyaa.si' + str(tor_list[-i])
		r = requests.get(str(cur_tor_url), allow_redirects=True)

		print(str(cur_tor) + "\n" + str(cur_tor_url) + "\n")

		try:
			open(str(cur_tor), 'wb').write(r.content)
		except Exception as e:
			print("Error: could not write to file\n")
			print(e)
		else:
			try:
				os.chmod(str(cur_tor), 0o744)
			except Exception as e:
				print("Error: could not change .torrent permissions\n")
				print(e)
			else:
				time.sleep(1)
				
				try:
					output_subprocess = subprocess.run(['transmission-remote', '-a', str(cur_tor)])
				except Exception as e:
					print("Error: could not start subprocess: transmission-remote -a\n")
					print(e)
				else:
					try:
						output_subprocess = subprocess.run(['transmission-remote', '-t', str(i+1), '-s']) 
					except Exception as e:
						print("Error: could not start subprocess: transmission-remote -s\n")
						print(e)


		try:
			subprocess.run(['transmission-remote', '-l'])
		except Exception as e:
			print("Error: could not start subprocess: transmission-remote -l\n")
			print(e)

