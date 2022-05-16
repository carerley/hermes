from email import message
from time import sleep
import requests
import webbrowser

class Sales:    
    def __init__(self) -> None:
        self.items = []
        self.headers = self.prepare_headers()
        self.wait_time = 10
        pass
    
    def add_items(self, items):        
        for item in items:
            item['status'] = 'unavailable'
            self.items.append(item)    

    def set_wait_time(self, wait_time):
        self.wait_time = wait_time

    def run(self):        
        while True:
            if self.all_items_available():
                break
            else:
                self.udpate_items()
            
            sleep(self.wait_time)                                    
        
    def all_items_available(self):
        for item in self.items:
            if item['status'] != 'available':
                return False
        return True

    def udpate_items(self):
        for i in range(0, len(self.items)):
            status = self.get_item_status(self.items[i])
            
            if status != self.items[i]['status']:                
                self.items[i]['status'] = status                
                self.notify_customer_about_item(self.items[i])
            
    def prepare_headers(self) -> object:
        headers_dict = self.parse_header_file('shop/header')
        headers = {
            'accept': headers_dict['accept'],
            'accept-encoding': headers_dict['accept-encoding'],
            'accept-language': headers_dict['accept-language'],
            'user-agent': headers_dict['user-agent']
        }
        return headers

    def parse_header_file(self, file_path):
        headers = dict()
        f = open(file_path)
        for line in f:
            i = line.find(':')
            name = line[:i]
            val = line[i+1:]
            headers[name] = val.strip()
        f.close()
        return headers

    def get_item_status(self, item):
        res = requests.get(item['url'], headers=self.headers)
        if res.status_code == 403:
            raise RuntimeWarning("Unauthorized to access the website")
        elif res.status_code == 404:            
            print('Item unavailable')
            return 'unavailable'
        elif res.status_code == 200:
            print('Item available')
            return 'available'
        else:
            print('Item might be available', '\nstatus code: ', res.status_code)            
            return 'unknown'

    def notify_customer_about_item(self, item):        
        webbrowser.open(item['url'], new=1)