# INF-141-Assignment-2

This project entails building a webcrawler that extracts URLs from a static corpus located in a local directory

frontier.py: this file acts as a representation of a frontier. It has a method to add a URL to the frontier, get the next URL and check if the frontier has many more URLs. Additionarlly, it has a methods to save the current state of the frontier adn load existing state.

crawler.py: this file is responsible for scraping URLs from the next available link in frontier and adding the scraped links back to the frontier

corpus.py: this file is responsible for handling corpus related functionalities like mapping a URL to its local file name. In order to amke it possible to work on a crawler without accessing the ICS network, this file accesses a static corpus located in the WEBPAGES_RAW directory and maps given URLs to local file names that contain the content of that URL.

main.py: This file glues everything together and is the starting point of the program. It instantiates the frontier and the crawler and starts the crawling process. It also registers a shutdown hook to save the current frontier state in case of an error or receiving of a shutdown signal.

Analytics produced:
- Keep track of the subdomains that is visited, and count how many different URLs it has processed from each of those subdomains.
- Find the page with the most valid out links (of all pages given to the crawler). Out links are the number of links that are present on a particular webpage.
- List of donwloaded URLs and identified traps.
