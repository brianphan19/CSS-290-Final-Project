import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class Scrapper():
    def __init__(self) -> None:
        options = Options()
        options.headless = True  # Run in normal mode for debugging
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def get_unit_value(self, loc_lat: float, loc_lon: float):
        url = f'https://globalsolaratlas.info/map?s={loc_lat},{loc_lon}&m=site'
        self.driver.get(url)
        
        try:
            # Wait for the specific photovoltaic power output value
            unit_value = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.site-data__unit-value sg-unit-value sg-unit-value-inner'))
            ).text.strip()
            unit_label = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.site-data__unit-label span.mat-menu-trigger'))
            ).text.strip()
            return unit_value, unit_label
        except Exception as e:
            self.driver.save_screenshot('error_screenshot.png')
            print(f"Error fetching data for coordinates ({loc_lat}, {loc_lon}): {e}")
            return 'Error', str(e)

    def close(self):
        self.driver.quit()

def fetch_data(latitude, longitude, results, index):
    scrapper = Scrapper()
    unit_value, unit_label = scrapper.get_unit_value(latitude, longitude)
    scrapper.close()
    results[index] = (latitude, longitude, unit_value, unit_label)

def main() -> None:
    coordinates = [
        (24.846565, -102.480469),
        (34.052235, -118.243683),
        (51.507222, -0.1275),
        (35.689487, 139.691711),
        (-33.865143, 151.209900)
    ]

    results = [None] * len(coordinates)
    threads = []

    for i, (latitude, longitude) in enumerate(coordinates):
        thread = threading.Thread(target=fetch_data, args=(latitude, longitude, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    for result in results:
        print(result)

if __name__ == '__main__':
    main()