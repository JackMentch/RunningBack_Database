import time
from selenium import webdriver
import warnings
from bs4 import BeautifulSoup
import pandas as pd

def get_rz_carries_runningbacks():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.delete_all_cookies()

    driver.get('https://www.lineups.com/nfl/running-back-rb-redzone-rush-attempts')
    driver.refresh()

    time.sleep(4)

    items = driver.find_elements_by_xpath("/html/body/app-root/div[3]/app-nfl/app-targets-gateway/div/div[2]/div[1]/div/pagination-controls/pagination-template/ul/li[6]")

    weeks_dropdown = driver.find_elements_by_xpath("/html/body/app-root/div[3]/app-nfl/app-targets-gateway/div/div[1]/div[3]/div[1]/div/div[4]/app-dropdown")

    for button in weeks_dropdown:
        button.click()
        dropdown_options = driver.find_elements_by_xpath("/html/body/app-root/div[3]/app-nfl/app-targets-gateway/div/div[1]/div[3]/div[1]/div/div[4]/app-dropdown/div/div/div[1]/div/label")

        for option in dropdown_options:
            option.click()
            all_weeks = driver.find_elements_by_xpath("/html/body/app-root/div[3]/app-nfl/app-targets-gateway/div/div[1]/div[3]/div[1]/div/div[4]/app-dropdown/div/div/div[1]/div/label")

            for get in all_weeks:
                get.click()


    time.sleep(2)

    df = pd.DataFrame()


    while items:

        html = driver.page_source
        bsObj = BeautifulSoup(html, features="html.parser")

        stats = bsObj.findAll(lambda tag: tag.name == 'tr' and tag.get('class') == ['t-content'])

        for stat in stats:

            name = stat.find("td", {"class": "text-left player-name-col inner-col-switch"}).get_text().strip()

            all_rz_carries = stat.find("td", {"data-title": "Total"}).get_text().strip()
            average_rz_carries = stat.find("td", {"data-title": "Avg"}).get_text().strip()

            total_rz_carries = {}

            finished = False
            week = 1

            while not finished:

                rz_carry = stat.find("td", {"data-title": f"Week {week}"})

                if not rz_carry:
                    break

                rz_carry = rz_carry.get_text().strip()

                if rz_carry == "":
                    rz_carry = 0

                total_rz_carries[f"Week_{week}_RZ_Carries"] = rz_carry
                week += 1

            df = df.append({'Name': name}, ignore_index=True)

            index = df.loc[df['Name'] == name].index

            for key, value in total_rz_carries.items():
                df.at[index, f"{key}"] = float(value)

            df.at[index, 'TOTAL_RZ_CARRIES'] = float(all_rz_carries)
            df.at[index, 'AVG_RZ_CARRIES'] = float(average_rz_carries)

        for item in items:
            item.click()

        items = driver.find_elements_by_xpath("/html/body/app-root/div[3]/app-nfl/app-targets-gateway/div/div[2]/div[1]/div/pagination-controls/pagination-template/ul/li[6]")

        if bsObj.find("li", {"class": "pagination-next disabled"}):
            break

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    driver.quit()

    return df
