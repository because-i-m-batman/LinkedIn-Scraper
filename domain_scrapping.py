from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import csv
import json
import os.path
import pandas as pd 





unvisited_queue = [] #List contaning the linkedin URL of individuals
visited = [] #all the visited url is present in this list


#Scrapping of Individual LinkedIn Id with a particular keyword
def domain_scrapping():

	driver = webdriver.Chrome('chromedriver') # giving path to the chrome driver/Firefox Driver
	driver.maximize_window()
	driver.get('https://www.linkedin.com/login')# opening website
	username = driver.find_element_by_id('username')
	username.send_keys('Your LinkedIn Username') #typing email
	password = driver.find_element_by_id('password')
	password.send_keys('Your LinkedIn Password')
	login_btn = driver.find_element_by_xpath('//*[@type="submit"]') #find the submit button
	login_btn.click()
	#keyword using machine learning engineer ,you can change it your required field
	keyword1 = "keywords=machine%20learning%20engineer&"
	cv = "https://www.linkedin.com/search/results/people/?"+ keyword1
	keyword2 = "&origin=SWITCH_SEARCH_VERTICAL&page="


	for i in range(1,101):

		page = str(i)
		people = cv + keyword2 + page

		driver.get(people)#searching for the profiles


		#perform scrolling operation to get the all the names of the profiles
		target = driver.find_element_by_id('a11y-notification')

		actions = ActionChains(driver)

		actions.move_to_element(target)
		actions.perform()


		#Extract names from the Profiles
		names = [el.text for el in driver.find_elements_by_xpath("//a[contains(@id,'ember')]//span[@class='name actor-name']")]
		print('Names')
		print(names)

		print('\n')
		#getting linkidIn ids
		url = [el.get_attribute('href') for el in driver.find_elements_by_css_selector('div.search-entity.search-result.search-result--person.search-result--occlusion-enabled.ember-view a.search-result__result-link.ember-view[href]')]

		#remove duplicates
		def Remove_duplicates(duplicate): 
		    final_list = [] 
		    for num in duplicate: 
		        if num not in final_list: 
		            final_list.append(num) 
		    return final_list 

		ids = Remove_duplicates(url)
		print('Linkedin Url')
		print(ids)

		unvisited_queue.extend(ids)

#exporting data to csv file
def csv_write():

	with open('domain.csv','w') as f:
		write = csv.writer(f)
		if not os.path.isfile('domain.csv'):
			field = ['LinkedIn URL']

			write.writerow(field)
		#check if the current url is not present in visited list	
		for i in unvisited_queue:
			if i not in visited:
				visited.append(i)
				write.writerow([i])

#expoting data to json file
def json_write():

	with open('domain.json','w') as f:

		json.dump('{}:{}'.format("Linkedin-url",unvisited_queue),f)

domain_scrapping()
csv_write()
json_write()