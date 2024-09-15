import requests
from bs4 import BeautifulSoup

def data_scrape(web_url):

    reponse = requests.get(web_url)

    if reponse.status_code == 200: 
        html_data = BeautifulSoup(reponse.text, 'html.parser')

        #getting the items(restaurants) under the given class with a tag 'p'
        restaurants = html_data.find_all('p', class_= "ccl-649204f2a8e630fd ccl-a396bc55704a9c8a ccl-ff5caa8a6f2b96d0 ccl-40ad99f7b47f3781")
        
        restaurant_names = [restaurant.get_text() for restaurant in restaurants] #getting the names/text only
        return restaurant_names
    else:
        return []
        
def main():
    cuisine_list =  [
        'american', 'arabic', 'asian', 'breakfast','café', 'chinese','drinks','filipino',
        'grocery','healthy','indian','italian','japanese', 'lebanese','mexican',
        'middle+eastern','north+indian','pakistani','thai'] #choice for the type of cuisine
    
    all_restaurants =[]
    
    for cuisine in cuisine_list:

        web_url = f'https://deliveroo.ae/restaurants/abu-dhabi/saadiyat?geohash=thqew2ggd3ss&sort=rating&offer=all+offers&cuisine={cuisine}'
        
        restaurant_names = data_scrape(web_url) #function call
        restaurants_10 = restaurant_names[:10] #getting 10 restaurants each for each cuisine

        all_restaurants.extend(restaurants_10) #adding the 10 restaurants for each cuisine to the bigger list
   
    for index, rest_name in enumerate(all_restaurants, 1):
        print(f"{index}.{rest_name}")
    
main()