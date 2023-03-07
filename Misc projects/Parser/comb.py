# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 12:48:52 2022

@author: i.adamovich
"""

import re, pandas as pd, smtplib, httpx, json
from email.message import EmailMessage
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from config import SENDER_EMAIL, APP_PASSWORD, params
from time import sleep

class scraper():
    
    def get_data():
        browser = Chrome("../chromedriver.exe")
        url = 'https://neagent.by/kvartira/snyat?roomCount=2,3,4&floor_from=1&floor_to=3&squareAllFrom=80&hasPhotos=1'
        browser.get(url)
        sleep(5)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        cards = soup.findAll('div', {"class": "c-card"})
        data = []
        
        for card in cards:
            site = 'neagent.by'
            url = card.find('div', class_='c-card__btns').find('a').get('href')
            addr = card.find('div', class_='c-card__addr').text.replace('\n', '')
            desc = card.find('div', class_='c-card__mess').text.replace('\n', ' ').strip()
            if 'вчера' in card.find('span', class_='date').text.strip():
                date = 'вчера'
            elif 'сегодня' in card.find('span', class_='date').text.strip():
                date = 'сегодня'
            elif card.find('span', class_='date').text.strip() == '':
                date = None
            else:
                date = datetime.strptime(
                    re.search(
                        '\d{4}-\d{2}-\d{2}',
                        card.find(
                            'span',
                            class_='date'
                        ).text.strip()).group(0).replace('-', '.'),
                    '%Y.%M.%d'
                ).date()
                
            try:
                time = datetime.strptime(
                    re.search(
                        '\d{2}:\d{2}',
                        card.find(
                            'span',
                            class_='date'
                        ).text.strip()).group(0) + ':00',
                    '%H:%M:%S'
                ).time()
            except:
                time = None
                
            try:
                rooms = int(card.find('div', class_='c-card__items').findAll('div', class_='c-card__item-txt')[0].text)
            except:
                rooms = None
                
            try:
                sq = float(
                    re.search(
                        '\d+',
                        card.find(
                            'div',
                            class_='c-card__items'
                        ).findAll(
                            'div',
                            class_='c-card__item-txt'
                        )[1].text.strip()
                    ).group(0)
                )
            except:
                sq = None
                
            try:
                floor = int(
                    re.search(
                        '^\d+',
                        card.find(
                            'div',
                            class_='c-card__items'
                        ).findAll(
                            'div',
                            class_='c-card__item-txt'
                        )[2].text.strip()
                    ).group(0)
                )
            except:
                floor = None
                
            try:
                price_rub = float(
                    re.search(
                        '[\d+\s*?\d*]+',
                        card.find(
                            'div',
                            class_='price'
                        ).text.replace(' ', '')
                    ).group()
                )
            except:
                price_rub = card.find('div', class_='price').text.strip()
            
            if 'койко' not in desc and 'Койко' not in desc:
                data.append([site, date, time, url, addr, rooms, sq, floor, desc, price_rub])
            else:
                continue
            
        for i in range(15, 151, 15):
            link = f'https://neagent.by/kvartira/snyat/{i}/?roomCount=3,4&floor_from=1&floor_to=3&squareAllFrom=80&hasPhotos=1'
            browser.get(link)
            sleep(8)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            cards = soup.findAll('div', {"class": "c-card"})
            if cards != []:
                
                for card in cards:
                    site = 'neagent.by'
                    url = card.find('div', class_='c-card__btns').find('a').get('href')
                    addr = card.find('div', class_='c-card__addr').text.replace('\n', '')
                    desc = card.find('div', class_='c-card__mess').text.replace('\n', ' ').strip()
                    if 'вчера' in card.find('span', class_='date').text.strip():
                        date = 'вчера'
                    elif 'сегодня' in card.find('span', class_='date').text.strip():
                        date = 'сегодня'
                    elif card.find('span', class_='date').text.strip() == '':
                        date = None
                    else:
                        date = datetime.strptime(
                            re.search(
                                '\d{4}-\d{2}-\d{2}',
                                card.find(
                                    'span',
                                    class_='date'
                                ).text.strip()
                            ).group(0).replace('-', '.'),
                            '%Y.%m.%d'
                        ).date()
            
                    try:
                        time = datetime.strptime(
                            re.search('\d{2}:\d{2}',
                                      card.find(
                                          'span',
                                          class_='date'
                                      ).text.strip()).group(0) + ':00',
                            '%H:%M:%S'
                        ).time()
                    except:
                        time = None
            
                    try:
                        rooms = int(
                            card.find(
                                'div',
                                class_='c-card__items'
                            ).findAll(
                                'div',
                                class_='c-card__item-txt'
                            )[0].text
                        )
                    except:
                        rooms = None
            
                    try:
                        sq = float(
                            re.search(
                                '\d+',
                                card.find(
                                    'div',
                                    class_='c-card__items'
                                ).findAll(
                                    'div',
                                    class_='c-card__item-txt'
                                )[1].text.strip()
                            ).group(0)
                        )
                    except:
                        sq = None
            
                    try:
                        floor = int(
                            re.search(
                                '^\d+',
                                card.find(
                                    'div',
                                    class_='c-card__items'
                                ).findAll(
                                    'div',
                                    class_='c-card__item-txt'
                                )[2].text.strip()
                            ).group(0)
                        )
                    except:
                        floor = None
            
                    try:
                        price_rub = float(
                            re.search(
                                '[\d+\s*?\d*]+',
                                card.find(
                                    'div',
                                    class_='price'
                                ).text.replace(' ','')
                            ).group()
                        )
                    except:
                        price_rub = card.find('div', class_='price').text.strip()
                        
                    if 'койко' not in desc and 'Койко' not in desc: 
                        data.append([site, date, time, url, addr, rooms, sq, floor, desc, price_rub])
                    else:
                        continue
            
            else:
                print(f'There\'re only {int(i / 15)} pages with content at {site}. Expected 10.')
                break

# =============================================================================
#                                 KVARTIRANT.BY
# =============================================================================
        site = 'kvartirant.by'
        sq, floor = None, None
        url = 'https://www.kvartirant.by/ads/flats/rent/'
        browser.get(url)
        sleep(5)
        
        browser.find_element(By.XPATH, '//*[@id="owner"]').click()
        browser.find_element(By.XPATH, '//*[@id="gw54hnrfg"]').click()
        browser.find_element(By.XPATH, '//*[@id="f9w348hr"]').click()
        browser.find_element(By.XPATH, '//*[@id="with_photo"]').click()
        browser.find_element(By.XPATH, '//*[@id="form1"]/div[10]/div[2]/input').click()
        sleep(5)
        
        soup = BeautifulSoup(browser.page_source, 'lxml')
        cards = soup.findAll('div', class_='bb-ad-item')

        if cards != []:
            for card in cards:
                url = card.find('div', class_='photo').find('a').get('href')
                addr = card.find('div', class_='title-obj').span.text
                desc = card.find('div', class_='bottom').span.text
                date = re.search('\d{2}\.\d{2}.\d{4}', card.find('p', class_='data').text).group(0)
                time = re.search('\d{2}:\d{2}', card.find('p', class_='data').text).group(0)
                rooms = card.find('div', class_='rooms-count rent-out-bg').span.text
                try:
                    price_rub = float(
                        re.search(
                            '[\d+\s*?\d*]+',
                            card.find(
                                'p',
                                class_='price'
                            ).text.replace(' ', '')
                        ).group(0)
                    )
                except:
                    price_rub = 'Договорная'
                    
                if 'койко' not in desc and 'Койко' not in desc:
                    data.append([site, date, time, url, addr, rooms, sq, floor, desc, price_rub])
                else:
                    continue
        
        for i in range(1, 21):
            link = f'https://www.kvartirant.by/ads/flats/rent/?tx_uedbadsboard_pi1%5Bsearch%5D%5Bq%5D=&tx_uedbadsboard_pi1%5Bsearch%5D%5Bdistrict%5D=0&tx_uedbadsboard_pi1%5Bsearch%5D%5Brooms%5D%5B0%5D=3&tx_uedbadsboard_pi1%5Bsearch%5D%5Brooms%5D%5B1%5D=4&tx_uedbadsboard_pi1%5Bsearch%5D%5Bprice%5D%5Bge%5D=&tx_uedbadsboard_pi1%5Bsearch%5D%5Bprice%5D%5Ble%5D=&tx_uedbadsboard_pi1%5Bsearch%5D%5Bcurrency%5D%5Be%5D=840&tx_uedbadsboard_pi1%5Bsearch%5D%5Bdate%5D=&tx_uedbadsboard_pi1%5Bsearch%5D%5Bagency_id%5D=&tx_uedbadsboard_pi1%5Bsearch%5D%5Bphoto%5D=on&tx_uedbadsboard_pi1%5Bsearch%5D%5Bowner%5D=on&page={i}'
            browser.get(link)
            sleep(8)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            cards = soup.findAll('div', class_='bb-ad-item')
            if cards != []:
                
                for card in cards:
                    url = card.find('div', class_='photo').find('a').get('href')
                    addr = card.find('div', class_='title-obj').span.text
                    desc = card.find('div', class_='bottom').span.text
                    date = datetime.strptime(
                        re.search(
                            '\d{2}\.\d{2}.\d{4}',
                            card.find(
                                'p',
                                class_='data'
                            ).text
                        ).group(0),
                        '%d.%m.%Y'
                    ).date()
                    time = datetime.strptime(
                        re.search(
                            '\d{2}:\d{2}',
                            card.find(
                                'p',
                                class_='data'
                            ).text
                        ).group(0) + ':00',
                        '%H:%M:%S'
                    ).time()
                    rooms = card.find('div', class_='rooms-count rent-out-bg').span.text
                    try:
                        price_rub = float(
                            re.search(
                                '[\d+\s*?\d*]+',
                                card.find(
                                    'p',
                                    class_='price'
                                ).text.replace(' ', '')
                            ).group(0)
                        )
                    except:
                        price_rub = 'Договорная'
                        
                    if 'койко' not in desc and 'Койко' not in desc:
                        data.append([site, date, time, url, addr, rooms, sq, floor, desc, price_rub])
                    else:
                        continue
            else:
                print(f'There\'re only {i} pages with content at {site}. Expected 20.')
                break
        
        header = ['Site', 'Date', 'Time', 'Link','Address','Rooms_n', 'Square', 'Floor', 'Description', 'Price_BYN']
        df = pd.DataFrame(data, columns = header)
        try:
            df.to_excel("../comb.xlsx", index=False)
            print('File saved.')
        except:
            print('Something went wrong. Couldn\'t save the file')
        print('Quitting...')
        browser.quit()
        print('Ahoy, Captain! All done, no errors occured!\n\nHave a nice day!')
    

    def send_mail(recipient_email, subject, content, excel_file='Null'):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = ', '.join(recipient_email)
        msg.set_content(content)
        
        if excel_file != 'Null':
            
            with open(excel_file, 'rb') as f:
                file_data = f.read()
                msg.add_attachment(
                    file_data
                    ,maintype="application"
                    ,subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    ,filename=re.search(
                        '\w+\.xlsx$',
                        excel_file
                        ).group(0)
                    )
    
        with smtplib.SMTP_SSL('smtp.mail.ru', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

    def kufar():
        with httpx.Client() as client:
            r = client.get(
                'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated',
                params=params
            )
            j = json.loads(r.text)

        page_count = len(j['pagination']['pages'])
        jj = []

        for i in range(1, page_count + 1):
            params.update(prt=str(i))
            r = httpx.get(
                'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated',
                params=params
            )
            page = json.loads(r.text)
            jj.append(page)

        dd = []

        for page in jj:
            for card in page['ads']:
                dd.append(card['ad_link'])

        s = '\n'.join(dd)
        return s