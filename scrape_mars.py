from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()

    mars_data = {}

    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = bs(response.text, "html.parser")

    results = soup.find_all("div", class_="content_title")

    news_titles = []
    
    for result in results:
        if (result.a):
            if (result.a.text):
                news_titles.append(result)
    
    end_titles = []
    for x in range(6):
        var=news_titles[x].text
        newvar = var.strip("\n\n")
        end_titles.append(newvar)

    presults = soup.find_all("div", class_="rollover_description_inner")

    news_paragraph = []
    for x in range(6):
        var=presults[x].text
        newvar = var.strip("\n\n")
        news_paragraph.append(newvar)
    
    
    mars_data["news_titles"] = end_titles
    mars_data["news_paragraph"] = news_paragraph



   
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html=browser.html
    soup = bs(html, "html.parser")

    
    footer = soup.find("footer")
    link = footer.find("a")
    fornext = link["data-link"]

   
    base_url="https://www.jpl.nasa.gov"
    clicknext = base_url+fornext
    browser.visit(clicknext)

    html=browser.html
    soup = bs(html, "html.parser")

   
    full_fig = soup.find("figure",class_="lede")
    link = full_fig.find("a")
    featured_image = link["href"]

    featured_image_url = base_url+featured_image

    
    mars_data["featured_image_url"] = featured_image_url

   
	#Mars Facts
    url = "https://space-facts.com/mars/"
    response = requests.get(url)
    soup = bs(response.text, "html.parser")

    tables = pd.read_html(url)
    mars_df = mars_facts[0]
    
    mars_df.columns = ["Mars", "Facts"]
    s = pd.Series(mars_df["Mars"])
    mars_df["Mars"] = s.str.strip(':')
    mars_df = mars_df.set_index("Mars")

    table_html = mars_df.to_html()

    mars_data["mars_table"] = mars_table


  
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    next_page_urls = []
    img_titles = []
    base_url = "https://astrogeology.usgs.gov"

    
    html = browser.html
    soup = bs(html, "html.parser")
    divs = soup.find_all("div", class_="description")

    counter = 0
    for div in divs:
        link = div.find("a")
        href=link["href"]
        img_title = div.a.find("h3")
        img_title = img_title.text
        img_titles.append(img_title)
        next_page = base_url + href
        next_page_urls.append(next_page)
        counter = counter+1
        if (counter == 4):
            break

    hi_rez_images=[]
    for next_page_url in next_page_urls:
        url = next_page_url
        browser.visit(url)
        html = browser.html
        soup = bs(html, "html.parser")
        link2 = soup.find("img", class_="wide-image")
        for_final = link2["src"]
        full_img = base_url + for_final
        hi_rez_images.append(full_img)
        next_page_urls = []
    
    hemisphere_image_urls = []

    cerberus = {"title":img_titles[0], "img_url": hi_rez_images[0]}
    schiaparelli = {"title":img_titles[1], "img_url": hi_rez_images[1]}
    syrtis = {"title":img_titles[2], "img_url": hi_rez_images[2]}
    valles = {"title":img_titles[3], "img_url": hi_rez_images[3]}

    hemisphere_image_urls = [cerberus, schiaparelli, syrtis, valles]

    #adding to dict
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_data

if __name__ == "__main__":
    scrape()