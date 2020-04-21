from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import json
import pandas as pd
from functools import reduce
import os.path  
import numpy as np
import urllib.request


#Read the domain.csv file for seacrhing each LinkedIn URL
df = pd.read_csv('domain.csv')

df = df.values.tolist()

#reducing data frame to list
df = reduce(lambda x,y: x+y, df)
not_visited = df

#Read the visited Url file, comment this portion if you are running it first time 
df1 = pd.read_csv('newVisitedUrl.csv')

df1 = df1.values.tolist()
df1 = reduce(lambda x,y:x+y,df1)
length_of_visited = len(df1)
visited = df1

start_from_this_url_agin = visited[length_of_visited-1]
print('visited')
print(visited)
print('\n')

#subtracting visited elements from the original domains ,you will get the unvisted domains
not_visited = set(not_visited) - set(visited)
not_visited = list(not_visited)
print(not_visited)

not_visited.insert(0,start_from_this_url_agin)

k = len(not_visited)
print('not_visited')
print(not_visited)

#opening file for writing the each individual profile data
if os.path.isfile('Testing-Subject-Profile-Scraping.csv'):
	f = open('Testing-Subject-Profile-Scraping.csv','a',newline='',encoding="utf-8")
	write = csv.writer(f)

#writing the field names that we are going to extract from each individual profiles
if not os.path.isfile('Testing-Subject-Profile-Scraping.csv'):
	f = open('Testing-Subject-Profile-Scraping.csv','w',newline='',encoding="utf-8")
	write = csv.writer(f)
	fields = ['Name','linkedin-Id','current_company','current_location','current_position','experience_in_profile','total_experience','experience_in_companies','experience_in_position','experience', 'School-Names', 'Degree','Volunteer-Events','volunteer_position','endorsed-skills','other-skills','Recommedations','Projects','Honors','Languages','Courses','certificate-course-names','Image-Source']
	write.writerow(fields)



fp = open('newVisitedUrl.csv','a',newline='',encoding="utf-8")
csv_writer = csv.writer(fp)


#converting categorical value of experience to numerical values

input_for_pofile = 'Computer Vision Engineer'


