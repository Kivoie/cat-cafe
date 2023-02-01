#!/bin/bash

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
# Overview: Background task to remove torrents
# that are already finished from the Transmission
# torrent list. Removes the torrent metadata, not
# the actual downloaded data.

readonly email='sudo python3 /home/ubuntu/Documents/cat-cafe/sendemail.py'
readonly animelist='/home/ubuntu/Downloads/animelist'
readonly space=' '

while :
do

	current_line=$(transmission-remote -l | grep 'Finished  ' | head -1)					#find the torrents that are already marked as finished

	if [ -n "$current_line" ]										#each torrent entry contains data like down/up, total size, ETA, state, etc
	then	

		current_torrent_name=$(sed -e 's/.*Finished   //' <<< $current_line)				#strip all leading characters, until and including the longest occurence of string 'Finished'
		current_torrent_name=${current_torrent_name#$space*$space}					#strip all leading space ' ' characters

		current_torrent_id=$(awk '{print $1}' <<< $current_line)					#isolate for the first variable in the torrent entry (the torrent ID number). ID does not persist upon daemon restart

		$email "${current_torrent_name}" && sudo transmission-remote -t ${current_torrent_id} -r	#run the email python program with the torrent title as the subject line, and remove said torrent from list
		printf "${current_torrent_name}\n" >> $animelist						#log the torrent name to the anime list
		sort -o $animelist $animelist									#sorts the animelist in a neat, ascending fashion
		awk -i inplace '!seen[$0]++' $animelist								#removes duplicate lines while editing file in place

	fi
	sleep 30												#run check every 30 seconds
done
