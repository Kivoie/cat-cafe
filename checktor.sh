#!/bin/bash

readonly torstate='/home/ubuntu/Documents/nyaa/.temp/torstate'
readonly space=' '
readonly colon=':'
readonly equal='='

#get the list of torrents
full_list=$(transmission-remote -l)

echo "$full_list"

printf "\n\n"

while IFS= read -r line; do
    
	downloading_name=$(grep ' Downloading ' <<< "$line" | sed -e 's/.*Downloading  //')

	if [ "${downloading_name}" ]:
	then

		dotenv -f "$torstate" -q never set "$downloading_name" 'Downloading'
	
	else



	fi

	finished_name=$(grep ' Finished ' <<< "$line" | sed -e 's/.*Finished  //')
	finished_name=${finished_name#*$space}


done <<< "$full_list"










