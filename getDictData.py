import json
from myknputils import *
import BeautifulSoup

propDictName = "propDict.dict"
predDictName = "predDict.dict"
urlListName = "url.list"
DBName = "database"

propDict = None
predDict = None
DB = None

with open(propDictName) as propfd:
    propDict = json.load(propfd)
with open(predDictName) as predfd:
    predDict = json.load(predfd)

with open(urlListName) as urllfd:
    urlList = json.load(urllfd)

knp = my_knp_utils()


for url in urlList:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    for htags in soup.find_all("h1"):
        htags.extract()
    for htags in soup.find_all("h2"):
        htags.extract()
    for htags in soup.find_all("h3"):
        htags.extract()
    for htags in soup.find_all("h4"):
        htags.extract()
    for htags in soup.find_all("h5"):
        htags.extract()


    results = knp.get_knp_results(map(lambda x: x.get_text(), soup.find(id="main").find_all(p)))
    
    [
        
    ]
        
        
    
