import requests
from scrapy.http import HtmlResponse
import json

def batsman_inning_extractor(trs_selector):
    #NOTE: batting Inning 1
    batting_inning_one = {}
    batting_scorecard = []
    batter_ref_schema = {
            "batsman" : "",
            "player_tags" : [],
            "player_status" : "",
            "runs" : "",
            "number_of_balls" : "",
            "fours" : "",
            "sixs" : "",
            "strike_rate" : ""
        }
    # trs = inner_resp.xpath("(//th[contains(text(),'BATTING')])[1]/parent::tr/parent::thead/following-sibling::tbody/tr")
    trs = trs_selector
    #for tr in trs[:-4]: LEGACY CONDITION
    for tr in trs:    
        player_name_raw = [t.strip() for t  in  tr.xpath("./td[1]//text()").getall() if t.strip()]
        
        if not player_name_raw:
            continue
        player_name = player_name_raw[0]
        if player_name in ["Extras","TOTAL","Fall of wickets","Did not bat:"]:
            if player_name=="Did not bat:":
                is_substitute = True
            continue

        player_tags = player_name_raw[1:]
        player_status = tr.xpath("./td[2]//text()").get("").strip()
        runs = tr.xpath("./td[3]//text()").get("").strip()
        number_of_balls = tr.xpath("./td[4]//text()").get("").strip()
        fours = tr.xpath("./td[6]//text()").get("").strip()
        sixs = tr.xpath("./td[7]//text()").get("").strip()
        strike_rate = tr.xpath("./td[8]//text()").get("").strip()
        # print(runs,number_of_balls,fours,sixs,strike_rate)
        batting_scorecard.append({
            "batsman" : player_name,
            "player_tags" : player_tags,
            "player_status" :player_status,
            "runs" : runs,
            "number_of_balls" : number_of_balls,
            "fours" : fours,
            "sixs" : sixs,
            "strike_rate" : strike_rate
        })

    fall_of_wicket = "".join(trs[-1].xpath(".//text()").getall()[2:]).strip()

    if len(batting_scorecard)==2:
        did_not_bat = [t.strip() for t in trs[-1].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']

        total_raw = [t.strip() for t in trs[-2].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
        total_run = total_raw[2]
        total_over = total_raw[0].replace("Ov","").strip()
        run_rate = total_raw[1].split(":")[-1].strip(")").strip()
        total_wicket = total_raw[3].strip("/").strip()

        extras_raw = [t.strip() for t in trs[-3].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
        total_extra_run = extras_raw[1]
        extras = extras_raw[0]
    elif len(batting_scorecard)==11 and is_substitute:
        did_not_bat = [t.strip() for t in trs[-2].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']

        total_raw = [t.strip() for t in trs[-3].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
        total_run = total_raw[2]
        total_over = total_raw[0].replace("Ov","").strip()
        run_rate = total_raw[1].split(":")[-1].strip(")").strip()
        total_wicket = 10

        extras_raw = [t.strip() for t in trs[-4].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
        total_extra_run = extras_raw[1]
        extras = extras_raw[0]
    elif len(batting_scorecard)!=11 or is_substitute:
        did_not_bat = [t.strip() for t in trs[-2].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']

        total_raw = [t.strip() for t in trs[-3].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
        total_run = total_raw[2]
        total_over = total_raw[0].replace("Ov","").strip()
        run_rate = total_raw[1].split(":")[-1].strip(")").strip()
        total_wicket = total_raw[3].strip("/").strip()

        extras_raw = [t.strip() for t in trs[-4].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
        total_extra_run = extras_raw[1]
        extras = extras_raw[0]
    
    else:
        did_not_bat = []

        total_raw = [t.strip() for t in trs[-2].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
        print(total_raw)
        total_run = total_raw[2]
        total_over = total_raw[0].replace("Ov","").strip()
        run_rate = total_raw[1].split(":")[-1].strip(")").strip()
        total_wicket = 10

        extras_raw = [t.strip() for t in trs[-3].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
        total_extra_run = extras_raw[1]
        extras = extras_raw[0]

    batting_inning_one ={
        "batting_scorecard" : batting_scorecard,
        "fall_of_wicket" : fall_of_wicket,
        "did_not_bat" : did_not_bat,
        "total_run" : total_run,
        "total_wicket" : total_wicket,
        "total_over" : total_over,
        "run_rate" : run_rate,
        "total_extra_run" : total_extra_run,
        "extras" : extras
        
    }
    # len(batting_inning_one["batting_scorecard"])
    return batting_inning_one

def bowling_inning_extractor(trs_selector):
    #NOTE :  Bowlling Inning Two:
    bowling_inning_two = []
    bowler = {
        "bowler" :"",
        "number_of_over" :"",
        "number_of_maiden_over" :"",
        "runs_conceded" :"",
        "number_of_wicktes" :"",
        "econ" :"",
        "wide_balls" :"",
        "no_balls" :""
    }
    # trs = match_resp.xpath("(//th[contains(text(),'BOWLING')])[2]/parent::tr/parent::thead/following-sibling::tbody/tr")
    trs = trs_selector
    for tr in trs:
        bowller_name = tr.xpath("./td[1]//a/span/text()").get("")
        if not bowller_name:
            continue
        number_of_over = tr.xpath("./td[2]/text()").get("")
        number_of_maiden_over = tr.xpath("./td[3]/text()").get("")
        runs_conceded = tr.xpath("./td[4]/text()").get("")
        number_of_wicktes = tr.xpath("./td[5]//strong/text()").get("")
        econ = tr.xpath("./td[6]//text()").get("")
        wb = tr.xpath("./td[10]//text()").get("")
        nb = tr.xpath("./td[11]//text()").get("")
        # print(bowller_name,number_of_over,number_of_maiden_over,runs_conceded,number_of_wicktes,econ,wb,nb)
        bowling_inning_two.append({
            "bowler" :bowller_name,
            "number_of_over" :number_of_over,
            "number_of_maiden_over" :number_of_maiden_over,
            "runs_conceded" :runs_conceded,
            "number_of_wicktes" :number_of_wicktes,
            "econ" :econ,
            "wide_balls" :wb,
            "no_balls" :nb
        })
    len(bowling_inning_two)
    return bowling_inning_two

def match_extractor(match_url):
    row_dict = {"match_url":match_url}
    
    match_r = requests.get(match_url)
    match_resp = HtmlResponse("example.com",body=match_r.text,encoding='utf-8')
    for tr in match_resp.xpath("//span[contains(text(),'MATCH DETAILS')]/parent::div/parent::div/following-sibling::div/table/tbody/tr"):
        # print(tr.xpath("./td//span/text()").getall())
        tds =[t.strip() for t in tr.xpath("./td//span/text()").getall() if t.strip()]
        if len(tds)==2:
            row_dict[tds[0]]=tds[1]
        elif len(tds)==1:
            row_dict["stadium"]=tds[0]
        elif len(tds)>2:
            row_dict[tds[0]]=" | ".join(tds[1:])
        else:
            print("[CHECK ERROR FLOW]",tds)

    if "Umpires" in row_dict:
        row_dict["Umpires"] =[a.strip() for a in row_dict["Umpires"].split("|") if a.strip()]

    bat_in_one = batsman_inning_extractor( match_resp.xpath("(//th[contains(text(),'BATTING')])[1]/parent::tr/parent::thead/following-sibling::tbody/tr"))
    bat_in_two = batsman_inning_extractor( match_resp.xpath("(//th[contains(text(),'BATTING')])[2]/parent::tr/parent::thead/following-sibling::tbody/tr"))

    bowl_in_one = bowling_inning_extractor(match_resp.xpath("(//th[contains(text(),'BOWLING')])[1]/parent::tr/parent::thead/following-sibling::tbody/tr"))
    bowl_in_two = bowling_inning_extractor(match_resp.xpath("(//th[contains(text(),'BOWLING')])[2]/parent::tr/parent::thead/following-sibling::tbody/tr"))
    row_dict["inning_one"] = {}
    row_dict["inning_two"] = {}
    row_dict["inning_one"]["batting"] = bat_in_one
    row_dict["inning_two"]["batting"] = bat_in_two
    row_dict["inning_one"]["Bowlling"] = bowl_in_one
    row_dict["inning_two"]["Bowlling"] = bowl_in_two

    return row_dict
# all_links = json.load(open("all_match_urls.json"))
all_links = ["https://www.espncricinfo.com/series/indian-premier-league-2007-08-313494/delhi-daredevils-vs-kolkata-knight-riders-47th-match-336030/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2009-374163/mumbai-indians-vs-rajasthan-royals-7th-match-392187/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2009-374163/chennai-super-kings-vs-kolkata-knight-riders-13th-match-392193/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2011-466304/royal-challengers-bangalore-vs-rajasthan-royals-20th-match-501217/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2009-374163/chennai-super-kings-vs-kolkata-knight-riders-13th-match-392193/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2011-466304/royal-challengers-bangalore-vs-rajasthan-royals-20th-match-501217/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2011-466304/delhi-daredevils-vs-pune-warriors-68th-match-501265/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2012-520932/kings-xi-punjab-vs-pune-warriors-14th-match-548319/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2012-520932/kolkata-knight-riders-vs-deccan-chargers-32nd-match-548338/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2012-520932/royal-challengers-bangalore-vs-chennai-super-kings-34th-match-548340/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2012-520932/pune-warriors-vs-rajasthan-royals-52nd-match-548358/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2013-586733/pune-warriors-vs-sunrisers-hyderabad-22nd-match-598018/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2013-586733/royal-challengers-bangalore-vs-rajasthan-royals-27th-match-598023/full-scorecard",
"https://www.espncricinfo.com/series/pepsi-indian-premier-league-2015-791129/kolkata-knight-riders-vs-rajasthan-royals-25th-match-829755/full-scorecard",
"https://www.espncricinfo.com/series/pepsi-indian-premier-league-2015-791129/royal-challengers-bangalore-vs-rajasthan-royals-29th-match-829763/full-scorecard",
"https://www.espncricinfo.com/series/pepsi-indian-premier-league-2015-791129/delhi-daredevils-vs-chennai-super-kings-49th-match-829801/full-scorecard",
"https://www.espncricinfo.com/series/pepsi-indian-premier-league-2015-791129/royal-challengers-bangalore-vs-delhi-daredevils-55th-match-829813/full-scorecard",
"https://www.espncricinfo.com/series/ipl-2017-1078425/royal-challengers-bangalore-vs-sunrisers-hyderabad-29th-match-1082619/full-scorecard",
"https://www.espncricinfo.com/series/ipl-2019-1165643/chennai-super-kings-vs-delhi-capitals-50th-match-1178425/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/rajasthan-royals-vs-royal-challengers-bangalore-qualifier-2-1312199/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers-hyderabad-vs-punjab-kings-14th-match-1359488/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/delhi-capitals-vs-kolkata-knight-riders-28th-match-1359502/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super-giants-vs-chennai-super-kings-45th-match-1359519/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers-hyderabad-vs-kolkata-knight-riders-47th-match-1359521/full-scorecard",
"https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/rajasthan-royals-vs-gujarat-titans-48th-match-1359522/full-scorecard"]

print(len(all_links))

output_list=[]

for url1 in all_links:
    #print(url1)
    try:
        data = match_extractor(url1)
        output_list.append(data)
    except Exception as e:
        print(f"-----> Error occurred on url {url1}: {e}")

json.dump(output_list,open("ipl_matches_data_all_test.json","w"),indent=2,ensure_ascii=False)


#data = match_extractor("https://www.espncricinfo.com/series/indian-premier-league-2007-08-313494/chennai-super-kings-vs-kolkata-knight-riders-11th-match-335993/full-scorecard")
#json.dump(data,open("sample.json","w"),indent=2,ensure_ascii=False)