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

readonly email='python3 /home/ubuntu/Documents/cat-cafe/sendemail.py'
readonly space=' '

while :
do

	current_line=$(transmission-remote -l | grep 'Finished  ' | head -1)

	if [ -n "$current_line" ]
	then

		current_torrent_name=$(sed -e 's/.*Finished   //' <<< $current_line)
		current_torrent_name=${current_torrent_name#$space*$space}

		current_torrent_id=$(awk '{print $1}' <<< $current_line)

		#echo -e "finished line: ${current_line}\ntorrent name: ${current_torrent_name}\ntorrent id: ${current_torrent_id}"
		
		$email "$current_torrent_name" && transmission-remote -t ${current_torrent_id} -r

	fi
	sleep 30
done
