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

    def get_unit_value(self, lat, lon):
        url = f'https://globalsolaratlas.info/map?c=11.609193,8.261719,3&s={lat},{lon}&m=site'
        self.driver.get(url)
        self.driver.implicitly_wait(10) 

        # Assuming the CSS selector is corrected as needed
        layer_full_name = driver.find_element(By.CSS_SELECTOR, '.site-data__layer-full-name p').text
        layer_name = driver.find_element(By.CSS_SELECTOR, '.site-data__layer-name gsa-site-data-key').text.strip()
        unit_value = driver.find_element(By.CSS_SELECTOR, '.site-data__unit-value sg-unit-value-inner').text.strip()
        unit_label = driver.find_element(By.CSS_SELECTOR, '.site-data__unit-label .mat-menu-trigger span').text.strip()

        print(f"Layer Full Name: {layer_full_name}")
        print(f"Layer Name: {layer_name}")
        print(f"Unit Value: {unit_value}")
        print(f"Unit Label: {unit_label}")

        self.driver.quit()
        return unit_value

# scrap = Scrapper()

# scrap.get_unit_value(lat, lon)