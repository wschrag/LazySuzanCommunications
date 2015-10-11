#generate a string of operations and numbers.
#Not that hard.
import math
import random


NUMITEMS = 1



def evaluate():
	return 1


#master code

def gen_num_seq():
	random.seed(10) # Testing code
	sequence = []
	for i in range(0,NUMITEMS):
		next = random.uniform(.1, 56468832)# + 0.1
		next_divide = random.randint(0,1)
		sequence.append(next)
		sequence.append(next_divide)
		#string_thing = ['{:.2f}'.format(x) for x in sequence]\
		string_thing = " ".join(map(str, sequence))
		#it goes thing div thing div...
	return string_thing
#sort comes later

#for some reason returns an int.
def parse_num_seq(sequence_str):
	sequence_list = sequence_str.split()
	result = float(1.0)
	for item in range(0, NUMITEMS):
		#print "The number: %f" % float(sequence_list[item * 2])
		if (int(sequence_list[(item * 2) + 1]) == 0):
			result *= float(sequence_list[item * 2])
		else:
			result /= float(sequence_list[item * 2])
	#print sequence_list[0] ok this works
	print "The total: %.40f" % result
	return result

def parse_num_seq_bad(sequence_str):
	sequence_list = crappy_sort(sequence_str.split())
	result = float(1.0)
	for item in range(0, NUMITEMS):
		#print "The number: %f" % float(sequence_list[item * 2])
		if (int(sequence_list[(item * 2) + 1]) == 0):
			result *= float(sequence_list[item * 2])
		else:
			result /= float(sequence_list[item * 2])
	#print sequence_list[0] ok this works
	print "The total: %.20f" % result
	return result

def parse_num_seq_good(sequence_str):
	sequence_list = better_sort(sequence_str.split())
	result = float(1.0)
	for item in range(0, NUMITEMS):
		#print "The number: %f" % float(sequence_list[item * 2])
		if (int(sequence_list[(item * 2) + 1]) == 0):
			result *= float(sequence_list[item * 2])
		else:
			result /= float(sequence_list[item * 2])
	#print sequence_list[0] ok this works
	print "The total: %.20f" % result
	return result

def sort_num_seq():
	return 0

def crappy_sort(sequence_list):
	endex = NUMITEMS - 1
	for item in range(0, NUMITEMS):
		while(sequence_list[(endex * 2) + 1] == 0):
				endex -= 1
		if (int(sequence_list[(item * 2) + 1]) == 0):
			hold_num = sequence_list[endex * 2]
			sequence_list[endex * 2] = sequence_list[item * 2]
			sequence_list[item * 2] = hold_num
			endex -= 1
	return sequence_list

def better_sort(sequence_list):
	endex = NUMITEMS - 1
	for item in range(0, NUMITEMS):
		if (int(sequence_list[(item * 2) + 1]) == 1):
			hold_num = sequence_list[endex * 2]
			sequence_list[endex * 2] = sequence_list[item * 2]
			sequence_list[item * 2] = hold_num
			endex -= 1
	return sequence_list

def true_one():
  return 0.1; 


#main
# "the sequence: %s" % gen_num_seq()
parse_num_seq(gen_num_seq())
parse_num_seq_bad(gen_num_seq())
parse_num_seq_good(gen_num_seq())
print "It is %.40f" % true_one()