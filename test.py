from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure Selenium WebDriver with WebDriver Manager
options = Options()
options.headless = True  # Run in headless mode (no GUI)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)



def get_unit(driver, lat, lon):
    url = f'https://globalsolaratlas.info/map?c=11.609193,8.261719,3&s={lat},{lon}&m=site'
    driver.get(url)

    # Wait for the content to load and extract data
    driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to become available
    unit_value = driver.find_element(By.CSS_SELECTOR, '.site-data__unit-value sg-unit-value-inner').text.strip()
    driver.quit()
    return unit_value

# URL of the webpage to scrape
# url = f'https://globalsolaratlas.info/map?c=11.609193,8.261719,3&s={lat},{lon}&m=site'
# driver.get(url)

# # Wait for the content to load and extract data
# driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to become available

# # Extract data using Selenium
# layer_full_name = driver.find_element(By.CSS_SELECTOR, '.site-data__layer-full-name p').text
# layer_name = driver.find_element(By.CSS_SELECTOR, '.site-data__layer-name gsa-site-data-key').text.strip()
# unit_value = driver.find_element(By.CSS_SELECTOR, '.site-data__unit-value sg-unit-value-inner').text.strip()
# unit_label = driver.find_element(By.CSS_SELECTOR, '.site-data__unit-label .mat-menu-trigger span').text.strip()

# # Print the extracted data
# print(f"Layer Full Name: {layer_full_name}")
# print(f"Layer Name: {layer_name}")
# print(f"Unit Value: {unit_value}")
# print(f"Unit Label: {unit_label}")
# # Close the browser
# driver.quit()

lat = 24.846565
lon =  -102.480469
print(get_unit(driver, lat, lon))


