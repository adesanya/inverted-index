import re
import sys
import time 

def read_files(fileNameA,fileNameB):
	fileA=open(fileNameA,'r')
	fileB=open(fileNameB,'r')
	contentA=fileA.read()
	contentB=fileB.read()
	fileA.close()
	fileB.close()
	return [contentA,contentB]

def Tokenize(text):
	text=text.lower().replace("_",' ')
	pattern=re.compile("\w+")
	return pattern.findall(text)

def words_in_both(wordListA_B):
	count=0
	wordListA_B.sort(reverse=True)
	for word in wordListA_B[0]:
		if word in wordListA_B[1]:
			count+=1
			print(word)
	if count==0:
		print("No common words found in both files")
	else:
		print(count)

if __name__=='__main__':
	try:
		print("Running word_in_both_files.py")
		start=time.time()
		fileNameA=sys.argv[1]
		fileNameB=sys.argv[2]
		files=read_files(fileNameA,fileNameB)	 
		words_in_both([set(Tokenize(files[0])),set(Tokenize(files[1]))])
		end=time.time()
		print("Program runnung time:{} seconds".format(end-start))
	except IndexError:
		print("Error: Please provide 2 valid  file names as arguments to this program")
	except IOError:
		print("Error: file does not exist")
