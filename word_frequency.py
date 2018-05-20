import re
import time 
import sys

'''
Function takes in a string (filename) and returns a list of words,and numbers in the file
'''
def split_words_in_file(filename):
	file=open(filename,'r')
	content=file.read().lower().replace("_",' ')
	pattern=re.compile("\w+")
	file.close()
	return pattern.findall(content)

'''
Function takes in a list of words (wordlist) and returns a list of sorted  tuples with each word and its frequency in the list eg[("Apple",2)]
'''
def frequency(wordlist):
	word_count=[]
	wordset=set(wordlist)
	for word in wordset:
		word_count.append((word,wordlist.count(word)))
	word_count.sort(key=lambda x:(-x[1],x[0]))
	return word_count

'''
Function takes in a list of tuples and prints them out for display
'''
def print_word_count(word_count):
	for item in word_count:
		print("{} - {}".format(item[0],item[1]))

if __name__=='__main__':
	try:
		RunTimes=[]
		print("Runing  word_frequency.py")
		for i in range(1,len(sys.argv)):
			start=time.time()
			words=split_words_in_file(sys.argv[i])	
			print_word_count(frequency(words))
			end=time.time()
			RunTimes.append(end-start)
		print("Program runnung time:{} seconds".format(end-start))
		print("File Run Times: {}".format(RunTimes))
	except IOError:
		print("Error: file does not exist")
