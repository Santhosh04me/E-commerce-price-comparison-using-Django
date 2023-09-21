from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup

def scrape_flipkart(search_text):
    flipkart_url = f"https://www.flipkart.com/search?q={search_text.replace(' ', '%20')}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    flipkart_response = requests.get(flipkart_url)
    flipkart_soup = BeautifulSoup(flipkart_response.text, "html.parser")
    
    flipkart_results = flipkart_soup.find_all("div", class_="_4rR01T")

    scraped_results = []

    for i, result in enumerate(flipkart_results[:4], 1):
        title = result.text.strip()
        price = flipkart_soup.find_all("div", class_="_3tbKJL")[i - 1].text.strip()
        scraped_results.append(f"Flipkart Result {i}:\nTitle: {title}\nPrice: {price}\n")

    return scraped_results
  

def scrape_amazon(search_text):
    amazon_url = f"https://www.amazon.in/s?k={search_text.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

    amazon_response = requests.get(amazon_url, headers=headers)
    amazon_soup = BeautifulSoup(amazon_response.text, "html.parser")
    
    amazon_results = amazon_soup.find_all("div", class_="s-result-item")

    scraped_results = []

    for i, result in enumerate(amazon_results[:4], 1):
        title = result.find("span", class_="a-text-normal").text.strip()
        price = result.find("span", class_="a-price-whole").text.strip()
        scraped_results.append(f"Amazon Result {i}:\nTitle: {title}\n Price: {price}\n")

    return scraped_results,redirect('search_results/')

def search_results(request):
    search_text = request.GET.get('search_text', '')  # Get the search text from the form submission
    
    # Check if a search query was entered
    if search_text:
        # Scrape Flipkart and Amazon results
        flipkart_results = scrape_flipkart(search_text)
        amazon_results = scrape_amazon(search_text)
    else:
        # If no search query was entered, set the results to empty lists
        flipkart_results = []
        amazon_results = []
    
    # Render the HTML template with the scraped results and search query
    return render(request, 'price/ecom.html', {
        'flipkart_results': flipkart_results,
        'amazon_results': amazon_results,
        'search_text': search_text,  # Pass the search query back to the template
    })
