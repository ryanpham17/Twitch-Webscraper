from parsel import Selector # type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up options for headless mode and window size
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
options.add_argument("start-maximized")

# Initialize Chrome options to block images
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)
driver.get("https://www.twitch.tv/directory/game/Art")

# Wait until it the driver loads
element = WebDriverWait(driver = driver, timeout = 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-target="directory-first-item"]'))
)

# Get the page source and parse with Parsel
sel = Selector(text=driver.page_source)
parsed = []

# Loop over the elements and extract the required data
for item in sel.xpath("//div[contains(@class,'tw-tower')]/div[@data-target]"):
    parsed.append({
        'title': item.css('h3::text').get(),
        'url': item.css('.tw-link::attr(href)').get(),
        'username': item.css('.tw-link::text').get(),
        'tags': item.css('.tw-tag ::text').getall(),
        'viewers': ''.join(item.css('.tw-media-card-stat::text').re(r'(\d+)')),
    })

# Print the parsed data
for entry in parsed:
    print(entry)
driver.quit()
