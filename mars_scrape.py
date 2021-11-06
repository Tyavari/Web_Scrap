# Import Dependencies 

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup 

import pymongo

import requests

from splinter import Browser

import pandas as pd
    
    
def scrape_mars():


    #Chromedriver

    executable_path = {'executable_path': ChromeDriverManager().install()}

    browser = Browser('chrome', **executable_path, headless=False)

    # Begin News url scrape

    news_url = 'https://redplanetscience.com'

    browser.visit(news_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Find most recent article 
    results = soup.find_all('div',class_="list_text")

    news_title = results[0].find('div',class_='content_title').text

    news_p = results[0].find('div',class_='article_teaser_body').text

    print(news_title)
    print('----')
    print(news_p)
    
    # Begin jpl scrape

    jpl_url = 'https://spaceimages-mars.com'

    browser.visit(jpl_url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')
    # Get image url 
    jpl_scrape_url = 'https://spaceimages-mars.com/'

    img_url = soup.find_all('a',class_='showimg fancybox-thumbs')[0]['href']

    featured_url = jpl_scrape_url+img_url

    print(featured_url)


    #Galaxy facts scrape
    galaxy_facts_url = 'https://galaxyfacts-mars.com'

    mars_info = pd.read_html(galaxy_facts_url)

    planet_profile = mars_info[1]

    mars_html = planet_profile.to_html(index=False, header=False)


    # Mars Hemispheres Scrape.

    mars_hemi_url = 'https://marshemispheres.com/'

    browser.visit(mars_hemi_url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')
    #find urls and createw empty list to hold them
    
    hemi_url = soup.find_all('div', class_='description')
    
    hemi_images = []
    hemi_names = ["Ceberus", "Schiaparelli", "Syrtis Major", "Valles Marineris"]
   
    for hemi_urls in hemi_url:
    
        hemi_page = hemi_urls.find('a', class_='itemLink')['href']
    
        hemi_page = f'{mars_hemi_url}{hemi_page}'

        hemi_response = requests.get(hemi_page)
    
        soup2 = BeautifulSoup(hemi_response.text, 'lxml')
    
        hemi_img_soup = soup2.find_all('li')[0]
    
        hemi_img = hemi_img_soup.find('a')['href']
    
        hemi_img = f'{mars_hemi_url}{hemi_img}'
    
        hemi_images.append(hemi_img)
    
    hemisphere_image_urls = [
    {"title": "Cerberus", "img_url": hemi_images[0]},
    {"title": "Schiaparelli", "img_url": hemi_images[1]},
    {"title": "Syrtis Major", "img_url": hemi_images[2]},
    {"title": "Valles Marineris", "img_url": hemi_images[3]}
]
    hemisphere_image_urls
    
    mars_dict = {
    "article_title": news_title,
    "article_teaser": news_p,
    "image": featured_url,
    "table": mars_html,
    "hemisphere_names": hemi_names,
    "hemispheres_dict":hemisphere_image_urls
    
    }

    browser.quit()
    return mars_dict
    
    
    
    
    
    


