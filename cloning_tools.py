#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import random
import re
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import numpy as np


def make_driver():

# ===========================================================
    # アカウント必要サイトのログインページURLの一覧
    login_url = "https://www.kickstarter.com/login?ref=nav"
    facebook_login_url = "https://ja-jp.facebook.com"
# ===========================================================


    # クロームドライバーの場所
    # driver_path = r"C:\Users\sueki\OneDrive\デスクトップ\chromedriver_win32\chromedriver.exe"
    driver_path = "/Users/niitsukouhei/Desktop/chromedriver_ver_78"

    # クロームドライバーの初期設定
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=ja')
    # --proxy-server="<アドレス>:<ポート>"
    options.add_argument('--blink-settings=imagesEnabled=false')
    # options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=driver_path,chrome_options=options)

    driver.get(login_url)

    # ログインページにてIDとPWを記入する動作
    user_id = driver.find_element_by_id("user_session_email")
    user_pw = driver.find_element_by_id("user_session_password")
    user_id.send_keys('xxxxxxxxxxxxxxxx')
    user_pw.send_keys('xxxxxxxxxxxxxxxx')
    button = "#new_user_session > fieldset > ol > li.clearfix > input"
    driver.find_element_by_css_selector(button).click()
# -----------------------------------------------------------------------

    # driver.get(facebook_login_url)
    # try:
    #     user_id = driver.find_element_by_id("email")
    #     user_pw = driver.find_element_by_id("pass")
    #     login_button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[2]/form/table/tbody/tr[2]/td[3]/label/input")
    # except NoSuchElementException:
    #     user_id = driver.find_element_by_name("email")
    #     user_pw = driver.find_element_by_name("pass")
    #     login_button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[1]/form/div[3]/button")

    # user_id.send_keys('09063624101')
    # user_pw.send_keys('dancek666')
    # login_button.click()

    return driver



# 一覧ページからターゲット商品を抽出する
def make_product_list(driver):

    # ===========================================================
    # 抽出したいサイトのURL
    target_url = "https://www.kickstarter.com/discover/advanced?category_id=16&sort=popularity&seed=2619227&page=1"
    # ===========================================================

    # ===========================================================
    # 抽出したい項目のセレクター
    selector_products_name = 'div.clamp-5.navy-500.mb3.hover-target > a > h3'
    selector_products_sum = 'div.pb3.pt3.px3-sm.px4 > div > div.ksr-green-700.medium > div:nth-child(1) > span:nth-child(1)'
    selector_products_achievement = 'div.ksr-green-700.medium > div:nth-child(2) > span:nth-child(1)'
    selector_products_url = 'div.h30.pt4.px3.mb1px > div.clamp-5.navy-500.mb3.hover-target > a'
    selector_products_location = 'div > div > div > div:nth-child(3) > div.pb3.pt3.px3-sm.px4 > div.ksr-green-700.medium > div.flex > a'
 
    # ===========================================================

    # ===========================================================
    # ページ上の操作で必要なセレクター
    button = "#projects > div.load_more.mt3 > a"
    # ===========================================================


    driver.get(target_url)
    driver.execute_script("window.scrollBy({top: 100,behavior: \"smooth\"});")
    sleep(1)
    driver.execute_script("window.scrollBy({top: 100,behavior: \"smooth\"});")
    sleep(1)

    driver.find_element_by_css_selector(button).click()

    driver.execute_script("window.scrollBy({top: 100,behavior: \"smooth\"});")
    sleep(1)
    driver.execute_script("window.scrollBy({top: 100,behavior: \"smooth\"});")
    sleep(1)

    # スクロール操作---------------------------------------------------------------------------
    print("スクロール回数を記入してください：")
    scroll = int(input())
    for i in range(scroll):

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        sleep(1)
        driver.execute_script("window.scrollBy({top: -100,behavior: \"smooth\"});")
        sleep(1)
        driver.execute_script("window.scrollBy({top: -100,behavior: \"smooth\"});")
        sleep(1)

        print("%d回スクロールしました" % i)

    html = driver.page_source.encode('utf-8')
    soups = BeautifulSoup(html, "html.parser")

    # 一覧から欲しい項目の要素一覧========================================================
    soups_products_name = soups.select(selector_products_name)
    if soups_products_name == '':
        soups_products_name = "name_none"
    
    soups_products_sum = soups.select(selector_products_sum)
    if soups_products_sum == '':
        soups_products_sum = "1111"
    # print("soups_products_name:%s",soups_products_sum)
    soups_aschievements = soups.select(selector_products_achievement)
    if soups_aschievements == '':
        soups_aschievements = "name_aschievements"

    soups_product_url = soups.select(selector_products_url)
    if soups_product_url == '':
        soups_product_url = "name_url"

    soups_products_location = soups.select(selector_products_location)
    if soups_products_location == '':
        soups_products_location = "<name_location>"

    arr_products_name = []
    arr_products_sum = []
    arr_aschievements = []
    arr_product_url = []
    arr_products_location = []
    # 一覧から欲しい項目の要素一覧========================================================

    for soup in soups_products_name:
        soup=soup.text.strip("<h3 class=\"type-18 light hover-item-text-underline mb1\"")
        arr_products_name.append(str(soup))

    for soup in soups_products_sum:
        soup = int(re.sub("\\D", "", soup.text))
        arr_products_sum.append(int(soup))

    for soup in soups_aschievements:
        soup = int(re.sub("\\D", "", soup.text))
        arr_aschievements.append(int(soup))

    for soup in soups_product_url:
        soup1 = re.findall(r'https:\/\/www.kickstarter.com\/[^"]+',str(soup))
        str_soup = str(soup1)
        replace_soup = str_soup.replace("[","")
        replace_soup = replace_soup.replace("]","")
        replace_soup = replace_soup.replace("\'","")
        arr_product_url.append(str(replace_soup))

    for soup in soups_products_location:
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', str(soup))
        arr_products_location.append(str(cleantext))

    # np_arr = np.array([arr_products_name,\
    #                     arr_products_sum,\
    #                     arr_aschievements,\
    #                     arr_product_url,\
    #                     arr_products_location])
    np_arr = np.array([arr_products_name,\
                    arr_aschievements,\
                    arr_product_url])

    # print(type(np_arr))
    col = np_arr.shape[1]
    print(col)
    print("%d件取得しました"%col)
    return np_arr



