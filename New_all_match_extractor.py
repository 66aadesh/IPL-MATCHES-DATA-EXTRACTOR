import requests
from scrapy.http import HtmlResponse
import json
from match_extractor import match_extractor

all_links = json.load(open("all_match_urls.json"))
# all_links = ["https://www.espncricinfo.com/series/indian-premier-league-2007-08-313494/delhi-daredevils-vs-kolkata-knight-riders-47th-match-336030/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2009-374163/mumbai-indians-vs-rajasthan-royals-7th-match-392187/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2009-374163/chennai-super-kings-vs-kolkata-knight-riders-13th-match-392193/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2011-466304/royal-challengers-bangalore-vs-rajasthan-royals-20th-match-501217/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2009-374163/chennai-super-kings-vs-kolkata-knight-riders-13th-match-392193/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2011-466304/royal-challengers-bangalore-vs-rajasthan-royals-20th-match-501217/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2011-466304/delhi-daredevils-vs-pune-warriors-68th-match-501265/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2012-520932/kings-xi-punjab-vs-pune-warriors-14th-match-548319/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2012-520932/kolkata-knight-riders-vs-deccan-chargers-32nd-match-548338/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2012-520932/royal-challengers-bangalore-vs-chennai-super-kings-34th-match-548340/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2012-520932/pune-warriors-vs-rajasthan-royals-52nd-match-548358/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2013-586733/pune-warriors-vs-sunrisers-hyderabad-22nd-match-598018/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2013-586733/royal-challengers-bangalore-vs-rajasthan-royals-27th-match-598023/full-scorecard",
# "https://www.espncricinfo.com/series/pepsi-indian-premier-league-2015-791129/kolkata-knight-riders-vs-rajasthan-royals-25th-match-829755/full-scorecard",
# "https://www.espncricinfo.com/series/pepsi-indian-premier-league-2015-791129/royal-challengers-bangalore-vs-rajasthan-royals-29th-match-829763/full-scorecard",
# "https://www.espncricinfo.com/series/pepsi-indian-premier-league-2015-791129/delhi-daredevils-vs-chennai-super-kings-49th-match-829801/full-scorecard",
# "https://www.espncricinfo.com/series/pepsi-indian-premier-league-2015-791129/royal-challengers-bangalore-vs-delhi-daredevils-55th-match-829813/full-scorecard",
# "https://www.espncricinfo.com/series/ipl-2017-1078425/royal-challengers-bangalore-vs-sunrisers-hyderabad-29th-match-1082619/full-scorecard",
# "https://www.espncricinfo.com/series/ipl-2019-1165643/chennai-super-kings-vs-delhi-capitals-50th-match-1178425/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/rajasthan-royals-vs-royal-challengers-bangalore-qualifier-2-1312199/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers-hyderabad-vs-punjab-kings-14th-match-1359488/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/delhi-capitals-vs-kolkata-knight-riders-28th-match-1359502/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super-giants-vs-chennai-super-kings-45th-match-1359519/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers-hyderabad-vs-kolkata-knight-riders-47th-match-1359521/full-scorecard",
# "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/rajasthan-royals-vs-gujarat-titans-48th-match-1359522/full-scorecard"]

print(len(all_links))

output_list=[]

for url1 in all_links:
    # print(url1)
    try:
        data = match_extractor(url1)
        output_list.append(data)
    except Exception as e:
        print(f"-----> Error occurred on url {url1}: {e}")

json.dump(output_list,open("IPL-ALL-MATCHES.json","w"),indent=2,ensure_ascii=False)


#data = match_extractor("https://www.espncricinfo.com/series/indian-premier-league-2007-08-313494/chennai-super-kings-vs-kolkata-knight-riders-11th-match-335993/full-scorecard")
#json.dump(data,open("sample.json","w"),indent=2,ensure_ascii=False)