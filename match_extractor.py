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

    # CONDITION FOR SUBTITUTE BATSMAN: -
    is_substitute = False
    flags_list = []
    
    fall_of_wicket = ""
    did_not_bat = []
    total_run = ""
    total_wicket = ""
    total_over = ""
    run_rate = ""
    total_extra_run = ""
    extras = ""
    
    for tr in trs:  
        player_name_raw = [t.strip() for t  in  tr.xpath("./td[1]//text()").getall() if t.strip()]
        
        if not player_name_raw:
            continue
        player_name = player_name_raw[0]
        if player_name in ["Extras","TOTAL","Fall of wickets","Did not bat:"]:
            # print(player_name)
            flags_list.append(player_name)
            # if player_name=="Did not bat:":
            #     is_substitute = True
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

    if "Fall of wickets" in flags_list:
        flag_index = flags_list.index("Fall of wickets")-len(flags_list)
        fall_of_wicket = "".join(trs[flag_index].xpath(".//text()").getall()[2:]).strip()

    if "Did not bat:" in  flags_list:
        flag_index = flags_list.index("Did not bat:")-len(flags_list)
        did_not_bat = [t.strip() for t in trs[flag_index].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
        

    if "Extras" in  flags_list:
        flag_index = flags_list.index("Extras")-len(flags_list)
        extras_raw = [t.strip() for t in trs[flag_index].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
        try:
            total_extra_run = extras_raw[1]
            extras = extras_raw[0]
        except IndexError:
            pass
    
    if "TOTAL" in  flags_list:
        flag_index = flags_list.index("TOTAL")-len(flags_list)
        total_raw = [t.strip() for t in trs[flag_index].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
        total_run = total_raw[2]
        total_over = total_raw[0].replace("Ov","").strip()
        run_rate = total_raw[1].split(":")[-1].strip(")").strip()
        try:
            total_wicket = total_raw[3].strip("/").strip()
        except IndexError:
            total_wicket = 10

    # fall_of_wicket = "".join(trs[-1].xpath(".//text()").getall()[2:]).strip()

    # print(json.dumps(batting_scorecard, indent=2))
    # print(len(batting_scorecard))
    # print(is_substitute)

    # if len(batting_scorecard)==2:
    #     did_not_bat = [t.strip() for t in trs[-1].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
 
    #     total_raw = [t.strip() for t in trs[-2].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
    #     total_run = total_raw[2]
    #     total_over = total_raw[0].replace("Ov","").strip()
    #     run_rate = total_raw[1].split(":")[-1].strip(")").strip()
    #     total_wicket = total_raw[3].strip("/").strip()

    #     extras_raw = [t.strip() for t in trs[-3].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
    #     total_extra_run = extras_raw[1]
    #     extras = extras_raw[0]
    # elif len(batting_scorecard)==11 and is_substitute:
    #     did_not_bat = [t.strip() for t in trs[-2].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']

    #     total_raw = [t.strip() for t in trs[-3].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
    #     total_run = total_raw[2]
    #     total_over = total_raw[0].replace("Ov","").strip()
    #     run_rate = total_raw[1].split(":")[-1].strip(")").strip()
    #     total_wicket = 10

    #     extras_raw = [t.strip() for t in trs[-4].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
    #     total_extra_run = extras_raw[1]
    #     extras = extras_raw[0]
    # elif len(batting_scorecard)!=11 or is_substitute:
    #     did_not_bat = [t.strip() for t in trs[-2].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']

    #     total_raw = [t.strip() for t in trs[-3].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
    #     total_run = total_raw[2]
    #     total_over = total_raw[0].replace("Ov","").strip()
    #     run_rate = total_raw[1].split(":")[-1].strip(")").strip()
    #     total_wicket = total_raw[3].strip("/").strip()

    #     extras_raw = [t.strip() for t in trs[-4].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
    #     total_extra_run = extras_raw[1]
    #     extras = extras_raw[0]
    
    # else:
    #     did_not_bat = []

    #     total_raw = [t.strip() for t in trs[-2].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
    #     # print(total_raw)
    #     total_run = total_raw[2]
    #     total_over = total_raw[0].replace("Ov","").strip()
    #     run_rate = total_raw[1].split(":")[-1].strip(")").strip()
    #     total_wicket = 10

    #     extras_raw = [t.strip() for t in trs[-3].xpath(".//text()").getall()[1:] if t.strip() and t.strip()!=',']
    #     total_extra_run = extras_raw[1]
    #     extras = extras_raw[0]

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
    
    teams = match_resp.xpath("//span[@class='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate']/text()").getall()
    team_a = teams[0]
    team_b = teams[1]
    # print(team_a,team_b)
    if not team_a or not team_b:
        print("[ERROR] team name issue : ",match_url)
    row_dict["team_a"] = team_a
    row_dict["team_b"] = team_b
    
    loser = match_resp.xpath("//div[@class='ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-opacity-50 ds-mb-2']/div/@title").get("")
    if not loser:
        loser = "NA"
        winner = "NA"
    else:
        teams.remove(loser)
        winner = teams[0]
    row_dict["winner"] = winner
    row_dict["loser"] = loser
    
    
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

    is_abandoned = match_resp.xpath("//span[contains(text(), 'Match abandoned without a ball bowled')]").getall()
    # print(is_abandoned)
    is_no_result = match_resp.xpath("//span[contains(text(), 'No result')]").getall()
    # print(is_no_result)

    row_dict["inning_one"] = {}
    row_dict["inning_two"] = {}
    row_dict["inning_one"]["batting"] = {}
    row_dict["inning_two"]["batting"] = {}
    row_dict["inning_one"]["Bowlling"] = []
    row_dict["inning_two"]["Bowlling"] = []
    if not is_abandoned: 
        if not is_no_result:
            bat_in_one = batsman_inning_extractor( match_resp.xpath("(//th[contains(text(),'BATTING')])[1]/parent::tr/parent::thead/following-sibling::tbody/tr"))
            bat_in_two = batsman_inning_extractor( match_resp.xpath("(//th[contains(text(),'BATTING')])[2]/parent::tr/parent::thead/following-sibling::tbody/tr"))

            bowl_in_one = bowling_inning_extractor(match_resp.xpath("(//th[contains(text(),'BOWLING')])[1]/parent::tr/parent::thead/following-sibling::tbody/tr"))
            bowl_in_two = bowling_inning_extractor(match_resp.xpath("(//th[contains(text(),'BOWLING')])[2]/parent::tr/parent::thead/following-sibling::tbody/tr"))
            row_dict["inning_one"]["batting"] = bat_in_one
            row_dict["inning_two"]["batting"] = bat_in_two
            row_dict["inning_one"]["Bowlling"] = bowl_in_one
            row_dict["inning_two"]["Bowlling"] = bowl_in_two
        else:
            bat_in_one = batsman_inning_extractor( match_resp.xpath("(//th[contains(text(),'BATTING')])[1]/parent::tr/parent::thead/following-sibling::tbody/tr"))
            # bat_in_two = batsman_inning_extractor( match_resp.xpath("(//th[contains(text(),'BATTING')])[2]/parent::tr/parent::thead/following-sibling::tbody/tr"))

            bowl_in_one = bowling_inning_extractor(match_resp.xpath("(//th[contains(text(),'BOWLING')])[1]/parent::tr/parent::thead/following-sibling::tbody/tr"))
            # bowl_in_two = bowling_inning_extractor(match_resp.xpath("(//th[contains(text(),'BOWLING')])[2]/parent::tr/parent::thead/following-sibling::tbody/tr"))
            row_dict["inning_one"]["batting"] = bat_in_one
            row_dict["inning_one"]["Bowlling"] = bowl_in_one
            

    return row_dict

# data = match_extractor("https://www.espncricinfo.com/series/indian-premier-league-2009-374163/mumbai-indians-vs-rajasthan-royals-7th-match-392187/full-scorecard")
data = match_extractor("https://www.espncricinfo.com/series/indian-premier-league-2012-520932/kings-xi-punjab-vs-pune-warriors-14th-match-548319/full-scorecard")
json.dump(data,open("sample.json","w"),indent=2,ensure_ascii=False)