import requests
import csv
import sys
import getopt
from cryptography.fernet import Fernet

def download_file(url):
    r = requests.get(url)
    with open("salarios_crypt.csv", "wb") as f:
        f.write(r.content)

def decrypt_file(input_file, key):
    cipher_suite = Fernet(key)
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    
    with open('salarios.csv', 'wb') as f:
        f.write(decrypted_data)

def show_help():
    print("Usage: python script.py -k <key> or --key=<key>")
    print("Example: python script.py -k OceanSecKEYcsv")

if __name__ == "__main__":
    key = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hk:", ["help", "key="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-k", "--key"):
            key = arg.encode()

    if key is None:
        show_help()
        sys.exit(2)

    url = "https://d.site.com/salarios_crypt.csv"
    download_file(url)
    decrypt_file("salarios_crypt.csv", key)
