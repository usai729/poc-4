import requests
from bs4 import BeautifulSoup
import time
import csv

url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"
user_agents = [
    # Windows Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
    
    # Windows Edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48',
    
    # Windows Firefox
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    
    # Windows Opera
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.277',
    
    # macOS Chrome
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    
    # macOS Safari
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    
    # macOS Firefox
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0',
    
    # Linux Chrome
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    
    # Android Chrome
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36',
    
    # iPhone Safari
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
]

#Create a data file and write the initial rows
with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(['Product Name', 'Price', 'Rating', 'Seller Name'])

#Loop through the user agents and get the data
for user_agent in user_agents:
    headers = {
        'User-Agent': user_agent
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)

    #Check if response status code is 200 - OK
    if response.status_code == 200:
        workingAgent = user_agent

        #Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='s-result-item') #Find all result elements

        #Iterate through results
        for item in items:
            #Get details of each product
            
            #Name
            product_name_elem = item.find("span", class_="a-size-base-plus a-color-base a-text-normal")
            if product_name_elem:
                product_name = product_name_elem.text.strip()
            else:
                continue

            #price
            price_elem = item.find("span", class_="a-price")
            if price_elem:
                price = price_elem.find("span", class_="a-offscreen").text.strip()
            else:
                continue

            #rating
            rating_elem = item.find("span", class_="a-icon-alt")
            if rating_elem:
                rating = rating_elem.text.strip()
            else:
                continue

            #seller name (not mentioned on results page)
            seller_name_elem = item.find("span", class_="a-size-base")
            if seller_name_elem:
                seller_name = seller_name_elem.text.strip()
            else:
                continue

            #Write details to the csv file
            with open('data.csv', "a", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                writer.writerow([product_name, price, rating, seller_name])

            print("Product Name:", product_name)
            print("Price:", price)
            print("Rating:", rating)
            print("Seller Name:", seller_name)
            
            print()

        break
    
    #Delay to avoid detection by amazon as scraper
    time.sleep(5)  