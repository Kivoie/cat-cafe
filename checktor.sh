#!/bin/bash

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
