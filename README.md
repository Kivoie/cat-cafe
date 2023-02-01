# cat-cafe Torrent Bot

A Python bot for automating torrenting tasks. Operator receives an email once a torrent is finished downloading. Only supports Transmission CLI. Intended to be run on a SoC (RPi, Jetson, etc) running Ubuntu Server. Basically: automatically downloads Anime.
  
## Getting Started

Clone the repository and start the bot:
```
git clone https://github.com/Kivoie/cat-cafe.git
cd cat-cafe
python3 nyaa.py "nyaa.si/URI/here"
```
  
A valid URI will look something like `https://nyaa.si/?f=0&c=1_0&q=%5BHorribleSubs%5D+sword+art+online+2+1080p`. Make sure to enclose within **double quotation marks**. Intended to be used only on `https://nyaa.si`, will not work for other sites.

Setup a cron job for `checktor.sh` and `stoptor.sh` to start upon boot (use `crontab -e` to edit cron jobs):
```
@reboot /bin/bash /path/to/cat-cafe/checktor.sh
@reboot /bin/bash /path/to/cat-cafe/stoptor.sh
```  
  
`nyaa.py` is responsible for scraping the HTML page and downloading the torrent files. Alternatively you may adjust it to grab the torrent magnet rather than downloading a torrent file.  
`sendemail.py` is responsible for sending you the email. Replace the following: your source email (bot), source email's application password, and destination email (your personal email).  
`checktor.sh` is responsible for determining WHEN to send the email.  
`stoptor.sh` is responsible for stopping Seeding torrents.
  
## Legal
cat-cafe  Copyright (C) 2022  Danny Vuong  
This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions. See the GNU General Public License for more details.  

I, Danny Vuong, am in no way liable, whatsoever, for any damages any user may cause as a result of P2P filesharing. By using any script(s) in this repository, you agree to the risks and legal consequences of using P2P filesharing including, but not limited to, fines, lawsuits, jail sentence, malwares/viruses, and privacy risks.
