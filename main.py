# Copyright (c) 2024 Timo Oosterom (timo@ntdev-technology.nl)

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.remote.webelement import WebElement # only used for type hinting

from exceptions import NoBrowserSpecified # custom exceptions
from helpers import XpathElementLoaded # custom helper classes


from mpAd import MpAd
	

class MpSelApi:

	def __init__(self, browser: str = 'chrome', drvOptions: dict = {}):
		self._browser = browser.lower()
		if self._browser not in ['chrome', 'firefox', 'edge']:	# Fuck Safari
			raise NoBrowserSpecified('Invalid browser or browser not supported.')

		self._driver= self._getWebDriver(drvOptions)


	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self._driver.quit()
	

	def _getWebDriver(self, drvOptions: dict = {}) -> webdriver.Chrome: # (or other browser, chrome is only for my ide to show completions)

		# TODO fix flexible driver for multiple browsers.
		# this is now just hardcoded to chrome


		self._options: webdriver.ChromeOptions = getattr(webdriver, f'{self._browser.title()}Options')()
		self._options.add_argument("--headless")
		self._options.add_argument("--window-size=1920,1080")
		self._options.add_argument("--disable-gpu")

		# Options = __import__('selenium.webdriver.' + self._browser + '.options', fromlist=['Options'])
		# self._options: webdriver.Chrome.options = Options.Options()
		# from selenium.webdriver.chrome.options import Options
		# self._options = Options()
		# self._options.headless = True
		# for option, value in drvOptions.items():
		# 	try:
		# 		setattr(self._options, option)
		# 	except:
		# 		print(f"Option <{option}> doesn't exist")
		
		driver = getattr(webdriver, self._browser.title())
		return driver(options = self._options)

		

	def getAd(self, url: str):
		ad = MpAd(url)
		ad._getInfo(self._driver)
		return ad
	

	def getAdsSearch(self, searchUrl: str, maxAds: int = 100, pages: int = 1, startPage: int = None):
		
		urls = []
		ads = []

		self._driver.get(searchUrl)

		#adCont: WebElement = self._driver.find_element(By.XPATH, './/html/body/div/div[1]/main/div/div[2]/ul') # replaced by line below, keep this line as reference
		adCont: WebElement = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.XPATH, './/html/body/div/div[1]/main/div/div[2]/ul')))
		WDW = WebDriverWait(self._driver, 10)

		for ad in adCont.find_elements(By.XPATH, './/li'):
			try:
				elem = WDW.until(XpathElementLoaded('.//div/div/a', parent_element=ad))
				#elem = WDW.until(lambda driver: ad.find_element(By.XPATH, './/div/div/a'))
				#elem = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.XPATH, './/div/div/a'), parent=ad))
				url = elem.get_attribute('href').split('?')[0]
				
				urls.append(url)
			except Exception as e:
				print(e)

		print(f'Ads found: {len(urls)}')
		print(f"Total ads: {len(adCont.find_elements(By.XPATH, './/li'))}")

		for i, url in enumerate(urls):
			print(i, url)
			ads.append(self.getAd(url))
		
		
		return ads
		

	






if __name__ == "__main__":
	with MpSelApi(browser='chrome') as app:
		ads = app.getAdsSearch('https://www.marktplaats.nl/l/computers-en-software/windows-laptops/p/1/#q:laptop')