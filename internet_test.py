import urllib.request

try:
    urllib.request.urlopen('http://www.google.com', timeout=5)
    print("internet available")
except:
    print("Connection failed")