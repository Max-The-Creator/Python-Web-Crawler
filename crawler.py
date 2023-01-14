import logging
import re
import os
from lxml import html, etree, cssselect
from urllib.parse import urlparse
from corpus import Corpus

logger = logging.getLogger(__name__)

class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier):
        self.frontier = frontier
        self.corpus = Corpus()
        self.history = {}
        self.max = ['',0]
        self.traps = set()


    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        
        
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            url_data = self.fetch_url(url)

            urls_per_page = 0
            for next_link in self.extract_next_links(url_data):
                
                if self.corpus.get_file_name(next_link) is not None:
                    if self.is_valid(next_link):
                        urls_per_page +=1
                        self.frontier.add_url(next_link)
            if urls_per_page > self.max[1]:
                self.max[1] = urls_per_page
                self.max[0] = next_link
        
    def data_dump2(self):
        file = open('Analytics.txt', mode = 'a')
     
        file.write("\n------------ PART 2 --------------\n\n")
        
        file.write(self.max[0] + " : " + str(self.max[1]) + "\n")

        file.write("----------- PART 3  TRAPS --------------\n")
        
        file.close()
        self.identified_traps()


    def fetch_url(self, url):
        """
        This method, using the given url, should find the corresponding file in the corpus and return a dictionary
        containing the url, content of the file in binary format and the content size in bytes
        :param url: the url to be fetched
        :return: a dictionary containing the url, content and the size of the content. If the url does not
        exist in the corpus, a dictionary with content set to None and size set to 0 can be returned.
        """
        url_data = {
            "url": url,
            "content": None,
            "size": 0
        }
        path = Corpus.get_file_name(self.corpus, url)
        if path != None:
            with open(path, "rb") as file:
                data = file.read()
                file_size = os.path.getsize(path)
            url_data['content'] = data
            url_data['size'] = file_size
            return url_data

        return url_data

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        """
        outputLinks = []
        root = html.fromstring(url_data['content'])
        new_Root = root.make_links_absolute(url_data['url'], resolve_base_href=True)
        #print(type(new_Root))

        parsed_uri = urlparse(url_data['url'])
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        
        
        
        tree = etree.ElementTree(root)
        r = tree.getroot()
        select = cssselect.CSSSelector("a")
        links = [element.get('href') for element in select(r)]
        #currentPath = url_data['url'].strip('/')
        for link in links:
            if link is None:
                pass
            else:
                outputLinks.append(link)
        return outputLinks

   


    def identified_traps(self):
        file = open("Analytics.txt", mode = 'a')
        for trap in self.traps:
            file.write(trap + '\n')
        file.close()
    
    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """
        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https"]):
            return False

        domain = '{uri.scheme}://{uri.netloc}/{uri.path}'.format(uri=parsed)
        
        #Duplicate subdomains
        split_path = parsed.path.split('/')
        dict_path = {}
        for i in split_path:
            if i not in dict_path:
                dict_path[i] = 0
            else:
                dict_path[i] += 1
        for freq in dict_path.values():
            if freq > 5:
                self.traps.add(url)
                return False

        

        #Inital count and Frequency
        if domain in self.history:
            if self.history[domain] > 1000:
                self.traps.add(url)   
                return False
            else:
                self.history[domain] += 1
        else:
            self.history[domain] = 1



        
        
        try:
            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower()) 

        except TypeError:
            print("TypeError for ", parsed)
            return False

