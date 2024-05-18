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

        return unit_value, unit_label
    
    def get_temperature(self, loc_lat: float, loc_lon: float):
        url: str = f'https://globalsolaratlas.info/map?c=11.609193,8.261719,3&s={loc_lat},{loc_lon}&m=site'
        self.driver.get(url)
        self.driver.implicitly_wait(10)

        temperature_value = self.driver.find_element(By.XPATH, "//div[contains(@class, 'site-data__layer-name') and contains(., 'TEMP')]/following-sibling::div[contains(@class, 'site-data__unit-value')]//sg-unit-value-inner").text.strip()
        return temperature_value
    
    def get_values(self, loc_lat: float, loc_lon: float):
        url: str = f'https://globalsolaratlas.info/map?c=11.609193,8.261719,3&s={loc_lat},{loc_lon}&m=site'
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        
        unit_value = self.driver.find_element(By.CSS_SELECTOR, '.site-data__unit-value sg-unit-value-inner').text.strip()
        temperature_value = self.driver.find_element(By.XPATH, "//div[contains(@class, 'site-data__layer-name') and contains(., 'TEMP')]/following-sibling::div[contains(@class, 'site-data__unit-value')]//sg-unit-value-inner").text.strip()
        
        return unit_value, temperature_value
    
    def close(self):
        self.driver.quit()

def main() -> None:
    scrap = Scrapper()
    coordinates = [
        (24.846565, -102.480469),
        (34.052235, -118.243683),
        (51.507222, -0.1275),
        (35.689487, 139.691711),
        (-33.865143, 151.209900)
    ]

    results = []
    for latitude, longitude in coordinates:
        try:
            unit_value, unit_label = scrap.get_unit_value(latitude, longitude)
            temperature_value, temperature_label = scrap.get_temperature(latitude, longitude)
            results.append((latitude, longitude, unit_value, unit_label, temperature_value, temperature_label))
        except Exception as e:
            results.append((latitude, longitude, 'Error', str(e), 'Error', str(e)))

    scrap.close()

    for result in results:
        print(result)

    scrap.close()
if __name__ == '__main__':
    main()