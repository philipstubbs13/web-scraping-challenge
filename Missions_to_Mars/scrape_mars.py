# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
  browser = init_browser()

  # NASA Mars News
  # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest) and collect the latest news title and paragraph text.
  # Assign the text to variables to reference later.

  # Visit the NASA Mars News Site.
  url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
  browser.visit(url)

  time.sleep(1)

  # Scrape page into soup.
  html = browser.html
  soup = bs(html, "html.parser")

  # Get latest news title and paragraph text.
  news_title = soup.find_all('div', class_='content_title')[0].text
  news_p = soup.find_all('div', class_="article_teaser_body")[0].text
  print(f"Latest news title: {news_title}.")
  print(f"Latest news paragraph text: {news_p}")


  # JPL Mars Space Images - Featured Image
  # Use splinter to navigate the site and find the image url for the current featured Mars image.
  # Assign the url string to a variable called featured_image_url.
  # Make sure to find the image url to the full size .jpg image.
  # Make sure to save a complete url string for this image.

  # Visit the url for JPL Featured Space Image.
  url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
  browser.visit(url)

  time.sleep(1)

  # Scrape page into soup.
  html = browser.html
  soup = bs(html, "html.parser")

  # Get image url for featured image.
  featured_image_base_url = "https://www.jpl.nasa.gov"
  featured_image_url_style = soup.find('article', class_="carousel_item")["style"]
  url_list = featured_image_url_style.split("'")
  featured_image_relative_path = url_list[1]
  featured_image_url = featured_image_base_url + featured_image_relative_path
  print(f"Featured image url: {featured_image_url}")


  # Mars Weather
  # Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.

  url = "https://twitter.com/marswxreport?lang=en"
  browser.visit(url)

  time.sleep(8)

  # Scrape page into soup.
  html = browser.html
  soup = bs(html, "html.parser")

  # Get latest Mars weather tweet.
  mars_weather_tweet = soup.find(attrs={"data-testid" : "tweet"})
  mars_weather_tweet_text = mars_weather_tweet.text

  mars_weather_list = mars_weather_tweet_text.split("InSight")
  mars_weather = mars_weather_list[1]

  print(f"Latest Mars weather tweet: {mars_weather}")


  # Mars Facts
  # Visit the Mars Facts webpage [here](https://space-facts.com/mars/).
  # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
  # Use Pandas to convert the data to a HTML table string.

  # Visit url for mars facts.
  url = "https://space-facts.com/mars/"
  browser.visit(url)

  time.sleep(1)

  # Scrape page into soup.
  html = browser.html
  soup = bs(html, "html.parser")

  # Get Mars facts table using pandas.
  tables = pd.read_html(url)
  tables

  # Convert table for site to pandas dataframe.
  df = tables[0]
  df.columns = ["Measurement", "Value"]
  df.set_index("Measurement", inplace=True)
  df.head()

  # Convert pandas dataframe to a html string.
  html_table = df.to_html()
  html_table

  # Remove any new line characters from the html string.
  html_table.replace('\n', '')

  # Save the html string to a file.
  df.to_html('mars_facts_table.html')


  # Mars Hemispheres
  # Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
  # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
  # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
  # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

  # Visit url for images of Mar's hemispheres.
  base_url = "https://astrogeology.usgs.gov"
  hemisphere_list_url = base_url + "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
  browser.visit(hemisphere_list_url)

  time.sleep(1)

  # Scrape page into soup.
  html = browser.html
  soup = bs(html, "html.parser")

  # Get hemisphere name and image url for the full resolution image.
  hemispheres = soup.find_all('div', class_='item')
  hemisphere_image_urls = []

  for hemisphere in hemispheres:
      link_text = hemisphere.find('h3').text
      splitted = link_text.split('Enhanced')
      title = splitted[0]
      browser.click_link_by_partial_text(link_text)
      hemisphere_page_html = browser.html
      soup = bs(hemisphere_page_html, "html.parser")
      downloads = soup.find('div', class_="downloads")
      img_url = downloads.a["href"]
      hemisphere_dict = { "title": title, "img_url": img_url }
      hemisphere_image_urls.append(hemisphere_dict)
      browser.back()
      
  print(hemisphere_image_urls)

  scraped_data = {
    "news_title": news_title,
    "news_p": news_p,
    "hemisphere_image_urls": hemisphere_image_urls,
    "html_table": html_table,
    "mars_weather": mars_weather,
    "featured_image_url": featured_image_url
  }
  print(scraped_data)
  return scraped_data

