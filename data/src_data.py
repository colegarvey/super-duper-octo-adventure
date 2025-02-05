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
PASSING_STATS_URLS = {
    '2024': ["https://www.nfl.com/stats/player-stats/category/passing/2024/post/all/passingyards/desc",
            "https://www.nfl.com/stats/player-stats/category/passing/2024/REG/all/passingyards/DESC?aftercursor=AAAAGQAAABlAoMIAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlNVFExSWl3aU16SXdNRFF6TkRFdE5USXpOUzA0TnprM0xUTmlPV0V0TUdReU56RXhZekJpWXpJM0lpd2lNakF5TkNKZGZRPT0=",
            "https://www.nfl.com/stats/player-stats/category/passing/2024/REG/all/passingyards/DESC?aftercursor=AAAAMgAAADJAdpAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXpOakVpTENJek1qQXdORFEwWmkwME1qTXdMVEl6TmpBdE9HVXhOQzFrWW1KbE1XUmxaR1V4TWpBaUxDSXlNREkwSWwxOQ=="],
    '2023': ["https://www.nfl.com/stats/player-stats/category/passing/2023/post/all/passingyards/DESC",
            "https://www.nfl.com/stats/player-stats/category/passing/2023/REG/all/passingyards/DESC?aftercursor=AAAAGQAAABlAogoAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlNekE1SWl3aU16SXdNRFF5TlRVdE5USTJOeTA1TnpNeExUZ3hZemd0TkRnMk56TmtZMlZqTldVeUlpd2lNakF5TXlKZGZRPT0=",
            "https://www.nfl.com/stats/player-stats/category/passing/2023/REG/all/passingyards/DESC?aftercursor=AAAAMgAAADJAgPgAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFORE1pTENJek1qQXdOR00wWmkwME16TTNMVFEwT0RJdE9UQTBZeTFoTkRkbU9HUm1NV1EwTVdJaUxDSXlNREl6SWwxOQ=="],
    '2022': ["https://www.nfl.com/stats/player-stats/category/passing/2022/post/all/passingyards/desc",
            "https://www.nfl.com/stats/player-stats/category/passing/2022/REG/all/passingyards/DESC?aftercursor=AAAAGQAAABlAooAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlNelk0SWl3aU16SXdNRFJrTlRVdE5USTJOeTB3TkRFekxUaGtNell0WVRWak0yWmtOemd4WVdFd0lpd2lNakF5TWlKZGZRPT0=",
            "https://www.nfl.com/stats/player-stats/category/passing/2022/REG/all/passingyards/DESC?aftercursor=AAAAMgAAADJAgegAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFOek1pTENJek1qQXdORFUwT0MwMFl6UXlMVFkxTkRFdFlUSmxaaTFoWWpneVpEbG1PR0ZpWlRraUxDSXlNREl5SWwxOQ=="]
    }
RUSHING_STATS_URLS = "https://www.nfl.com/stats/player-stats/category/rushing/2024/post/all/rushingyards/desc"
RECEIVING_STATS_URLS = ["https://www.nfl.com/stats/player-stats/category/receiving/2024/post/all/receivingreceptions/desc"]


def link_helper(lst_of_links):
    p_links = {}

    for link in lst_of_links:
        driver.get(link)
        time.sleep(3)  # Wait for JavaScript to load
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find all player rows
        player_rows = soup.select("a.d3-o-player-fullname")

        for player in player_rows:
            name = player.text.strip()
            link = BASE_URL + player["href"] + "stats/"
            p_links[name] = link

        return p_links


def get_player_links(passing=0, rushing=0, receiving=0):
    """Scrape player profile links from the NFL stats page."""
    player_links = {}

    if (passing): 
        for key, value in PASSING_STATS_URLS.items():
            player_links[key] = link_helper(value)
    elif (rushing):
        for key, value in RUSHING_STATS_URLS.items():
            player_links[key] = link_helper(value)
    elif (receiving):
        for key, value in RECEIVING_STATS_URLS.items():
            player_links[key] = link_helper(value)

    return player_links


# __________________________________________________________________________


def get_passing_stats(player_url, year):
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
                "Year": year,
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


def get_rushing_stats(player_url, year):
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
                "Year": year,
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


def get_receiving_stats(player_url, year):
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
                "Year": year,
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

            player_links_dict = get_player_links(**{key:1})
            all_stats = {}

            for year, links in player_links_dict.items():

                for name, url in links.items():
                    print(f"Scraping stats for {name}...")
                    stats = funcs[key](url, year)

                    if stats:
                        all_stats[(name, year)] = stats

            # Save to CSV
            df = pd.DataFrame([
                {"Player": player[0], **stat} for player, stats in all_stats.items() for stat in stats
            ])
            df.to_csv(f"nfl_{key}_stats.csv", index=False)
            print(f"Data saved to nfl_{key}_stats.csv")