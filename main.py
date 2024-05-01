import os
import time
import phonenumbers
from phonenumbers import geocoder
from opencage.geocoder import OpenCageGeocode
import requests

apiKey = "8a5b8b0d900345cfa1ec05fee980c6a4"

try:
    import phonenumbers
    from phonenumbers import geocoder
    from opencage.geocoder import OpenCageGeocode
    import requests
except ImportError:
    print("Installing required libraries...")
    try:
        os.system("pip install phonenumbers opencage requests")
        import phonenumbers
        from phonenumbers import geocoder
        from opencage.geocoder import OpenCageGeocode
        import requests
    except Exception as e:
        print("Failed to install required libraries. Please install them manually.")
        print(f"Error: {e}")
        exit()

def get_phone_info(phone_number):
    phone_info = {}
    phone_info['phone_number'] = phone_number
    phoneNo = phonenumbers.parse(phone_number)
    phone_info['location'] = geocoder.description_for_number(phoneNo, "en")
    geotracker = OpenCageGeocode(apiKey)
    results = geotracker.geocode(phone_info['location'])
    if results and len(results):
        result = results[0]
        phone_info['country'] = result['components']['country']
        phone_info['continent'] = result['components']['continent']
        phone_info['latitude'] = result['geometry']['lat']
        phone_info['longitude'] = result['geometry']['lng']
        phone_info['additional_details'] = result['annotations']
        phone_info['place_name'] = find_place_name(result['geometry']['lat'], result['geometry']['lng'])
    else:
        phone_info['error'] = f"Location information not found for {phone_number}"
    return phone_info

def print_phone_info(phone_info):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;32m")
    print(r"""
┓┏┏┓┏┓┓┏┓┏┓  ┏┓┓┏┏┓┳┓┏┓  ┳┳┓┏┓┏┓
┣┫┣┫┃ ┃┫ ┏┛  ┃┃┣┫┃┃┃┃┣   ┃┃┃┣ ┃┃
┛┗┛┗┗┛┛┗┛┗┛  ┣┛┛┗┗┛┛┗┗┛  ┻┛┗┻ ┗┛
          AUTHOR : RUBIN.
        """)

    print("\033[1;34m")
    print("-" * 60)
    print("\033[1;36m")
    print(f"Phone Number Place: {phone_info['place_name']}")
    print(f"Phone Number: {phone_info['phone_number']}")
    print(f"Location: {phone_info['location']}")
    print(f"Country: {phone_info['country']}")
    print(f"Continent: {phone_info['continent']}")
    print(f"Latitude: {phone_info['latitude']}, Longitude: {phone_info['longitude']}")
    print("\n\033[1;35mAdditional Details:")
    for key, value in phone_info['additional_details'].items():
        if isinstance(value, dict):
            for k, v in value.items():
                print(f"{key.title().replace('_', ' ')} {k}: {v}")
                time.sleep(0.2)
        else:
            print(f"{key.title().replace('_', ' ')}: {value}")
            time.sleep(0.2)
    print("\033[1;31m")
    print("-" * 60)
    input("\nPress Enter to continue...")

def find_place_name(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'display_name' in data:
            return data['display_name']
    return "Place name not found"

phone_number = input("Enter phone number with country code (e.g., +15551234567): ").strip()
phone_info = get_phone_info(phone_number)
print_phone_info(phone_info)