# 取得した各商品ページ内の情報の抽出を行う
def make_price(driver,arr_product_urls):

    # ===========================================================
    # 抽出したい項目のセレクター
    selector_products_price = 'div > div > div:nth-child(3) > div > div.flex.flex-column-lg.mb4.mb5-sm > div:nth-child(1) > div.flex.items-center > span > span'
    selector_products_people = 'div > div > div:nth-child(3) > div > div.flex.flex-column-lg.mb4.mb5-sm > div.ml5.ml0-lg.mb4-lg > div'
    # selector_products_maker = "button > div.text-left.type-16.bold"
    anker_list_selector = '#experimental-creator-bio > div.fixed.t0.b0.l0.r0.z-modal-3 > div.grid-container-full.absolute.w100p > div > div > div > div > div > div.shadow-low.bg-white.p4.max-h70vh.auto-scroll-y.clip > div > div.flex.flex-column.flex-row-lg.flex-wrap.mb6 > div.flex-1.mt3.mt0-lg > div'
    # ===========================================================

    target_url = []
    arr_products_price = []
    arr_products_people = []
    facebook_contact_url= []
    web_url=[]
    twitter_url=[]
    instagram_url=[]

    for i in range(arr_product_urls.shape[1]):
        a = i + 1
        print("%d件目です"%a)
        target_url.append(arr_product_urls[2][i])
        driver.get(target_url[i])

        html = driver.page_source.encode('utf-8')
        soups = BeautifulSoup(html, "html.parser")
        soups_products_price = soups.select(selector_products_price)

        for soup in soups_products_price:
            soup = int(re.sub("\\D", "", soup.text))
            if soup == '':
                soup = None
            # print(soup)
            arr_products_price.append(int(soup))

        soups_products_people = soups.select(selector_products_people)

        for soup in soups_products_people:
            soup = int(re.sub("\\D", "", soup.text))
            if soup == '':
                soup = None
            # print(soup)
            arr_products_people.append(int(soup))


        button = "#experimental-creator-bio > button"
        target = driver.find_element_by_css_selector(button)
        driver.execute_script("arguments[0].click();", target)
        sleep(1)

        html = driver.page_source.encode('utf-8')
        soups = BeautifulSoup(html,"html.parser")

        # 連絡先を抽出する動作-----------------------------------------------------------------------
        link_soup = str(soups.select(anker_list_selector))

        facebook_link_soup = re.search(r'(http|https):\/\/www\.facebook\.com\/[a-z]*(.|)[a-z]*',link_soup)
         
        if facebook_link_soup != None:
            facebook_link_soup = str(facebook_link_soup.group())
            facebook_link_soup = facebook_link_soup.replace("[","")
            facebook_link_soup = facebook_link_soup.replace("]","")
            facebook_link_soup = facebook_link_soup.replace("\'","")

        facebook_contact_url.append(facebook_link_soup)


        web_link_soup = re.search(r'https:\/\/(www\.)?[a-z]*\.[a-z]*',link_soup)
        if web_link_soup != None:
            web_link_soup = str(web_link_soup.group())
            web_link_soup = web_link_soup.replace("[","")
            web_link_soup = web_link_soup.replace("]","")
            web_link_soup = web_link_soup.replace("\'","")

        web_url.append(web_link_soup)

        twitter_link_soup = re.search(r'(http|https):\/\/twitter\.com\/[0-9a-zA-Z_]{1,15}',link_soup)
        if twitter_link_soup != None:
            twitter_link_soup = str(twitter_link_soup.group())
            twitter_link_soup = twitter_link_soup.replace("[","")
            twitter_link_soup = twitter_link_soup.replace("]","")
            twitter_link_soup = twitter_link_soup.replace("\'","")

        twitter_url.append(twitter_link_soup)


        # instagram_link_soup = re.search(r'https:\/\/www.instagram.com\/[a-z]+',link_soup)
        # if instagram_link_soup != None:
        #     instagram_link_soup = str(instagram_link_soup.group())
        #     instagram_link_soup = instagram_link_soup.replace("[","")
        #     instagram_link_soup = instagram_link_soup.replace("]","")
        #     instagram_link_soup = instagram_link_soup.replace("\'","")

        # instagram_url.append(instagram_link_soup)



        # print(len(arr_products_price))
        # print(len(arr_products_people))
        # print(len(facebook_contact_url))



        np_arr = np.array([arr_products_price,\
                            arr_products_people,\
                            
                            # ,\
                            facebook_contact_url,\
                            web_url,\
                            twitter_url])
                            # instagram_url])

    return np_arr