#profile scraping
def profile_scraping():

	driver = webdriver.Chrome('chromedriver') # giving path to the chrome driver
	driver.maximize_window()

	driver.get('https://www.linkedin.com/login')# opening website
	username = driver.find_element_by_id('username')
	username.send_keys('Your LinkedIn Username') #typing email


	password = driver.find_element_by_id('password')
	password.send_keys('Your LinkedIn Password')  
	login_btn = driver.find_element_by_xpath('//*[@type="submit"]') #find the submit button
	login_btn.click()



	for i in range(k):

	
		

		visited.append(not_visited[0]) #adding the current profile to the visited list
		driver.get(not_visited[0])
		csv_writer.writerow([not_visited[0]])
		img_src = []

		#getting the image url for each individual
		img = driver.find_elements_by_css_selector('section.pv-top-card.artdeco-card.ember-view div.ph5.pb5 div.display-flex div.pv-top-card--photo.text-align-left div.pv-top-card__photo-wrapper.ml0 div.presence-entity.pv-top-card__image.presence-entity--size-9.ember-view img')
		for src in img:
			img_src.append(src.get_attribute('src')) #storing image source into list

		print('\n')
		print('Image Source')
		print(img_src)

	
	

		#scrolling the window,scrolling is necessary because without scrolling it to the bottom of the page ,you will get some missing value

		driver.execute_script('window.scrollTo(0,500);')
		time.sleep(1)
		driver.execute_script('window.scrollTo(500,1000);')
		time.sleep(1)
		driver.execute_script('window.scrollTo(1000,1500);')
		time.sleep(1)
		driver.execute_script('window.scrollTo(1500,2000);')
		time.sleep(1)
		driver.execute_script('window.scrollTo(2000,2500);')
		time.sleep(1)
		driver.execute_script('window.scrollTo(2500,3000);')
		time.sleep(1)
		driver.execute_script('window.scrollTo(3000,3500);')
		time.sleep(1)
		driver.execute_script('window.scrollTo(3500,4000)')
			

		try:
			#clicking buttons show more for education and experience
			try:#show more button for skills field
				show_more_button_skills = driver.find_element_by_css_selector('.pv-profile-section__card-action-bar.pv-skills-section__additional-skills.artdeco-container-card-action-bar.artdeco-button.artdeco-button--tertiary.artdeco-button--3.artdeco-button--fluid')
				driver.execute_script("arguments[0].click();", show_more_button_skills)
			except:
				print("No such element")

			try:#show more button for eduaction field
				show_more_button_education = driver.find_elements_by_css_selector('.pv-profile-section__see-more-inline.pv-profile-section__text-truncate-toggle.link.link-without-hover-state')
				for i in show_more_button_education:
					driver.execute_script("arguments[0].click();", i)
			except:
				print('No such element')

	

		finally:

			#name of the candidate 
			name_of_candidate = [el.text for el in driver.find_elements_by_css_selector('div.flex-1.mr5 li.inline.t-24.t-black.t-normal.break-words')]
			print('\n')
			print(name_of_candidate)
			print('\n')

			#experience
			company = []
			position = []
			experience = []

			try:#Extract the company names
				temp_company_variable1 = [el.text for el in driver.find_elements_by_css_selector('section.pv-profile-section.experience-section.ember-view h3.t-16.t-black.t-bold span' )]
				company.extend(temp_company_variable1[0:2])
				#Exract positions on which individual has worked on
				temp_position_variable1 = [el.text for el in driver.find_elements_by_css_selector('section.pv-profile-section.experience-section.ember-view h3.t-14.t-black.t-bold span')]
				position.extend(temp_position_variable1[0:2])
				#Experience of the candidates in respective jobs or position
				temp_experience_variable1 = [el.text for el in driver.find_elements_by_css_selector('section.pv-profile-section.experience-section.ember-view h4.t-14.t-black.t-normal span' )]
				experience.extend(temp_experience_variable1[0:2])
			
			



			finally:


				temp_company_variable2 = [el.text for el in driver.find_elements_by_css_selector('section.pv-profile-section.experience-section.ember-view p.pv-entity__secondary-title.t-14.t-black.t-normal')]
				company.extend(temp_company_variable2)

				temp_position_variable2 = [el.text for el in driver.find_elements_by_css_selector('section.pv-profile-section.experience-section.ember-view div.pv-entity__summary-info.pv-entity__summary-info--background-section h3.t-16.t-black.t-bold')]
				position.extend(temp_position_variable2)

				temp_experience_variable2 = [el.text for el in driver.find_elements_by_css_selector('section.pv-profile-section.experience-section.ember-view div.pv-entity__summary-info.pv-entity__summary-info--background-section h4.t-14.t-black--light.t-normal span.pv-entity__bullet-item-v2')]
				experience.extend(temp_experience_variable2)

			#removing noises and redundant data

			for i in company:
				if "Company Name" == i:
					company.remove(i)

			for i in position:		
				if 'Title' == i:
					position.remove(i)

			for i in experience:		
				if 'Total Duration' == i:
					experience.remove(i)

			for i in company:	
				if 'Full-time' == i:
					company.remove(i)

			print('Company')
			print(company)

			print('\n')
			print('experience')
			print(experience)

			print('\n')
			print('position')
			print(position)

			try:#Current Company
				current_company = [el.text for el in driver.find_elements_by_xpath('//div[@class = "display-flex mt2"]//a[@data-control-name = "position_see_more"]//span')]
				print('\n')
				print('current company')
				print(current_company)
			
			except:
				current_company = []
				print("No such element")

			
			try:#current location
				current_location = [el.text for el in driver.find_elements_by_css_selector('div.display-flex.mt2 li.t-16.t-black.t-normal.inline-block ')]
				print('\n')
				print('current location')
				print(current_location)
			
			except:
				current_location = []
				print('No such element')

			try:#current position
				cp = driver.find_element_by_css_selector('section.pv-top-card.artdeco-card.ember-view div.ph5.pb5 div.display-flex.mt2 div.flex-1.mr5 h2.mt1.t-18.t-black.t-normal')
				current_postion = [cp.text]
				print('\n')
				print('Current Position')
				print(current_postion)
			
			except:
				current_postion = []
				print('No such element')

			#Education

			try:
				#School and college names
				school_names = [el.text for el in driver.find_elements_by_css_selector('.pv-profile-section.education-section.ember-view h3.pv-entity__school-name.t-16.t-black.t-bold')]
				print('\n')
				print("school name")
				print(school_names)
			
			except:
				school_names = []
				print('No such element')

			try:#Degree names	
				degree = [el.text for el in driver.find_elements_by_css_selector('.pv-profile-section.education-section.ember-view .pv-entity__secondary-title.pv-entity__degree-name.t-14.t-black.t-normal span.pv-entity__comma-item')]
				print('\n')
				print('degree name')
				print(degree)
				print('\n')
			except:
				degree = []

			
			

			#vulunteer
			try:
				volunteer_position = [el.text for el in driver.find_elements_by_css_selector('section.pv-profile-section.volunteering-section.ember-view h3.t-16.t-black.t-bold ')] 
				volunteer_events = [el.text for el in driver.find_elements_by_css_selector('section.pv-profile-section.volunteering-section.ember-view span.pv-entity__secondary-title')]
				print(volunteer_events,volunteer_position)
				print('\n')
			except:
				volunteer_events = []
				volunteer_position = []

			#skills
			try:
				skills = [el.text for el in driver.find_elements_by_css_selector('section.pv-profile-section.pv-skill-categories-section.artdeco-container-card.ember-view span.pv-skill-category-entity__name-text.t-16.t-black.t-bold')]
				print('skills')
				print(skills)
				print('\n')
			except:
				skills = []
			
			#recommedation
			try:    
				recommedations = [el.text for el in driver.find_elements_by_css_selector('li.pv-recommendation-entity.ember-view h3.t-16.t-black.t-bold ')]
				print('recommedations')
				print(recommedations)
				print('\n')
			except:
				recommedations = []
			
			#projects     
			try:  
				projects = [el.text for el in driver.find_elements_by_css_selector('.accordion-panel.pv-profile-section.pv-accomplishments-block.projects.ember-view li')]
				print('projects')
				print(projects)
				print('\n')
			except:
				projects = []
			
			#honors and awards
			try:
				honors = [el.text for el in driver.find_elements_by_css_selector('.accordion-panel.pv-profile-section.pv-accomplishments-block.honors.ember-view li')]
				print('honors')
				print(honors)
				print('\n')
			
			except:
				honors = []

			#language
			try:
				language = [el.text for el in driver.find_elements_by_css_selector('.accordion-panel.pv-profile-section.pv-accomplishments-block.languages.ember-view li')]
				print('language')
				print(language)
				print('\n')
			
			except:
				language = []

			#courses
			try:
				courses = [el.text for el in driver.find_elements_by_css_selector('.accordion-panel.pv-profile-section.pv-accomplishments-block.courses.ember-view li')]
				print('courses')
				print(courses)
				print('\n')
			
			except:
				courses = []

			#certificate and courses
			try:
				certificate_course_names = [el.text for el in driver.find_elements_by_css_selector('.pv-profile-section.pv-profile-section--certifications-section.ember-view h3.t-16.t-bold')]
				print('cerificate courses names')
				print(certificate_course_names)
				print('\n')
			except:
				certificate_course_names = []
			#endorsed skills

			try:
				endorsed_skills = [el.text for el in driver.find_elements_by_css_selector('.pv-skill-categories-section__top-skills.pv-profile-section__section-info.section-info.pb1 span.pv-skill-category-entity__name-text.t-16.t-black.t-bold')]
				print('endorsed skills')
				print(endorsed_skills)
			
			except:
				endorsed_skills = []
			
			#other skills
			try:
				other_skills = [el.text for el in driver.find_elements_by_css_selector('.pv-skill-categories-section__expanded span.pv-skill-category-entity__name-text.t-16.t-black.t-bold')]
				print('\n')
				print('other_skills')
				print(other_skills)
			
			except:
				other_skills = []
			
			total_experience = []
			experience_in_profile = []
			totalexperience,experienceinprofile = experience_in_numerical_format(experience,position)

			total_experience.append(totalexperience)			#total Experience in years and months
			experience_in_profile.append(experienceinprofile)	#total experience in given or required profile
			
			#exporting all the data to the csv file
			export_list = [name_of_candidate,[str(not_visited[0])],current_company,current_location,current_postion,experience_in_profile,total_experience,company,position,experience,school_names,degree,volunteer_events,volunteer_position,endorsed_skills,other_skills,recommedations,projects,honors,language,courses,certificate_course_names,img_src]
			write.writerow(export_list)



		not_visited.pop(0)

		

