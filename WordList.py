from nltk.corpus import stopwords
from collections import defaultdict
import math

STOPWORDS = set(stopwords.words('english'))

def add_element(token:str, line_num:int, d:dict):
	if token not in STOPWORDS:
	    if d.get(token) == None:
	        d[token] = [1, {line_num}]
	    else:
	        d[token][0] += 1
	        d[token][1].add(line_num)

                
def count_words(content:list) -> dict: #Dict{str:[int, set{int}]}
    d = {}
    line_num = 0
    for line in content:
        line_num += 1
        start_pointer = 0
        end_pointer = 0
        for l in line:
            if l.isalnum():
                end_pointer += 1
                if end_pointer == len(line):
                    add_element(line[start_pointer:].lower(), line_num, d)
            else:
                if end_pointer - start_pointer == 0:
                    end_pointer += 1
                    start_pointer = end_pointer
                else:
                    token = line[start_pointer:end_pointer].lower()
                    add_element(token, line_num, d)
                    end_pointer += 1
                    start_pointer = end_pointer
    return d

def common_line_num(l:list) -> list: #l is the list of sets of line numbers, returns the max count of common line numbers
    d = {}
    searched_set = set()
    result = 0
    counter = 1

    for s in l:
        for line_num in s:
            if line_num not in searched_set:
                searched_set.add(line_num)
                max_lines = 0
                for line_num_set in l:
                    if line_num in line_num_set:
                        max_lines += 1
                if max_lines > result:
                    result = max_lines
                    counter = 1
                elif max_lines == result:
                    counter += 1

    return [result, counter]


def idf(doc_num:int,df:float)->float:
    return math.log10(doc_num/df)

def tfidf(tf:int,df:int,doc_num:int)->float:
    return (1 + math.log10(tf)) * idf(doc_num,df)

def calculate_tfidf(index_dict:dict,total_doc_num:int):
    for word,doc_dict in index_dict.items():
        df = len(doc_dict.keys())
        for id,doc_info in doc_dict.items():
            doc_info["tf-idf"] = tfidf(doc_info["tf-idf"],df,total_doc_num)

	
#update index_dict with cite_num,line_num,term_freq
def update_index_dict(index_dict:dict,doc:"Document"):
    doc_id = doc.docID
    num_of_cites = doc.num_of_cites
    doc_dict = count_words(doc.content)
    
    for word,pair in doc_dict.items():
        freq = pair[0]
        index_dict[word][doc_id] = defaultdict(dict)
        d = index_dict[word][doc_id]
        d["line_num"] = list(pair[1])
        #store the tf temporarily
        d["tf-idf"] = freq 
        d["cite"] = num_of_cites


