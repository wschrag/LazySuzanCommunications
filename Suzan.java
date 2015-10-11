import math
final int NUMITEMS = 1;
double[] sequence;
boolean[] divides;
Random rand_gen = new Random(10);
//objects, basically.


public static void main(String[] args) {
sequence = new double[NUMITEMS];
divides = new boolean[NUMITEMS];



parse_num_seq(gen_num_seq());
//parse_num_seq_bad(gen_num_seq());
//parse_num_seq_good(gen_num_seq());
System.out.println("It is %.40f", 0.1f);
System.out.println("It is %.40f", (0.1f + 0.2f);
}



//subprocess.check_output([args])

//we made telephone.

//master code
public String master_start() {
//def gen_num_seq():
	double[] sequence
	for (int i = 0; i < NUMITEMS; i++) {
		next = random.nextFloat();// + 0.1
		next_divide = random.nextBoolean();
		sequence[i] = next;
		divides[i] = next_divide
		sequence.append(next_divide);
		#string_thing = ['{:.2f}'.format(x) for x in sequence]\
		string_thing = " ".join(map(str, sequence))
		#it goes thing div thing div...
	}
	return NULL;
}
#sort comes later

#for some reason returns an int.
public float parse_num_seq(list? string?) {
float result = 1.0f;
for (int i = 0; i < NUMITEMS; i++) {
    if (int(boolean thing from holder):
			result *= float(sequence_list[item * 2])
		else:
			result /= float(sequence_list[item * 2])
}


}
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



def crappy_sort(sequence_list):
	endex = NUMITEMS - 1
	for item in range(0, endex):
		while(sequence_list[(endex * 2) + 1] == 0):
				endex -= 1
		if (int(sequence_list[(item * 2) + 1]) == 0):
			hold_num = sequence_list[endex * 2]
			sequence_list[endex * 2] = sequence_list[item * 2]
			sequence_list[item * 2] = hold_num
			endex--;
	return sequence_list
