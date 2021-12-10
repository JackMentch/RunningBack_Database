import time
from selenium import webdriver
import warnings
from bs4 import BeautifulSoup
import pandas as pd

def get_touches_runningbacks():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.delete_all_cookies()

    driver.get('https://www.lineups.com/nfl/player-stats/running-back-rb-touches')
    driver.refresh()

    time.sleep(4)

    items = driver.find_elements_by_xpath("/html/body/app-root/div[3]/app-targets-gateway/div/div[2]/div[1]/div/pagination-controls/pagination-template/ul/li[6]")

    weeks_dropdown = driver.find_elements_by_xpath("/html/body/app-root/div[3]/app-targets-gateway/div/div[1]/div[3]/div[1]/div/div[4]/app-dropdown")


    for button in weeks_dropdown:
        button.click()
        dropdown_options = driver.find_elements_by_xpath("/html/body/app-root/div[3]/app-targets-gateway/div/div[1]/div[3]/div[1]/div/div[4]/app-dropdown/div/div/div[1]/div/label")

        for option in dropdown_options:
            option.click()
            all_weeks = driver.find_elements_by_xpath("/html/body/app-root/div[3]/app-targets-gateway/div/div[1]/div[3]/div[1]/div/div[4]/app-dropdown/div/div/div[1]/div/label")

            for get in all_weeks:
                get.click()


    time.sleep(2)

    df = pd.DataFrame()

    while items:

        html = driver.page_source
        bsObj = BeautifulSoup(html, features="html.parser")

        players = bsObj.findAll(lambda tag: tag.name == 'tr' and tag.get('class') == ['t-content'])
        stats = bsObj.findAll(lambda tag: tag.name == 'tr' and tag.get('class') == ['t-content'])


        for stat in stats:
            name = stat.find("td", {"class": "text-left player-name-col inner-col-switch"}).get_text().strip()

            touchdowns = stat.find("td", {"data-title": "TD"}).get_text().strip()
            all_touches = stat.find("td", {"data-title": "Total"}).get_text().strip()
            average_touches = stat.find("td", {"data-title": "Avg"}).get_text().strip()

            total_touches = {}

            finished = False
            week = 1

            while not finished:

                touches = stat.find("td", {"data-title": f"Week {week}"})

                if not touches:
                    break

                touches = touches.get_text().strip()

                if touches == "":
                    touches = 0

                total_touches[f"Week_{week}_Touches"] = touches
                week += 1

            df = df.append({'Name': name}, ignore_index=True)

            index = df.loc[df['Name'] == name].index

            for key, value in total_touches.items():
                df.at[index, f"{key}"] = float(value)

            df.at[index, 'TOTAL_TOUCHES'] = float(all_touches)
            df.at[index, 'AVG_TOUCHES'] = float(average_touches)
            df.at[index, 'TOTAL_TOUCHDOWNS'] = float(touchdowns)

        for item in items:
            item.click()

        items = driver.find_elements_by_xpath("/html/body/app-root/div[3]/app-targets-gateway/div/div[2]/div[1]/div/pagination-controls/pagination-template/ul/li[6]")

        if bsObj.find("li", {"class": "pagination-next disabled"}):
            break

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    # df.to_csv("touches.csv", sep=',')

    driver.quit()

    return df

