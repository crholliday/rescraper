from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
from bs4 import BeautifulSoup
import locale

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
            # set local to convert string to int
            locale.setlocale(locale.LC_ALL, 'en-US')
            price_decimal = Decimal(sub(r'[^\d.]', '', prop.find("li", class_="srp-item-price").getText(strip=True)))
            square_feet = locale.atoi(prop.find("li", attrs={"data-label": "property-meta-sqft"}).span.getText(strip=True))
            persquarefoot = price_decimal/square_feet

            Property.objects.get_or_create(
                detail_url=prefix + prop.a["href"],
                address=self.get_formatted_address(prop),
                external_identifier= self.get_formatted_address(prop),
                price=price_decimal,
                features=desc,
                is_multifamily=True,
                google_map_url="https://www.google.com/maps/place/" + self.get_formatted_address(prop),
                price_per_foot = persquarefoot,
            )

            prop.find()

    def get_formatted_address(self, prop):
        try:
            street = prop.find("span", class_="listing-street-address").getText()
        except AttributeError:
            street = "no street address"

        try:
            city = prop.find("span", class_="listing-city").getText()
        except AttributeError:
            city = "no city"

        try:
            state = prop.find("span", class_="listing-region").getText()
        except AttributeError:
            state = "no state"

        try:
            zip = prop.find("span", class_="listing-postal").getText()
        except AttributeError:
            zip = "no zip"

        return street + ", " + city + ", " + state + " " + zip
