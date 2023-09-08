# Python functions to be able to extract documentation from websites
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urlparse
import os
import html2text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define root domain to crawl
domain = "docs.temporal.io/dev-guide/java"
full_url = "https://docs.temporal.io/dev-guide/java"

# Set up the selenium driver
options = webdriver.ChromeOptions()
options.headless = True  # to run chrome in headless mode
driver = webdriver.Chrome(options=options)

driver.get(full_url)

def crawl(url):
    # Parse the URL and get the domain
    local_domain = urlparse(url).netloc

    # Create a queue to store the URLs to crawl
    queue = deque([url])

    # Create a set to store the URLs that have already been seen (no duplicates)
    seen = set([url])

    # Create a directory to store the text files
    if not os.path.exists("text/"):
            os.mkdir("text/")

    # Convert local_domain to a acceptable directory name, switching out periods for underscores
    # and slashes for underscores
    if not os.path.exists("text/"+local_domain+"/"):
            os.mkdir("text/" + local_domain + "/")

    # Create a directory to store the csv files
    if not os.path.exists("processed"):
            os.mkdir("processed")

    # While the queue is not empty, continue crawling
    while queue:

        # Get the next URL from the queue
        url = queue.pop()
        print(url) # for debugging and to see the progress

        try:
            # Wait up to 10 seconds till the element is visible
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.theme-doc-markdown.markdown"))
            )

            # Once it's loaded, parse it with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            div_content = soup.select_one('div.theme-doc-markdown.markdown')
            

            if div_content:
                # Extract all the text from within the div
                text_content = div_content.get_text()
                # print(text_content.strip())
                # convert the html to markdown
                # markdown = markdownify.markdownify(text_content)
                # print(markdown)
                # Convert HTML to Markdown
                text_maker = html2text.HTML2Text()
                text_maker.ignore_links = False
                markdown_content = text_maker.handle(div_content.prettify())
                # save to a file
                with open('text/'+local_domain+'/'+url[8:].replace("/", "_") + ".md", "w", encoding="UTF-8") as f:
                    f.write(markdown_content)
                
            else:
                print("Couldn't find the div.")

        finally:
            driver.quit()  # always quit the driver

crawl(full_url)