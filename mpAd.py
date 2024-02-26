# Copyright (c) 2024 Timo Oosterom (timo@ntdev-technology.nl)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import mpAdDateToDateTime, mpBidDateToDateTime
from datetime import datetime



class MpBid:
	def __init__(self, ad: 'MpAd', bidder: str, amount: int, date: datetime):
		"""
		A little class to store bids on MpAd ads.
		
		:param ad: (MpAd) the ad the bid is placed on
		:param bidder: (str) the name of the bidder
		:param amount: (int) the amount of the bid
		:param date: (datetime) the date and time the bid was placed
		"""
	
		self._bidder	: str 		= bidder	# name of the bidder
		self._amount	: int 		= amount	# amount of the bid
		self._date		: datetime 	= date		# date and time the bid was placed
		self._Ad		: MpAd		= ad 		# the ad the bid is placed on


	def __str__(self):
		return f'€{self.amount} by {self.bidder} on {self.date.strftime("%d-%m-%Y")}'


	def __eq__(self, other: object) -> bool:
		if not isinstance(other, MpBid):
			return False
		elif (self._Ad == other._Ad) and (self._bidder == other._bidder) and (self._amount == other._amount) and (self._date == other._date):
			return True
		else:
			return False
		
	def __ne__(self, other: object) -> bool:
		return not self.__eq__(other)


	@property
	def bidder(self):
		return self._bidder
	
	@property
	def amount(self):
		return self._amount
	
	@property
	def date(self):
		return self._date


class MpAd:
	def __init__(self, url: str) -> None:
		"""

		:param url: (str) the url of the ad
		"""
		self._url			: str 			= url									# url of the ad
		self._id			: int			= url.split('/')[-1].split('-')[0]		# id of the ad
		self._name			: str			= ''									# name of the ad	
		self._description	: str 			= ''									# description of the ad
		self._price			: float			= 0.0									# asking price of the ad
		self._bidding 		: bool			= False									# is bidding enabled
		self._bids			: list[MpBid]	= []									# list of bids on the ad sorted by date. latest first
		self._date			: datetime 		= None									# date and time the ad was posted


	def _getInfo(self, driver: webdriver.Chrome) -> None:
		WDW = WebDriverWait(driver, 10)
		driver.get(self._url)
		self._name = WDW.until(EC.presence_of_element_located((By.CLASS_NAME, 'Listing-title'))).text
		self._description = driver.find_element(By.CLASS_NAME, 'Description-description').find_element(By.XPATH, './/div').text
		price = driver.find_element(By.CLASS_NAME, 'Listing-price').text.strip('€ ').replace(',', '.')
		if price.isnumeric():
			self._price = float(price)
		elif price == 'Bieden':
			self._price = 0.0
			self._bidding = True
		self._bids = self._getBids(driver)
		sroot = driver.find_element(By.CLASS_NAME, 'Stats-root')
		date = sroot.find_element(By.XPATH, './span[3]/span').text
		self._date = mpAdDateToDateTime(date)
		
		
	def _getBids(self, driver: webdriver.Chrome) -> list[MpBid]:
		bids = []
		if self._bidding:
			try:
				bidCont = driver.find_element(By.CLASS_NAME, 'BiddingList-container')
			except:
				print('bidding enabled but no bids found')
				return [] # no bids found
			
			# continue if bids are found
			for bid in bidCont.find_elements(By.XPATH, './div'):
				name = bid.find_element(By.XPATH, './div[1]').text
				amount = bid.find_element(By.XPATH, './div[2]').text.strip('€ ').replace(',', '.')
				date = mpBidDateToDateTime(bid.find_element(By.XPATH, './div[3]').text)
				mpbid = MpBid(self, name, amount, date)
				bids.append(mpbid)
				print(mpbid)

		bids.sort(key=lambda x: x.date, reverse=True)
		print(bids)
		return bids

	
	def __eq__(self, other: object) -> bool:
		if not isinstance(other, MpAd):
			return False
		elif self._id == other._id:
			return True
		else:
			return False
		
	def __ne__(self, other: object) -> bool:
		return not self.__eq__(other)


	def __str__(self):
		return f'Marktplaats ad. Id: {self._id}, Name: {self._name}, Url: {self._url}'

	@property
	def url(self):
		return self._url
	
	@property
	def id(self):
		return self._id
	
	@property
	def name(self):
		return self._name
	
	@property
	def description(self):
		return self._description
	
	@property
	def price(self):
		return self._price
	
	@property
	def bidding(self):
		return self._bidding
	
	@property
	def bids(self):
		return self._bids
	
	@property
	def date(self):
		return self._date