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

while :
do
	sleep 30									#poll every n seconds

	while :
	do
		echo "checking torrents..."
		full_list=$(transmission-remote -l)						#get the list of all added torrents
		curtor=$(grep -i 'seeding' <<< $full_list | head -1)				#select the current torrent
		echo "selected torrent: ${curtor}"

		if [ -z "${curtor}" ]								#check if any torrent exists. if not, then skip to next iteration
		then
			break
		fi

		if [ "$(awk '{print $5}' <<< $curtor)" != 'Done' ]				#check if the current torrent is labeled as Done. pretty sure this line is redundant
		then
			break
		fi

		curtor_id=$(awk '{print $1}' <<< $curtor)					#find the ID for the current torrent

		transmission-remote -t ${curtor_id} -S						#stop the selected torrent from the list
		sleep 1

	done
done

