from time import sleep, time
import requests
import webbrowser

class Sales:    
    def __init__(self) -> None:
        self.items = []
        self.headers = self.prepare_headers()
        self.wait_time = 60
        self.max_duration_hour = 1
        pass
    
    def add_items(self, items):        
        for item in items:
            item['status'] = 'unavailable'
            self.items.append(item)    

    def set_wait_time_second(self, wait_time):
        self.wait_time = wait_time
    
    def set_max_duration_hour(self, duration):
        self.max_duration_hour = duration

    def run(self):
        start_time = time()
        while True:            
            if time() - start_time > self.max_duration_hour * 3600:
                print('Reached max duration.')
                break

            if self.all_items_available():
                print('All items are available.')
                break
        
            self.udpate_items()
        
    def all_items_available(self):
        for item in self.items:
            if item['status'] != 'available':
                return False
        return True

    def udpate_items(self):
        for i in range(0, len(self.items)):
            new_status = self.get_item_status(self.items[i])
            
            if new_status != self.items[i]['status']:                
                self.items[i]['status'] = new_status
                self.notify_customer_about_item(self.items[i])
            
            sleep(self.wait_time)
            
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
        headers_dict = dict()
        f = open(file_path)
        for line in f:
            i = line.find(':')
            name = line[:i]
            val = line[i+1:]
            headers_dict[name] = val.strip()
        f.close()
        return headers_dict

    def get_item_status(self, item):
        if item['status'] == 'available':
            return 'available'

        res = requests.get(item['url'], headers=self.headers)
        
        if res.status_code == 403:
            message = 'Unauthorized access to website.\n'
            message += '=================\n'
            message += 'Item name: ' + item['name'] + '\n' 
            message += 'Item url: ' + item['url'] + '\n' 
            message += 'Cause: header file outdated or IP being blocked .\n'
            message += '=================\n'

            raise RuntimeWarning(message)
        
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