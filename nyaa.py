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
		tor_titles = ''										#variable to store all torrent titles
		tor_list = ''										#variable to store all magnets from the anchors
		tor_array = []										#array to associate torrent names with .torrent url
		batch_find = None

		hits = page_soup.findAll("tr" , {"class" : "success"})					#find all table rows with the class "success"

		hit_count = len(hits)									#find the number of results. this should be equal to the number of rows returned

		for i in range (0,hit_count):								#find the names of all the torrents
			titles = hits[i].text
			for title in titles.splitlines():
				if title.endswith('.mkv') or title.endswith('.mp4'):
					tor_titles += title + "\n"
				if '[batch]' in title.lower() or '(batch)' in title.lower():
					tor_titles += title + "\n"
					batch_find = i
					break
			if batch_find:
				break

		for i in range (0,hit_count):								#iterate through all rows and find all anchor <a> tags
			for link in hits[i].find_all('a', href=True):
				anchor += link['href'] + "\n"							#save all anchors to a variable	
			if i == batch_find:
				break

		for line in anchor.splitlines():							#iterate through all anchors and find all lines ending in ".torrent"
			if line.endswith('.torrent'):
				tor_list += line + "\n"								#save all torrent URLs to a variable

		tor_titles = list(tor_titles.splitlines())						#list-ify the torrent names
		tor_list = list(tor_list.splitlines())							#list-ify the torrent urls

		print(tor_titles)
		print(tor_list)

		if batch_find == None:
			for i in range (0,hit_count):								#associate each title with their own unique url
				try:
					tor_array += [i,tor_titles[i],tor_list[i]]
				except Exception as e:
					print("Error: could not populate array\n")
					print(e)
		else:
			tor_array += [batch_find,tor_titles[batch_find],tor_list[batch_find]]

		print(*tor_array, sep = "\n")

		#for i in range (0,hit_count):								#determine if there is a torrent file for 'batch' downloads
		#	if ('(batch)' or '[batch]') in tor_titles[i].lower():
		#		batch_find = i
		#		break

		for i in range (0,hit_count):
			
			if batch_find:									#if batch_find was populated from the prevoius block, then immediately set the counter to the located 'batch' file
				try:
					i = int(batch_find)
				except Exception as e:
					print(e)
							
			cur_tor = str(downloads_dir) + str(tor_titles[i])					#append the torrent title to the downloads directory for a path-and-file association

			if cur_tor.lower().endswith('.mkv'):						#if the torrent name ends with '.mkv' then strip the '.mkv' and append the '.torrent' file extension
				cur_tor = re.sub(r"].mkv", '].torrent', cur_tor)
			elif cur_tor.lower().endswith('.mp4'):						#if the torrent name ense with '.mp4' then strip the '.mp4' and append the '.torrent' file extension
				cur_tor = re.sub(r"].mp4", '].torrent', cur_tor)
			else:
				cur_tor = str(cur_tor) + '.torrent'

			cur_tor_url = 'https://nyaa.si' + str(tor_list[i])			#append the URL to the domain
			r = requests.get(str(cur_tor_url), allow_redirects=True)			#GET the .torrent file

			print(str(cur_tor) + "\n" + str(cur_tor_url) + "\n")				#display the torrent name and the full url

			try:
				open(str(cur_tor), 'wb').write(r.content)				#save the .torrent file to the file system
			except Exception as e:
				print("Error: could not write to file\n")
				print(e)
			
			if batch_find != None:								#stop iterating if the downloaded file is the 'batch' torrent file
				break

			#old logic to add and start the torrents
			#else:
			#	try:
			#		os.chmod(str(cur_tor), 0o744)
			#	except Exception as e:
			#		print("Error: could not change .torrent permissions\n")
			#		print(e)
			#	else:
			#		time.sleep(1)
			#	
			#		try:
			#			output_subprocess = subprocess.run(['transmission-remote', '-a', str(cur_tor)])
			#		except Exception as e:
			#			print("Error: could not start subprocess: transmission-remote -a\n")
			#			print(e)
			#		else:
			#			try:
			#				output_subprocess = subprocess.run(['transmission-remote', '-t', str(i+1), '-s']) 
			#			except Exception as e:
			#				print("Error: could not start subprocess: transmission-remote -s\n")
			#				print(e)


		try:
			subprocess.run(['transmission-remote', '-l'])
		except Exception as e:
			print("Error: could not start subprocess: transmission-remote -l\n")
			print(e)

