from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import threading

class Scrapper():
    def __init__(self) -> None:
        options = Options()
        options.headless = True  # Run in headless mode (no GUI)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def get_unit_value(self, loc_lat: float, loc_lon: float):
        url: str = f'https://globalsolaratlas.info/map?c=11.609193,8.261719,3&s={loc_lat},{loc_lon}&m=site'
        self.driver.get(url)
        self.driver.implicitly_wait(5)  # Reduced wait time

        try:
            unit_value = self.driver.find_element(By.CSS_SELECTOR, '.site-data__unit-value sg-unit-value-inner').text.strip()
            unit_label = self.driver.find_element(By.CSS_SELECTOR, '.site-data__unit-label .mat-menu-trigger span').text.strip()
            return unit_value, unit_label
        except Exception as e:
            return 'Error', str(e)

    def close(self):
        self.driver.quit()

def fetch_data(scrapper, latitude, longitude, results, index):
    unit_value, unit_label = scrapper.get_unit_value(latitude, longitude)
    results[index] = (latitude, longitude, unit_value, unit_label)

def main() -> None:
    start = time.time()
    coordinates = [
        (24.846565, -102.480469),
        (34.052235, -118.243683),
        (51.507222, -0.1275),
        (35.689487, 139.691711),
        (-33.865143, 151.209900)
    ]

    scrap = Scrapper()
    results = [None] * len(coordinates)
    threads = []

    for i, (latitude, longitude) in enumerate(coordinates):
        thread = threading.Thread(target=fetch_data, args=(scrap, latitude, longitude, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    scrap.close()

    for result in results:
        print(result)

if __name__ == '__main__':
    main()
