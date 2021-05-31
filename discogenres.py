#### discogenres by ILLVAN ####

# To run this, install BeautifulSoup 

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import os
path = os.getcwd()
csvpath = path+'\\'+'DATA.csv'  
htmlpath = path+'\\'+'DATA.html'

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
url = 'https://blog.discogs.com/en/genres-and-styles/'
headers = {'User-Agent':user_agent,} 
request = urllib.request.Request(url,None,headers)
opener = urllib.request.build_opener()
response = opener.open(request)
data = response.read()
soup = BeautifulSoup(data, "html.parser")
   
genrelist = []
genrecont = []
genredict = {}

h3s = soup.findAll('h3')
for h3 in h3s:
    genrelist.append(h3.contents[0])
uls = soup.findAll('ul')
for ul in uls:
    subgenres = []
    subgtags = ul.findAll('a')
    for subgtag in subgtags:
        if subgtag['href'].startswith('https://en.wikipedia'):
            continue
        subgspan = subgtag.find('span',{'class':'gsl-artist'})
        if subgspan is not None:
            subg = str(subgspan.contents[0])  
        else:
            subg = subgspan
        relspan = subgtag.find('span',{'class':'gsl-title'})
        #print(relspan)
        if relspan is not None:
            reltext = str(relspan.contents[0])
            relsplit = reltext.split()
            relcom = relsplit[0]
            releases = relcom.replace(',','')
        else:
            releases = relspan
        despan = subgtag.find('span',{'class':'gsl-label'})
        if despan is not None:
            de = str(despan.contents[0])  
        else:
            de = despan
        subgenres.append([subg,releases,de])
    genrecont.append(subgenres)
genrecont = genrecont[1:16]
n = 0
for cont in genrecont:
    nam = genrelist[n]
    genredict[nam] = genrecont[n]
    n = n + 1 
# print(genredict)

subdict = {}
for k,v in genredict.items():
    for sub in v:
        subname = sub[0]
        releases = sub[1]
        desc = sub[2]
        genname = k
        subdict[subname] = [genname,releases,desc]
print(subdict)  

df = pd.DataFrame.from_dict(subdict,orient='index')
mask = df.applymap(lambda x: x is None)
cols = df.columns[(mask).any()]
for col in df[cols]:
    df.loc[mask[col], col] = ''
df.to_csv(csvpath, sep=',', encoding='UTF-8'  )
df.to_html(htmlpath)
print(df)