print(not_visited)
print(visited)

#Experience in Numerical values
def experience_in_numerical_format(experience,position):
	for i in range(len(experience)):

		experience[i] = experience[i].replace('mo','month')
		experience[i] = experience[i].replace('yr','year')

	for i in range(len(experience)):

		experience[i] = experience[i].replace('months','month')
		experience[i] = experience[i].replace('years','year')	

	exper_and_profiles = dict(zip(position,experience))
	

	Total_month = []
	Total_year = []

	#converting string of experience into integers and calculating the total experince
	for i in range(len(experience)):
		experience[i] = experience[i].replace(' ','')
		if 'year'  in experience[i] and 'month' in experience[i]:
			s = experience[i].split('year')
			Total_year.append(s[0])
			Total_month.append(s[1])
			

		elif 'year'in experience[i]:
			s = experience[i].split('year')
			Total_year.append(s[0])
			

		elif 'month' in experience[i]:
			s = experience[i].split('month')
			Total_month.append(s[0])


	for i in range(len(Total_year)):
		try:
			Total_year[i] = int(Total_year[i])*12
		except:
			Total_year[i] = 0.5*12
			
			
				
	for i in range(len(Total_month)):

		print(Total_month[i])
		Total_month[i] = Total_month[i].replace('month','')
		Total_month[i] = int(Total_month[i])
		
	



	Total_years_experience = (sum(Total_month) + sum(Total_year))/12
	print('\n')
	print('Total Experience in Years')
	print(Total_years_experience)

	#calaculating experience in given profile
	year = []
	month = []
	experience_in_profile = []
	for key,value in exper_and_profiles.items():
			key = key.lower()
			if 'machine learning' in key:
				experience_in_profile.append(value)
	try:
		
		
		for i in range(len(experience_in_profile)):
			experience_in_profile[i] = experience_in_profile[i].replace(' ','')
			if 'year'  in experience_in_profile[i] and 'month' in experience_in_profile[i]:
				s = experience_in_profile[i].split('year')
				year.append(s[0])
				month.append(s[1])

			elif 'year'in experience_in_profile[i]:
				s = experience_in_profile[i].split('year')
				year.append(s[0])

			elif 'month' in experience_in_profile[i]:
				s = experience_in_profile[i].split('month')
				month.append(s[0])


		for i in range(len(year)):
			year[i] = int(year[i])*12
		for i in range(len(month)):
			month[i] = month[i].replace('month','')
			month[i] = int(month[i])

		experience_in_given_profile = float(sum(month)+sum(year))/12

	except:
		experience_in_given_profile =np.nan

	print('\n')
	print('Experience in given profile')
	print(experience_in_given_profile)
	return Total_years_experience,experience_in_given_profile


profile_scraping()


		

		
