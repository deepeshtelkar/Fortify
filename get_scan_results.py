#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import csv
import time
import requests


class get_urls:
	"Class to capture streaming data in real time from YAHOO"

	# -- constructor --
	def __init__(self):
		self.titles = ['Date', 'URL', 'Critical', 'High', 'Low']
		self.output_file = "job-data.csv"

		self.urls = [
			'https://jenkins.optum.com/bff/job/API-Gateway/job/API-Gateway-Fortify/lastSuccessfulBuild/console',
			'https://jenkins.optum.com/bff/job/Fox-UI/job/Fox-UI-Fortify/lastSuccessfulBuild/console',
			'https://jenkins.optum.com/bff/job/Fox-Claims/job/Fox-Claims-Fortify/lastSuccessfulBuild/console',
			'https://jenkins.optum.com/bff/job/MDM-Mediator/job/MDM-Mediator-Fortify/lastSuccessfulBuild/console',
			'https://jenkins.optum.com/bff/job/BPM-Mediator/job/BPM-Mediator-Fortify/lastSuccessfulBuild/console',
			'https://jenkins.optum.com/bff/job/FOX-Process/job/Fox-Process-Fortify/lastSuccessfulBuild/console',
			'https://jenkins.optum.com/bff/job/Fox-Common/job/Fox-Common-Fortify/lastSuccessfulBuild/console',
			'https://jenkins.optum.com/bff/job/Member-Validation/job/Member-Validation-Fortify/lastSuccessfulBuild/console'
		]

		return


	# -- get URL content --
	def get_url_content(self, url):
		result = requests.get(url)
		page = result.text

		return page


	# -- get data from page --
	def get_data_content(self, page, url):
		row = {
			'Date': "",
			'URL': url,
			'Critical': 0,
			'High': 0,
			'Low': 0
		} 

		lines = page.split("\n")

		for i in range(0, len(lines)):
			if lines[i].find("Finished at:") >= 0:
				ini = lines[i].find(":") + 1
				end = lines[i][ini:].find("T") + ini
				row['Date'] = lines[i][ini:end].strip()

			if lines[i].find("Scan Results") >= 0:
				ini = lines[i+2].find(":") + 1
				row['Critical'] = lines[i+2][ini:].strip()
				ini = lines[i+3].find(":") + 1
				row['High'] = lines[i+3][ini:].strip()
				ini = lines[i+4].find(":") + 1
				row['Low'] = lines[i+4][ini:].strip()

		return row


	# -- write data on csv --
	def write_csv(self, csv_file, data):
		fp = open(csv_file, 'w')
		writer = csv.DictWriter(fp, fieldnames=self.titles, extrasaction='ignore', delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
		writer.writeheader()
		for i in data:
			writer.writerow(i)
		fp.close()

		return


######################################################################################################################
## MAIN


gu = get_urls()

if __name__ == "__main__":
	data = []

	for i in gu.urls:
		page = gu.get_url_content(i)
		row = gu.get_data_content(page, i[0])
		data.append(row)

	gu.write_csv(gu.output_file, data)



