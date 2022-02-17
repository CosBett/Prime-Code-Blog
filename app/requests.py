from email.quoprimime import quote
from app import app
import requests,json

BASE_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
def get_quotes(): 
    response = requests.get(f"{BASE_URL}")
    if response.status_code ==200:
      quote = response.json()
      return quote
      
