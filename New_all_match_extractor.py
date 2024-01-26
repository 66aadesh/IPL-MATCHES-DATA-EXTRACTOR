import requests
from scrapy.http import HtmlResponse
import json
from match_extractor import match_extractor

all_links = json.load(open(r"IDEA\all_match_urls.json"))
print(len(all_links))

output_list=[]

for url1 in all_links:
    # print(url1)
    try:
        data = match_extractor(url1)
        output_list.append(data)
    except Exception as e:
        print(f"-----> Error occurred on url {url1}: {e}")

json.dump(output_list,open("IPL-ALL-MATCHES-2.json","w"),indent=2,ensure_ascii=False)


#data = match_extractor("https://www.espncricinfo.com/series/indian-premier-league-2007-08-313494/chennai-super-kings-vs-kolkata-knight-riders-11th-match-335993/full-scorecard")
#json.dump(data,open("sample.json","w"),indent=2,ensure_ascii=False)