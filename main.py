import logging
import configparser
import os
import time
from selenium import webdriver
from gui import *
from math import ceil
from threading import Thread

# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("logs.log", 'w', encoding="utf-8",)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)

driverpath = f'{os.getcwd()}\\geckodriver.exe'


class BrowserThread(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.start()

	def run(self):
		driver.maximize_window()
		driver.implicitly_wait(30)
		login()
		while True:
			if active[0] and frames:
				editcamps()

def login():
	config = configparser.ConfigParser()
	if os.path.isfile('config.ini'):
		config.read('config.ini')
		login = config['Admin']['Login']
		password = config['Admin']['Pass']
	else:
		log.critical('Config file (config.ini) not found')
	log.info('Opening main page...')
	driver.get('https://megapu.sh/?a=campaigns&f=stop')
	log.info('Done')
	input_login = driver.find_element_by_id('login')
	input_pass = driver.find_element_by_id('password')
	input_login.send_keys(login)
	input_pass.send_keys(password)
	input()
	driver.get('https://megapu.sh/?a=campaigns&f=stop')


def editcamps():
	pages = ceil(int(driver.find_element_by_class_name('counter-stop').text) / 25) #counter-running
	for frame in frames:
		log.debug('Checking frame...')
		if frame['id'].get() != '0':
			for page in range(pages):
				driver.get(f'https://megapu.sh/?a=campaigns&f=stop&camp_id={frame["id"].get()}&action=edit&page={page}')
				time.sleep(3)
				log.debug('Searcing for campid...')
				if driver.find_element_by_id('camp_id').text == frame['id'].get():
					log.debug(f'Found {frame["id"].get()}')
					break


if __name__ == '__main__':
	driver = webdriver.Firefox(executable_path=driverpath)
	browser = BrowserThread()
	root.mainloop()
