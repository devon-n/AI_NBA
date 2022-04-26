# import libraries
from datetime import datetime
from pytz import timezone
import time
import requests
import pandas as pd
from datetime import date
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
chrome_options = Options()

# chrome_options.add_argument("--headless")
chrome_options.headless = True # also works
PATH = '/home/dev/Desktop/Projects/AI/chromedriver'
driver = webdriver.Chrome(PATH, options=chrome_options)

# get urls betfair and bet365
bf_url = 'https://www.betfair.com.au/exchange/plus/basketball/competition/10547864'
current_year = ' ' + str(date.today().year)

# Lists
odds_df = ''
bf_odds_list = []

# Scrape odds
driver.get(bf_url)


# Scrape
time.sleep(3)
table = driver.find_element_by_tag_name('section.coupon-card')

if table:
    
    # DATE
    date = table.find_element_by_tag_name('span.card-header-title').text
    date = date[-6:]
    date = date + current_year
    
    table_rows = table.find_elements_by_tag_name('tr')
    for table_row in table_rows:   
        
        
        # TEAMS
        team_names = table_row.find_elements_by_class_name('name')
        if len(team_names) > 0:
            vis_team = team_names[0].text
            home_team = team_names[1].text
            
        # ODDS
        prices = table_row.find_elements_by_class_name('bet-button-price')
        if len(prices) > 0:
            vis_odds = prices[0].text
            home_odds = prices[2].text
        
            if vis_team:
                odds_dict = {
                    'Date': date,
                    'Visitor': vis_team,
                    'Home': home_team,
                    'BF V Odds': vis_odds,
                    'BF H Odds': home_odds
                }
                bf_odds_list.append(odds_dict)

driver.quit()

odds_df = pd.DataFrame(bf_odds_list)
odds_df['Game'] = odds_df['Home'] + ' - ' + odds_df['Visitor']
odds_df.drop_duplicates(subset=['Game'], keep='first', inplace=True)
odds_df.drop('Game', axis=1, inplace=True)


# Save to file
old_odds = pd.read_csv('/home/dev/Desktop/Projects/AI/NBA/Web_Scraping/NBA_BF_Odds.csv')
merged = pd.concat([old_odds, odds_df])
merged.drop_duplicates(subset=['Visitor', 'Home'], inplace=True, keep='first', ignore_index=True)
merged.to_csv('/home/dev/Desktop/Projects/AI/NBA/Web_Scraping/NBA_BF_Odds.csv', index=False)