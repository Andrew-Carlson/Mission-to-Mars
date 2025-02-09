# import dependencies

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up and create an instance of splinter (prep automated browser and specify that it is chrome)
executable_path = {'executable_path': ChromeDriverManager().install()}

# **executable_path is unpacking the dictionary we've stored the path in
# headless=False means that all of the browser's actions will be displayed in a Chrome window so we can see them.
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'

browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1) 

# more info: https://splinter.readthedocs.io/en/latest/matchers.html
# the .is_element_present_by_css function checks for certain elements that are argued
# div.list_text is the html tag and class for the article titles on the webpage 

#  returns True since element is present

# You can use the html attribute to get the html content of the visited page
# create an HTML object and parse with bs4
html = browser.html

news_soup = soup(html, 'html.parser')

# assigned slide_elem as the variable to look for the <div /> tag 
# and its descendent (the other tags within the <div /> element)
slide_elem = news_soup.select_one('div.list_text') # select_one() finds only the first tag that matches a selector

# the period is used for assigning classes in div.list_text

slide_elem

# find the title of the article in the div tag of class list_text
# The output should be the HTML containing the content title and anything else nested inside of that <div />.
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_= 'content_title').get_text()

news_title

# There are two methods used to find tags and attributes with BeautifulSoup:
# .find() is used when we want only the first class and attribute we've specified.
# .find_all() is used when we want to retrieve all of the tags and attributes.

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

news_p


# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button on the webpage
full_image_elem = browser.find_by_tag('button')[1]

full_image_elem.click()

# Parse the resulting html with soup 
html = browser.html

img_soup = soup(html, 'html.parser')

img_soup

# Find the relative image url
img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')

img_url_rel

# create an absolute url that works. The above url is only partial
img_url = f'https://spaceimages-mars.com/{img_url_rel}'

img_url

# We're using an f-string for this print statement because it's a cleaner way to create print statements; 
# they're also evaluated at run-time. This means that it, 
# and the variable it holds, doesn't exist until the code is executed and the values are not constant. 
# This works well for our scraping app because the data we're scraping is live and will be updated frequently.


# ### Scrape facts table using Pandas

# use pandas read_html() function to return a list of all the tables present  in the html code of the website.
# using the index [0] will return the first table found in the html. 

df = pd.read_html('https://galaxyfacts-mars.com/')[0]

# create column names for df
df.columns=['description', 'Mars', 'Earth']

# .set_index() function, we're turning the Description column into the DataFrame's index. 
# inplace=True means that the updated index will remain in place without having to reassign the DataFrame to a new variable.
df.set_index('description', inplace = True)

# use pandas to convert dataframe into its html code:
df.to_html()

# notice that it is an html table element with the tag <table /> along with many nested elements
# the dataframe can be put into a web application since it is made up of this html code

# Live sites are a great resource for fresh data, but the layout of the site may be updated or otherwise changed. 
# When this happens it's likely the scraping code will break and need to be reviewed and updated to be used again.
# For example, an image may suddenly become embedded within an inaccessible block of code because the developers 
# switched to a new JavaScript library. 
# It's not uncommon to revise code to find workarounds or even look for a different, scraping-friendly site all together.


# ### Deliverable 1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# Use Browser to visit URL
url = 'https://marshemispheres.com/'

browser.visit(url)

# create a list to store all Mars hemisphere image urls ant titles.
hemisphere_image_urls = []

# Write code to retrieve the image urls and titles for each hemisphere.
# Documentation: https://splinter.readthedocs.io/en/latest/elements-in-the-page.html
image_links =  browser.find_by_css('a.product-item img')
image_links

# get the count of image links on the webpage. This can therefore be iterated in a for loop
len(image_links)

# create for loop to access all images
for i in range(len(image_links)): # i will iterate over the items 0,1,2,and 3
    
    # create an empty dictionary to store image and title for each hemisphere
    hemispheres = {}
    
    # use find_by_css function and the click method to click the image on the webpage to get to the next link
    browser.find_by_css('a.product-item img')[i].click()
    
    # find sample image and extract 
    sample_elem = browser.find_by_text('Sample').first
    
    # Add to dictionary: the key img_url will have the value of the image URL which is sample_elem['href']
    hemispheres['img_url'] = sample_elem['href']
    
    # Add to dictionary: they key is the title and the key is the 
    hemispheres["title"] = browser.find_by_css('h2.title').text
    
    # append each dictionary made for each image url and title to the hemisphere_image_urls list made.
    hemisphere_image_urls.append(hemispheres)
    
    # we need to navigate to the start page so that the following error does not occur;
    # ElementDoesNotExist: no elements could be found with css "a.product-item img"
    
    browser.back()

# Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# end the automated browsing session.
# this is very important because the automated browser would otherwise not know when to shutdown
# the browser will therefore continure to listen for instructions and this can put a strain on the computer's memory or battery.
browser.quit()

