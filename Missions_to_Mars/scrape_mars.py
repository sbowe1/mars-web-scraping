import pandas as pd
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser

def scrape():
    # Set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    # Visit url
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Scrape into BeautifulSoup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Queries
    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()


    # JPL Featured Image
    # Visit url
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Scrape into BeautifulSoup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Query
    featured_image_url = url + soup.find('img', class_='headerimage fade-in')['src']


    # Mars Facts
    url = 'https://galaxyfacts-mars.com/'

    # Read tabes from HTML
    tables = pd.read_html(url)
    mars_facts = tables[1]
    mars_facts = mars_facts.rename(columns={0: 'Description', 1: 'Value'})
    mars_facts.set_index('Description', inplace=True)
    mars_facts_html = mars_facts.to_html().replace('\n', '')

    # Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere_image_urls = []

    # Hemispheres as item elements
    mars_items = soup.find_all('div', class_='item')

    # Looping through each hemisphere item
    for x in mars_items:
        try:
            hemisphere = x.find('div', class_='description')
            title = hemisphere.h3.text.rsplit(' ', 1)[0]

            new_url = hemisphere.a['href']
            browser.visit(url+new_url)

            html = browser.html
            soup = bs(html, 'html.parser')

            # Obtaining the first image url
            img_url = url + soup.find('li').a['href']

            dict = {
                'title': title,
                'img_url': img_url
            }

            hemisphere_image_urls.append(dict)

        except Exception as e:
            print(e)

    browser.quit()

    # Compiling all results into a single dictionary
    mars_data = {
        'News Title': news_title,
        'News Paragraph Text': news_p,
        'Featured Image URL': featured_image_url,
        'Mars Facts': mars_facts_html,
        'Hemisphere Images': hemisphere_image_urls
    }

    return mars_data