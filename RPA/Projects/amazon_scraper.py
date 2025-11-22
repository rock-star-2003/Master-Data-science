# import requests
# from bs4 import BeautifulSoup
# import time # Added for an essential pause

# HEADERS = { 
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#     'Accept-Language': 'en-US, en;q=0.5',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Connection': 'keep-alive',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# }


# link = "https://amzn.in/d/auEZxWh"



# def scrap_data(link):
#     try:
#         responce = requests.get(link,headers=HEADERS, timeout= 10)
#         time.sleep(2)
#         responce.raise_for_status() # Check for bad status codes (4xx or 5xx)

#         html_scrap = BeautifulSoup(responce.content, "html.parser")

#         product_details = html_scrap.find("div",{"id":'ppd'})

#         def clean_data(data):
#             if data:
#                 data = data.get_text(strip = True)
#                 return data
#             else:
#                 return '❌ no data found........'
        
#         def find_data(tag_name,attributes_dict):
#             return clean_data( product_details.find(tag_name,attributes_dict))
        
#         product_title = find_data('span',{'id':'productTitle'})
#         brand_name = product_title.split()[0]
#         current_price = int(''.join(filter(str.isdigit,find_data('span',{'class':'priceToPay'}))))
#         list_price = find_data('span',{'class':'basisPrice'})

#         print({
#             "ProductTitle" : product_title,
#             "BrandName" : brand_name,
#             "CurrentPrice" : current_price,
#             "ListPrice" : list_price,
#         })

#     except requests.exceptions.RequestException as e:
#         print(f"❌ Request Error: {e}")
#         print("This often means Amazon detected the bot and blocked the request.")
#     except Exception as e:
#         print(f"❌ General Error: {e}")


# scrap_data(link)

# import requests
# from bs4 import BeautifulSoup
# import time 
# import random # Import for adding random delay

# import random

# USER_AGENT_LIST = [
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
#     'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.93 Mobile Safari/537.36',
# ]

# # Function to get randomized headers
# def get_random_headers():
#     return {
#         'User-Agent': random.choice(USER_AGENT_LIST),
#         'Accept-Language': 'en-US, en;q=0.5',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     }

# links = [
#     'https://amzn.in/d/auEZxWh',
# 'https://dl.flipkart.com/s/Hfn3wIuuuN',
# 'https://amzn.in/d/8ROjVGv',
# 'https://dl.flipkart.com/s/rErkQqNNNN',
# 'https://amzn.in/d/4l7qK8y',
# 'https://dl.flipkart.com/s/Hl34XHuuuN'

# ]

# def find_data(parent_element, tag_name, attributes_dict):
#     """Helper function to find and clean data, handling NoneType."""
#     if not parent_element:
#         return '❌ Parent element not found'
    
#     data = parent_element.find(tag_name, attributes_dict)
    
#     if data:
#         return data.get_text(strip=True)
#     else:
#         return '❌ no data found........'

# def scrap_data(link):
#     # --- 1. Retry Loop ---
#     MAX_RETRIES = 3
#     for attempt in range(MAX_RETRIES):
#         try:
#             # Add a random, human-like delay between requests
#             delay = random.uniform(5, 15) # Wait between 5 and 15 seconds
#             print(f"Attempt {attempt + 1}/{MAX_RETRIES}: Waiting {delay:.2f} seconds...")
#             time.sleep(delay)
            
            


#             # --- 2. Make Request ---
#             session = requests.session()
#             session.headers.update(get_random_headers())
#             response = session.get(link)

#             # response = requests.get(link, headers=HEADERS, timeout=20)
#             response.raise_for_status()

#             # --- 3. Check for Captcha/Block Page (Crucial Step) ---
#             if "captcha" in response.text.lower() or "apology" in response.text.lower():
#                 print("⚠️ Block detected! Amazon served a CAPTCHA or block page.")
#                 if attempt < MAX_RETRIES - 1:
#                     print("Retrying with a longer delay...")
#                     continue
#                 else:
#                     return {"Error": "Blocked by Amazon after max retries."}

#             # --- 4. Parse HTML ---
#             html_scrap = BeautifulSoup(response.content, "html.parser")

#             # --- 5. Find the Parent Element (ppd) ---
#             product_details = html_scrap.find("div", {"id": 'ppd'})
            
#             # --- 6. GRACEFUL EXIT: Check if the parent element was found ---
#             if not product_details:
#                 # If ppd is missing, the page is likely a block or redirect.
#                 print("❌ Parent container (div#ppd) not found. Retrying...")
#                 if attempt < MAX_RETRIES - 1:
#                     continue
#                 else:
#                     return {"Error": "Failed to find product container after max retries."}

#             # --- 7. Extract Data using the Robust Helper ---
#             product_title = find_data(product_details, 'span', {'id': 'productTitle'})
            
#             # Note: Using the reliable 'a-price-whole' is better than 'priceToPay' for requests
#             current_price_str = find_data(product_details, 'span', {'class': 'a-price-whole'})
#             list_price = find_data(product_details, 'span', {'class': 'basisPrice'})

#             # --- Data Cleaning ---
#             brand_name = product_title.split()[0] if '❌' not in product_title else 'N/A'
#             current_price = int(''.join(filter(str.isdigit, current_price_str.replace(',', '').replace('.', '')))) if '❌' not in current_price_str else 'N/A'

#             # --- Success! Return the data ---
#             return {
#                 "ProductTitle": product_title,
#                 "BrandName": brand_name,
#                 "CurrentPrice": current_price,
#                 "ListPrice": list_price,
#             }

#         except requests.exceptions.RequestException as e:
#             print(f"❌ Request Error: {e}. Retrying...")
#             if attempt == MAX_RETRIES - 1:
#                 return {"Error": f"Request failed after max retries: {e}"}
#         except Exception as e:
#             # Catch any other error, like the one you saw.
#             print(f"❌ General Error: {e}. Retrying...")
#             if attempt == MAX_RETRIES - 1:
#                 return {"Error": f"Failed due to unexpected error after max retries: {e}"}
            
#     return {"Error": "Exited retry loop without success."}


# result = [scrap_data(link) for link in links]
# print("\n--- Final Result ---")
# print(result)

