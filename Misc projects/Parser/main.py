# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 13:11:22 2022

@author: i.adamovich
"""
from comb import scraper
from mail_body import random_text
from config import RECIPIENT_EMAIL

scraper.get_data()
try:
    scraper.send_mail(
        RECIPIENT_EMAIL,
        'Квартиры на сегодня',
        scraper.kufar()  # Or random_text(), or comb.xlsx from chosen directory
    )
    print('E-mail is out.')
except:
    print('Something went wrong. Couldn\'t send the e-mail.')