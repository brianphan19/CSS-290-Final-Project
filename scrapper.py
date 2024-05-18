from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class Scrapper():
    def __init__(self) -> None:
        options = Options()
        options.headless = True  # Run in headless mode (no GUI)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def get_unit_value(self, loc_lat:float, loc_lon:float):
        url:str = f'https://globalsolaratlas.info/map?c=11.609193,8.261719,3&s={loc_lat},{loc_lon}&m=site'
        self.driver.get(url)
        self.driver.implicitly_wait(10) 

        unit_value = self.driver.find_element(By.CSS_SELECTOR, '.site-data__unit-value sg-unit-value-inner').text.strip()
        unit_label = self.driver.find_element(By.CSS_SELECTOR, '.site-data__unit-label .mat-menu-trigger span').text.strip()

        self.driver.quit()
        return unit_value, unit_label

scrap = Scrapper()

latitude:float = 24.846565
longtitude:float =  -102.480469
print(scrap.get_unit_value(latitude, longtitude))