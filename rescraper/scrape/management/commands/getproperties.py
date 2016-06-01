from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
from bs4 import BeautifulSoup

from decimal import Decimal
from re import sub

from scrape.models import Property


class Command(BaseCommand):
    help = 'Loads properties into database'

    def handle(self, *args, **options):
        self.load_realtor_properties()

        self.stdout.write(self.style.SUCCESS('Successfully loaded properties'))

    # Load the realtor.com properties into the Property objects
    def load_realtor_properties(self):
        # Use selenium to make this as painless as possible (javascript redirects, etc)
        driver = webdriver.Chrome('c:/chromedriver/chromedriver.exe')
        driver.get(
                'http://www.realtor.com/realestateandhomes-search/73103/type-multi-family-home/radius-5/sby-6?pgsz=100')

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        prefix = "http://www.realtor.com"
        properties = soup.find_all("div", class_="srp-item-body")

        for prop in properties:
            desc = ""
            desc_ul = prop.find("ul", class_="property-meta").find_all("li")
            for item in desc_ul:
                desc += item.get_text(strip=False) + ", "

            # Convert string to decimal
            price_decimal = Decimal(sub(r'[^\d.]', '', prop.find("li", class_="srp-item-price").getText(strip=True)))

            Property.objects.get_or_create(
                detail_url=prefix + prop.a["href"],
                address=prop.a.getText(strip=True),
                external_identifier=prop.a.getText(strip=True),
                price=price_decimal,
                features=desc,
                is_multifamily=True,
            )
