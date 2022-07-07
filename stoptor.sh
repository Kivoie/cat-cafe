#!/bin/bash

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

