import json as js
import numpy as np
import matplotlib.pyplot as plt

import os
import sys

def ensure_exists(dir_fp):
    if not os.path.exists(dir_fp):
        os.makedirs(dir_fp)

def print_dems(dem_leading_digit_count, county_count, year):
	fig = plt.figure()
	bars = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
	y_pos = np.arange(1, len(bars)+1)
	plt.bar(y_pos, dem_leading_digit_count, color = 'b')
	plt.xticks(y_pos)
	plt.xlabel('Leading digit by county')
	plt.ylabel('Number of occurrences')
	plt.title(f'{year} Democrats\' Benford')
	add_benford_line(plt, y_pos)
	plt.show()

def print_reps(rep_leading_digit_count, county_count, year):
	fig = plt.figure()
	bars = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
	y_pos = np.arange(1, len(bars)+1)
	plt.bar(y_pos, rep_leading_digit_count, color = 'r')
	plt.xticks(y_pos)
	plt.xlabel('Leading digit by county')
	plt.ylabel('Number of occurrences')
	plt.title(f'{year} Republicans\' Benford')
	add_benford_line(plt, y_pos)
	plt.show()

def print_all(dem_leading_digit_count, rep_leading_digit_count, county_count, year, state_to_check):
	fig, (ax1, ax2) = plt.subplots(1, 2)
	bars = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
	y_pos = np.arange(1, len(bars)+1)
	ax1.bar(y_pos, dem_leading_digit_count, color = 'b')
	ax1.set_xticks(y_pos)
	ax1.set_xlabel('Leading digit by county')
	ax1.set_ylabel('Number of occurrences')
	ax1.set_title(f'{year} Democrats\' Benford')
	add_benford_line(ax1, y_pos, county_count)
	ax2.bar(y_pos, rep_leading_digit_count, color = 'r')
	ax2.set_xticks(y_pos)
	ax2.set_xlabel('Leading digit by county')
	ax2.set_ylabel('Number of occurrences')
	ax2.set_title(f'{year} Republicans\' Benford')
	add_benford_line(ax2, y_pos, county_count)
	fig.tight_layout()
	if state_to_check != '':
		fig.suptitle(f'Out of {county_count} counties in {state_to_check}')
	else:
		fig.suptitle(f'Out of {county_count} counties in the USA')
	fig.subplots_adjust(top=0.88)

	# save the plot
	ensure_exists(f'./plots/{year}')
	out_fp = ''
	if state_to_check != '':
		out_fp = f'./plots/{year}/{state_to_check}.png'
	else:
		out_fp = f'./plots/{year}/USA.png'
	plt.savefig(out_fp)
	plt.close()
	#plt.show()

def add_benford_line(ax, y_pos, county_count):
	benford_values = np.array([30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6])
	benford_values_aligned = benford_values * 0.01 * county_count
	ax.plot(y_pos, benford_values_aligned, color = 'g')

#State is optional, format needed is two-letter acronym. If state is not provided, does entire USA
def do_2016(state_to_check = ''):
	file = open('2016.json')
	json = js.load(file)

	year = 2016

	dem_leading_digit_count = np.zeros(9)
	rep_leading_digit_count = np.zeros(9)

	county_count = 0
	for key, value in json.items():
		dem_value = value[0]
		rep_value = value[1]
		state = value[7]
		county = value[8]
		if state == state_to_check or state_to_check == '':
			print(f'{county}, {state} has {dem_value} dem votes and {rep_value} rep votes')
			dem_leading = int(str(dem_value)[0])
			dem_leading_digit_count[dem_leading - 1] += 1
			rep_leading = int(str(rep_value)[0])
			rep_leading_digit_count[rep_leading - 1] += 1
			county_count += 1
	print_all(dem_leading_digit_count, rep_leading_digit_count, county_count, year, state_to_check)

#State is optional, format needed is full state name. If state is not provided, does entire USA
def do_2020(state_to_check = ''):
	file = open('2020.json')
	json = js.load(file)

	year = 2020

	dem_leading_digit_count = np.zeros(9)
	rep_leading_digit_count = np.zeros(9)

	county_count = 0
	for key, value in json.items():
		dem_value = value[3]
		rep_value = value[2]
		state = value[0]
		county = value[1]
		if state == state_to_check or state_to_check == '':
			print(f'{county}, {state} has {dem_value} dem votes and {rep_value} rep votes')
			dem_leading = int(str(dem_value)[0])
			dem_leading_digit_count[dem_leading - 1] += 1
			rep_leading = int(str(rep_value)[0])
			rep_leading_digit_count[rep_leading - 1] += 1
			county_count += 1
	print_all(dem_leading_digit_count, rep_leading_digit_count, county_count, year, state_to_check)

state_abbrevs = [ '', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY' ];
for i in state_abbrevs:
	do_2016(i)
states = ['', 'Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
for i in states:
	do_2020(i)
