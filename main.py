from bs4 import BeautifulSoup
import requests
import csv

def data_scrape(web_url):
    print(f"Fetching data from: {web_url}")
    response = requests.get(web_url)

    if response.status_code == 200: 
        print("Successfully fetched the main page data.")
        html_data = BeautifulSoup(response.text, 'html.parser')

        # getting restaurant names & URLs
        restaurant_tags = html_data.find_all('a', class_="HomeFeedUICard-3e299003014c14f9")
        print(f"Found {len(restaurant_tags)} restaurants on the main page.")

        # extracting restaurant names & URLs
        top_restaurants = []
        for tag in restaurant_tags[:1]:  # limiting to top 10 restaurants under each cuisine + top offers
            restaurant_name_tag = tag.find('p', class_="ccl-649204f2a8e630fd ccl-a396bc55704a9c8a ccl-ff5caa8a6f2b96d0 ccl-40ad99f7b47f3781")
            if restaurant_name_tag:
                restaurant_name = restaurant_name_tag.get_text()  # getting restaurant name
                restaurant_url = "https://deliveroo.ae" + tag['href']  # getting restaurant's specific URL
                print(f"Restaurant found: {restaurant_name}")
                top_restaurants.append({'name': restaurant_name, 'url': restaurant_url})
      
        menu_items = []

        for restaurant in top_restaurants:
            print(f"Fetching menu for restaurant: {restaurant['name']}")
            restaurant_menu = []

            # making a request to each restaurant's menu page
            restaurant_response = requests.get(restaurant['url'])
            if restaurant_response.status_code == 200:
                print(f"Successfully fetched menu page for {restaurant['name']}")
                html_menu_data = BeautifulSoup(restaurant_response.text, 'html.parser')

                # finding all divs with the specific class for menu items
                menu_item_divs = html_menu_data.find_all('div', class_="MenuItemCard-03b1bfbfe7cb723c MenuItemCard-3217cba068edacdb")
                
                print(f"Found {len(menu_item_divs)} menu item sections for {restaurant['name']}")

                # iterating through each div & finding specific p tags for item names
                for div in menu_item_divs:
                    # finding item name within this div
                    item_name_tag = div.find('p', class_="ccl-649204f2a8e630fd ccl-a396bc55704a9c8a ccl-0956b2f88e605eb8 ccl-ff5caa8a6f2b96d0 ccl-40ad99f7b47f3781")
                    description_tag = div.find('span', class_="ccl-649204f2a8e630fd ccl-6f43f9bb8ff2d712 ccl-08c109442f3e666d")
                    price_tag = div.find('span', class_="ccl-649204f2a8e630fd ccl-6f43f9bb8ff2d712 ccl-32ec9a3197735a65 ccl-08c109442f3e666d")

                    if item_name_tag and description_tag and price_tag:
                        menu_item = {
                            "name": item_name_tag.get_text(),
                            "description": description_tag.get_text(),
                            "price": price_tag.get_text(),
                        }
                        restaurant_menu.append(menu_item)

            # appending the menu for the restaurant
            menu_items.append({
                "restaurant": restaurant,
                "menu": restaurant_menu
            })

        return top_restaurants, menu_items
    else:
        print(f"Failed to fetch data from {web_url}. Status code: {response.status_code}")
        return [], []


def write_to_csv(data, filename):
    print(f"Writing data to CSV file: {filename}")
    # defining CSV headers
    headers = ['Restaurant ID', 'Restaurant Name', 'Menu Item', 'Description', 'Price', 'Link']
    
    # opening CSV file in write mode
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # writing header
        writer.writerow(headers)
        
        # writing the data rows
        for row in data:
            writer.writerow(row)
    print("CSV writing complete.")

def main():
    cuisine_list =  [
        'american', 'arabic', 'asian', 'breakfast','café', 'chinese','drinks','filipino',
        'grocery','healthy','indian','italian','japanese', 'lebanese','mexican',
        'middle+eastern','north+indian','pakistani','thai'] #choices for the type of cuisine
    
    csv_data = []
    restaurant_id = 1  # starting with restaurant ID 1

    for cuisine in cuisine_list:
        print(f"Processing cuisine: {cuisine}")
        web_url = f'https://deliveroo.ae/restaurants/abu-dhabi/saadiyat?geohash=thqew2ggd3ss&sort=rating&offer=all+offers&cuisine={cuisine}'
        
        # scraping static restaurant data using BeautifulSoup
        restaurant_names, menus = data_scrape(web_url)

        # processing data for CSV writing
        for restaurant, menu in zip(restaurant_names, menus):
            for item in menu['menu']:
                # appending restaurant ID, restaurant name, menu item details to CSV data
                    csv_data.append([restaurant_id, restaurant['name'], item['name'], item['description'], item['price'], restaurant['url']])
            restaurant_id += 1

    # writing the data to CSV
    write_to_csv(csv_data, 'restaurants_sample.csv')
    print("All data processed successfully.")

main()
