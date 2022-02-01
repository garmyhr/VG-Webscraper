# VG-Webscraper
A webscraper that pulls titles and time of publishing from www.vg.no

# Running the script
    $ python web-scraper.py

Runs in an infinite loop, checking for new articles every 30 seconds.

Articles without timestamps will automatically be given a datetime with the current date at 00:00:00

Can be terminated using CTRL+C




