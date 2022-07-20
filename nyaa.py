import urllib.request, requests, os, time, re, subprocess, sys
from bs4 import BeautifulSoup

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
# Overview: Code to parse https://nyaa.si for
# HTML magnets/torrent URIs, and download
# '.torrent' files. You can setup Transmission
# to automatically add and start new .torrent
# files. Refer to the following documentation
# on configuring Transmission CLI:
# https://github.com/transmission/transmission/blob/main/docs/Editing-Configuration-Files.md

# # # # # # # # # # # # # # # # # # # # # #
# Specifics: Parses for '.mkv' and '.mp4' files
# as those are the most file formats found on
# this site. Play using VLC media player or
# any equivalent player with '.mkv' support.
# If code finds a 'batch' file, download that
# instead of each file individually.

downloads_dir = '/home/ubuntu/Downloads/'

if __name__ == "__main__":

	print("\tcat-cafe  Copyright (C) 2022  Danny Vuong\n\tThis program comes with ABSOLUTELY NO WARRANTY.\n\tThis is free software, and you are welcome to redistribute it\n\tunder certain conditions.\n\n")

	try:
		url = str(sys.argv[1])
	except Exception as e:
		print("An error has ocurred. Received an invalid argument.\n")
		print(e)
		quit()

	try:
		print(url)
		client = urllib.request.urlopen(url)							#(attempt to) open a tcp stream. May fail for servers guarded by Cloudflare (?)
	
	except Exception as e:
		print("Unable to open remote url.\n")
		print(e)
	
	else:

		html_page = client.read()								#read the entire html page, save to variable
	finally:
		client.close()										#close tcp stream


	try:
                page_soup = BeautifulSoup(html_page, "html.parser")					#use beautifulsoup parser
	
	except Exception as e:
		print("Error: BeautifulSoup failed to parse\n")
		print(e)
		quit()
	
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
				if '[batch]' in title.lower() or '(batch)' in title.lower() and 'unofficial batch' not in title.lower():
					tor_titles += title + "\n"
					batch_find = i
					break
			if batch_find != None:
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
			for i in range (0,hit_count):							#associate each title with their own unique url
				try:
					tor_array += [i,tor_titles[i],tor_list[i]]
				except Exception as e:
					print("Error: could not populate array\n")
					print(e)
		else:
			tor_array += [batch_find,tor_titles[batch_find],tor_list[batch_find]]

		print(*tor_array, sep = "\n")

		for i in range (0,hit_count):
			
			if batch_find:									#if batch_find was populated from the prevoius block, then immediately set the counter to the located 'batch' file
				try:
					i = int(batch_find)
				except Exception as e:
					print(e)
							
			cur_tor = str(downloads_dir) + str(tor_titles[i])				#append the torrent title to the downloads directory for a path-and-file association

			if cur_tor.lower().endswith('.mkv'):						#if the torrent name ends with '.mkv' then strip the '.mkv' and append the '.torrent' file extension
				cur_tor = re.sub(r"].mkv", '].torrent', cur_tor)
			elif cur_tor.lower().endswith('.mp4'):						#if the torrent name ense with '.mp4' then strip the '.mp4' and append the '.torrent' file extension
				cur_tor = re.sub(r"].mp4", '].torrent', cur_tor)
			else:
				cur_tor = str(cur_tor) + '.torrent'

			cur_tor_url = 'https://nyaa.si' + str(tor_list[i])				#append the URL to the domain
			r = requests.get(str(cur_tor_url), allow_redirects=True)			#GET the .torrent file

			print(str(cur_tor) + "\n" + str(cur_tor_url) + "\n")				#display the torrent name and the full url

			try:
				open(str(cur_tor), 'wb').write(r.content)				#save the .torrent file to the file system
			except Exception as e:
				print("Error: could not write to file\n")
				print(e)
			
			if batch_find != None:								#stop iterating if the downloaded file is the 'batch' torrent file
				break

			#old logic to add and start each torrent downloaded. Use this if you do not want to use auto-start feature in Transmission CLI.
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

