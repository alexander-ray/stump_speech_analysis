import re
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup

# Get speech as list given a url
def get_speech(url):
    try:
        # Getting text of page
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        txt = str(soup)

        # speech lies between up_partition and down_partition
        up_partition = '<span class="displaytext">'
        down_partition = '<span class="displaynotes">'
        txt = txt.split(up_partition)[1]
        txt = txt.split(down_partition)[0]
        txt = txt.replace('<p>','').replace('</p>','').replace('<br>','').replace('</br>','').replace('</div>','').replace('</span><hr noshade="noshade" size="1"/>','').strip()

        # Return list of lowercase words without punctuation
        txt = txt.lower()
        txt = re.sub('[^a-z\ \']+', " ", txt)
        words = list(txt.split())
        return {i:words.count(i) for i in set(words)}

    except Exception as e:
        return "Exception occurred \n" +str(e)

def get_relevant_urls(base_url):
    try:
        content = urllib.request.urlopen(base_url).read()
        soup = BeautifulSoup(content, 'html.parser')

        urls = []
        # All relevant urls contain ws
        tags = soup.find_all(href=re.compile("ws"))
        for t in tags:
            if("Remarks" in t.string):
                urls.append(urllib.parse.urljoin(base_url, t['href']))

        return urls
    except Exception as e:
        return "Exception occurred \n" +str(e)

def save_remarks():
    clinton_remark_urls = get_relevant_urls('http://www.presidency.ucsb.edu/2008_election_speeches.php?candidate=70&campaign=2008CLINTON&doctype=5000')
    clinton_remarks = []
    for e in clinton_remark_urls:
        clinton_remarks.append(['clinton', get_speech(e)])
    with open('clinton_remarks', 'w') as fout:
        json.dump(clinton_remarks, fout)


    obama_remark_urls = get_relevant_urls('http://www.presidency.ucsb.edu/2008_election_speeches.php?candidate=44&campaign=2008OBAMA&doctype=5000')
    obama_remarks = []
    for e in obama_remark_urls:
        obama_remarks.append(['obama', get_speech(e)])
    with open('obama_remarks', 'w') as fout:
        json.dump(obama_remarks, fout)
