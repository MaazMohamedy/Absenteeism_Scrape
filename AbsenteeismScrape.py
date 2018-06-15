"""
This program scrapes data from https://data1.cde.ca.gov/dataquest/ on absenteeism rates for
all 13,655 active k-12 schools in California. The csv file, absenteeismRates.csv, 
displays absenteeism rates for all reported ethnicities from every school. Data for certain
ethnicites is witheld in the instance when the student population of that ethnicity is
small enough to be considered identifying. 

Current school directory is read and stored as a data frame.
Requests library is used to return html of the page holding our data. 
BeutifulSoup is used to parse html and extract desired data.
Profile is used to time the program.

Not complete
"""
import cProfile, pstats, io
from bs4 import BeautifulSoup
import requests
import csv 
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from openpyxl import Workbook
import time
import profile

def errorCheck(soup):
	content = (soup.find('div', id='content'))
	if (content.find('div', id='ContentPlaceHolder1_pnlNoReport') ):
		return True

	return False

def FillTable(j):
	recordType = 'School' #df.iloc[j,0]
	county = df.iloc[j,2]
	cdsCode = df.iloc[j,1]
	district = df.iloc[j,3]
	school = df.iloc[j,4]
	charter = df.iloc[j,8]
	isPublic = df.iloc[j,9]
	street = df.iloc[j,10]
	zip_ = df.iloc[j,11]

	cdsCode = '0'+str(cdsCode) if len(str(cdsCode)) == 13 else str(cdsCode)


	url = 'https://data1.cde.ca.gov/dataquest/DQCensus/AttChrAbsRate.aspx?agglevel=School&cds=' + cdsCode + '&year=2016-17'

    # receiving the source html and creating a BeautifulSoup object
	source = requests.get(url).text
	soup = BeautifulSoup(source, 'lxml')

	#Check for cases when there is no data is available (ex: Special-ed schools)
	if (errorCheck(soup) == True):
		return

	table1 = soup.find('div', class_="table-responsive")
	listOfRowsTable1 = table1.findAll('tr')
	firstRowTable1 = listOfRowsTable1[0]


	for i in range(1,10) :
		firstRowTable1 = listOfRowsTable1[i]
		Ethnicity = firstRowTable1.findAll('td')
		csv_writer.writerow([recordType, county, district, cdsCode, school, charter, isPublic, street, zip_,
		Ethnicity[0].text, Ethnicity[1].text, Ethnicity[2].text, Ethnicity[3].text ])

	return



pr = cProfile.Profile()
pr.enable()

df = pd.read_excel('SchoolDirectory.xlsx', sheet_name='Sheet1')
csvFile = open('absenteeismRatesTestRun.csv', 'w')
csv_writer = csv.writer(csvFile)
csv_writer.writerow(['Record Type', 'County', 'District', 'CDS Code', 'School', 'Charter Yes/No', 'Public Yes/No', 'Street City', 'Street Zip', 'Ethnicity', 'Cumulative enrolment', 'Chronic absenteeism count', 'Chronic absenteeism rate'])

cds_Codes = []

for i in range(0,13654):
	FillTable(i)

csvFile.close()
pr.disable()
pr.print_stats()#end def main
