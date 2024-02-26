# Copyright (c) 2024 Timo Oosterom (timo@ntdev-technology.nl)

from selenium.webdriver.common.by import By 
from selenium.webdriver.remote.webelement import WebElement # only used for type hinting
from selenium import webdriver # only used for type hinting
from datetime import datetime



class XpathElementLoaded(object):
    
    def __init__(self, xpath: str, parent_element: WebElement = None) -> None:
        """
        This class is used to wait for an element to be loaded in the DOM.
        Using xpath to find the element.

        Args:
            xpath (str): The xpath of the element to wait for.
            parent_element (WebElement): The parent element of the element to wait for. If None, the element will be searched for in the entire document.
        """
        self._xpath = xpath
        self._parent_element = parent_element


    def __call__(self, driver: webdriver.Chrome) -> WebElement | None:
        """
        This is the method that is called when we use the WebDriverWait object.
        
        Args:
            driver: The WebDriver object.
        
        Returns:
            WebElement: if a WebElement with specified xpath is found.
            None: if no WebElement with specified xpath is found.
        """
        if self._parent_element:
            elem = self._parent_element.find_element(By.XPATH, self._xpath)
        else:
            elem = driver.find_element(By.XPATH, self._xpath)

        if elem:
            return elem
        else:
            return False
        

DutchToEnglishMonth = {
    'jan': 'Jan',
    'feb': 'Feb',
    'mrt': 'Mar',
    'apr': 'Apr',
    'mei': 'May',
    'jun': 'Jun',
    'jul': 'Jul',
    'aug': 'Aug',
    'sep': 'Sep',
    'okt': 'Oct',
    'nov': 'Nov',
    'dec': 'Dec'
}


def mpAdDateToDateTime(mpDate: str) -> datetime:
    for dutch_month, english_month in DutchToEnglishMonth.items():
        mpDate = mpDate.replace(dutch_month, english_month)
    mpDate = mpDate.replace("'", "20")
    return datetime.strptime(mpDate, "sinds %d %b. %Y, %H:%M")

def mpBidDateToDateTime(mpDate: str) -> datetime:
    for dutch_month, english_month in DutchToEnglishMonth.items():
        mpDate = mpDate.replace(dutch_month, english_month)
    mpDate = mpDate.replace("'", "20")
    return datetime.strptime(mpDate, "%d %b. %Y")