# scrapes absenteeism rates from:  https://data1.cde.ca.gov/dataquest/
# this script is just for testing purposes to scrape absenteeism rates from a handful of schools
from bs4 import BeautifulSoup
import requests
import csv 

# cds_Codes = ['19734601939149', '19734601932862', '36676783630522'] # Walnut high, Diamond Bar high, Ayala High
cds_Codes = ['19734601939149'] #Walnut High

csvFile = open('absenteeism.csv', 'w')
csv_writer = csv.writer(csvFile)
csv_writer.writerow(['school_cds_code', 'Lead_Contamination_Level', 'Absenteeism_Rate'])

for cds_code in cds_Codes: 
	# creates URL by splicing the cds code into the template url
	url = 'https://data1.cde.ca.gov/dataquest/DQCensus/AttChrAbsRate.aspx?agglevel=School&cds=' + cds_code + '&year=2016-17'
	
	# print('\n')

	# receiving the source html and creating a BeautifulSoup Object
	source = requests.get(url).text
	# print(source)
	soup = BeautifulSoup(source, 'lxml')

	firstTable = soup.find('div', class_="table-responsive")
	# print(firstTable)
	listOfRowsTable1 = firstTable.findAll('tr')
	firstRowTable1 = listOfRowsTable1[1]
	AfricanAmerican = firstRowTable1.findAll('td')[3].text

	print("African American absenteeism rate: \n")
	print(AfricanAmerican)
	print("\n ----------------- \n")
	break
	# getting the html for the second table - which contains the cumulative absenteeism rate for x school
	secondTable = soup.find('div', id='ContentPlaceHolder1_pnlTotal')
	secondTable = secondTable.find('div', class_="table-responsive")

	#list of TRs - there should be 5 TRs for the 5 rows in the table
	listOfRows = secondTable.findAll('tr')

	#Row with the absenteeism rate we are looking for
	firstRow = listOfRows[1]

	absenteeism_rate = firstRow.findAll('td')[3].text

	# print(absenteeism_rate)

	csv_writer.writerow([cds_code, 'N/A', absenteeism_rate])

csvFile.close()