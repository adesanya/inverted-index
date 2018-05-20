import json
import lxml 
import bs4 as bs
import pymongo
from pymongo import Connection
from lxml import etree, objectify
import re
import codecs
import math

def get_json_file(filename):
    file=open(filename,'r')
    content=file.read()
    jsonObj=json.loads(content)
    file.close()
    return jsonObj

def split_words_in_file(content):
	pattern=re.compile("\w+")
	return pattern.findall(content)

def stop_Words():
    file=open('stopwords.txt','r')
    content=file.read().split()
    file.close()
    return content

def remove_stopwords(wordList,stopWords):
    word_freq=frequency(wordList)
    for word in word_freq:
        if word[0] in stopWords:
            word_freq.remove(word)
    return word_freq

def xml_format(filename):
    file=codecs.open(filename,'r',"utf-8")
    content=file.read()
    file.close()
    return bs.BeautifulSoup(content,"lxml")

def frequency(wordlist):
	word_count=[]
	wordset=set(wordlist)
	for word in wordset:
		word_count.append((word,wordlist.count(word)))
	word_count.sort(key=lambda x:(-x[1],x[0]))
	return word_count

def get_page_content(path):
    xml_file=xml_format(path)
    word_list=[]

class page_analyzer:
    def __init__(self,path,stopWords):
       self.file_xml=xml_format(path)
       self.word_count=remove_stopwords(split_words_in_file(self.file_xml.text),stopWords)
       self.title=self.file_xml.title
       self.path=path
       self.stopwords=stopWords
       self.largest_word_count=()#(word,count)
       self.total_tokens=sum([i[1] for i in self.word_count])
       self.word_count_TF=[]

    def most_frequent_word(self):
        try:
            max_counrt=0
            found=self.word_count[0]
            for word_c in self.word_count:
                if word_c[1]>max_counrt:
                    found=word_c
                    max_counrt=word_c[1]
            self.largest_word_count=found
            return found
        except:
            return None

    def word_in_title(self, token):
        try:
            return token in self.title.string
        except :
            return False

    def computeTF(self):
        for w_c in self.word_count:
            self.word_count_TF.append((w_c[0],w_c[1],(w_c[1]/self.total_tokens)))

    def analyze(self):
        self.most_frequent_word()
        self.computeTF()
        
                
            
    
    

class index_builder:
    def __init__(self):
        print("Initializing Index Builder ...")
        self.connect=Connection('localhost', 27017)
        self.db=self.connect.ICS_Inverted_Index
        self.tokens=self.db.tokens
        self.stopWords=stop_Words()
        self.num_of_analyzed_files=0
        self.file_dict=get_json_file("WEBPAGES_RAW/bookkeeping.json")
        print("Initializing Complete")

    def write_to_db(self,token,file,word_count,positions,in_title,TF):
        self.tokens.insert({"token":token, "file_path":file,"word_count":word_count,"positions":positions,"in_title":in_title,"TF":TF})

    def build_index(self):
        print("Building Index ...")
        count=0#note change back to 0
        flag=False
        for file in self.file_dict.keys():
            if file=="0/439":
                flag=True
            if flag==False:
                continue
            file_path="WEBPAGES_RAW/"+file
            file_analysis=page_analyzer(file_path,self.stopWords)
            file_analysis.analyze()
            for token in file_analysis.word_count_TF:
                in_title=file_analysis.word_in_title(token[0])
                positions=0
                self.write_to_db(token[0],file,token[1],positions,in_title,token[2])
                print("Token: {}    Word Count: {}    File: {} TF: {}".format(token[0],token[1],file,token[2]))
            count+=1
            self.num_of_analyzed_files=count
        print("Finished Building Index")


    def compute_IDF(self,token):
        num_of_files=index.tokens.find({"token":token}).count()
        return math.log(self.num_of_analyzed_files / num_of_files)

    def compute_tf_idf(self,token):
        files_with_token=index.tokens.find({"token":token})
        print(token)
        for entry in files_with_token:
            file=entry.get("file_path")
            tf_idf=float(entry.get("TF"))*self.compute_IDF(token)
            print("Token:{}\nFile:{}\nURL: {}\nTF-IDF:{}\n".format(token,file,self.file_dict[file],tf_idf))
        print("------------------------------------------------------------------------"
              )
        
        
    def run(self):
        self.build_index()
        
 
        
if  __name__=="__main__":
    print("Running")
    index=index_builder()
    index.run()
    print("Done")

