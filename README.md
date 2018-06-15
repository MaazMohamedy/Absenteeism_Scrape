# Absenteeism_Scrape

This program scrapes data from https://data1.cde.ca.gov/dataquest/ on absenteeism rates for
all 13,655 active k-12 schools in California. The csv file, absenteeismRates.csv, 
displays absenteeism rates for all reported ethnicities from every school. Data for certain
ethnicites is witheld in the instance when the student population of that ethnicity is
small enough to be considered identifying. 

Current school directory is read and stored as a data frame.
Requests library is used to return html of the page holding our data. 
BeutifulSoup is used to parse html and extract desired data.
Profile is used to time the program.

This project is still work in progress.

