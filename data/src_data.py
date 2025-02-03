import time
# import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

BASE_URL = "https://www.nfl.com"
PASSING_STATS_URL = "https://www.nfl.com/stats/player-stats/"
RUSHING_STATS_URL = "https://www.nfl.com/stats/player-stats/category/rushing/2024/post/all/rushingyards/desc"
RECEIVING_STATS_URL = "https://www.nfl.com/stats/player-stats/category/receiving/2024/post/all/receivingreceptions/desc"



def get_player_links(passing=0, rushing=0, receiving=0):
    """Scrape player profile links from the NFL stats page."""
    if (passing): driver.get(PASSING_STATS_URL)
    elif (rushing): driver.get(RUSHING_STATS_URL)
    elif (receiving): driver.get(RECEIVING_STATS_URL)
    time.sleep(3)  # Wait for JavaScript to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    player_links = {}

    # Find all player rows
    player_rows = soup.select("a.d3-o-player-fullname")

    for player in player_rows:
        name = player.text.strip()
        link = BASE_URL + player["href"] + "stats/"
        player_links[name] = link

    return player_links


# __________________________________________________________________________


def get_passing_stats(player_url):
    """Scrape player passing stats."""
    driver.get(player_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    stats_table = soup.select_one("table.d3-o-table")  # Adjust selector as needed

    if not stats_table:
        return None

    passing_stats = []
    for row in stats_table.select("tbody tr"):
        cells = row.find_all("td")

        if len(cells) > 1:
            wk = cells[0].text.strip()
            opp = cells[1].text.strip()
            result = cells[2].text.strip()
            comp = cells[3].text.strip()
            att_p = cells[4].text.strip()
            yds_p = cells[5].text.strip()
            avg_p = cells[6].text.strip()
            td_p = cells[7].text.strip() 
            intr = cells[8].text.strip() 
            sck = cells[9].text.strip()
            scky = cells[10].text.strip() 
            rate = cells[11].text.strip() 
            att_r = cells[12].text.strip() 
            yds_r = cells[13].text.strip() 
            avg_r = cells[14].text.strip() 
            td_r = cells[15].text.strip() 
            fum = cells[16].text.strip() 
            lost = cells[17].text.strip() 

            passing_stats.append({
                "Wk": wk,
                "Opp": opp,
                "Result": result,
                "Comp": comp,
                "Att_P": att_p,
                "Yds_P": yds_p,
                "Avg_P": avg_p,
                "TD_P": td_p,
                "Ints": intr,
                "Sck": sck,
                "Scky": scky,
                "Rate": rate,
                "Att_R": att_r,
                "Yds_R": yds_r,
                "Avg_R": avg_r,
                "TD_R": td_r,
                "Fum": fum,
                "Lost": lost,   
            })

    return passing_stats


  # __________________________________________________________________________


def get_rushing_stats(player_url):
    """Scrape player rushing stats."""
    driver.get(player_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    stats_table = soup.select_one("table.d3-o-table")  # Adjust selector as needed

    if not stats_table:
        return None

    rushing_stats = []
    for row in stats_table.select("tbody tr"):
        cells = row.find_all("td")

        if len(cells) > 1:
            wk = cells[0].text.strip()
            opp = cells[1].text.strip()
            result = cells[2].text.strip()
            att_r = cells[3].text.strip()
            yds_r = cells[4].text.strip()
            avg_r = cells[5].text.strip()
            lng_r = cells[6].text.strip()
            td_r = cells[7].text.strip() 
            rec = cells[8].text.strip() 
            yds = cells[9].text.strip() 
            avg = cells[10].text.strip() 
            lng = cells[11].text.strip() 
            td = cells[12].text.strip() 
            fum = cells[13].text.strip() 
            lost = cells[14].text.strip() 
            

            rushing_stats.append({
                "Wk": wk,
                "Opp": opp,
                "Result": result,   
                "Att_R": att_r,
                "Rds_R": yds_r,
                "Avg_R": avg_r,
                "Lng_R": lng_r,
                "TD_R": td_r,
                "Rec": rec,
                "Yds": yds,
                "Avg": avg,
                "Lng": lng,
                "TD": td,
                "Fum": fum,
                "Lost": lost
            })

    return rushing_stats


# __________________________________________________________________________


def get_receiving_stats(player_url):
    """Scrape player receiving stats."""
    driver.get(player_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    stats_table = soup.select_one("table.d3-o-table")  # Adjust selector as needed

    if not stats_table:
        return None

    receiving_stats = []
    for row in stats_table.select("tbody tr"):
        cells = row.find_all("td")

        if len(cells) > 1:
            wk = cells[0].text.strip()
            opp = cells[1].text.strip()
            result = cells[2].text.strip()
            rec_r = cells[3].text.strip()
            yds_r = cells[4].text.strip()
            lng_r = cells[5].text.strip()
            td_r = cells[6].text.strip()
            att = cells[7].text.strip() 
            yds = cells[8].text.strip() 
            avg = cells[9].text.strip() 
            lng = cells[10].text.strip() 
            td = cells[11].text.strip() 
            fum = cells[12].text.strip() 
            lost = cells[13].text.strip() 
            

            receiving_stats.append({
                "Wk": wk,
                "Opp": opp,
                "Result": result,  
                "Rec_R": rec_r, 
                "Yds_R": yds_r,
                "Lng_R": lng_r,
                "TD_R": td_r,
                "Att": att,            
                "Yds": yds,
                "Avg": avg,
                "Lng": lng,
                "TD": td,
                "Fum": fum,
                "Lost": lost
            })

    return receiving_stats


# __________________________________________________________________________


def write_player_data(passing=0, rushing=0, receiving=0):
    cat = {"passing": passing, "rushing": rushing, "receiving": receiving}
    funcs = {"passing": get_passing_stats, "rushing": get_rushing_stats, "receiving": get_receiving_stats}

    for key, value in cat.items():
        if not value: continue
        else:
            print(f"Scraping {key} stats..")

            player_links = get_player_links(**{key:1})
            all_stats = {}

            for name, url in player_links.items():
                print(f"Scraping stats for {name}...")
                stats = funcs[key](url)

                if stats:
                    all_stats[name] = stats

            # Save to CSV
            df = pd.DataFrame([
                {"Player": player, **stat} for player, stats in all_stats.items() for stat in stats
            ])
            df.to_csv(f"nfl_{key}_stats.csv", index=False)
            print(f"Data saved to nfl_{key}_stats.csv")