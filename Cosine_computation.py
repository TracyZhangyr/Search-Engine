from nltk.corpus import stopwords
from WordList import common_line_num
import math
from collections import defaultdict
from queue import PriorityQueue
import WordList
import re

STOPWORDS = set(stopwords.words('english'))

class Score:
    def __init__(self,docID:str,total_score:float):
        self.docID = docID
        self.total_score = total_score
    
    def __lt__(self,other):
        if self.total_score <= other.total_score:
            return False
        else:
            return True

class Cosine_computation:
    def __init__(self, query_list:[], word_dict: dict):
        self.query_list = self.tokenize_query_list(query_list)
        self.word_dict = word_dict
        self.query_frequence_dict = self.get_query_frequency()
        self.total_score_dict = self.score_with_no_cos()
        self.score_priotiy_queue = self.score_priotiy_queue()


        #dict{"word":{"docID":{"tf-idf":float,"line_num":[int],"cite":int}}}
    
    def score_priotiy_queue(self)->PriorityQueue:
        pq = PriorityQueue()
        for docID,total_score in self.total_score_dict.items():
            pq.put(Score(docID,total_score))
        return pq

        
    def score_with_no_cos(self)->dict:
        total_score_dict = dict()
        select_doc_dict = dict()
        
        for query in set(self.query_list):
            if query in self.word_dict.keys():      
                for docID, inner_dict in self.word_dict[query].items():
                    select_doc_dict[docID] = {query: inner_dict}
                    # dict{"docID": {"tf-idf":float,"line_num":[int],"cite":int}
            
                for docID, inner_dict in select_doc_dict.items():
                    total_score = 0
                    for term in inner_dict.keys():
                        total_score += inner_dict[term]["tf-idf"]
                    total_score_dict[docID] = total_score
        
        for docID, inner_dict in select_doc_dict.items():
            line_num_list = []
            temp = 0
            cite = 0
            
            for term in inner_dict.keys():
                if temp == 0:
                    cite = select_doc_dict[docID][term]["cite"]  #get cite for one time
                line_num_list.append(select_doc_dict[docID][term]["line_num"])  #get list of list_num
            line_num_score = self.get_line_num_score(line_num_list)
            cite_score = self.get_cite_score(cite)
            total_score_dict[docID] = total_score_dict[docID] + line_num_score + cite_score       
        return total_score_dict 
  
    
    def ranking(self) -> dict:
        #score_dict = defaultdict(float)
        #query_length = len(query_list)
        query_normalization_vector = dict()
        doc_normalization_vector = defaultdict(dict)
        cosine_score_dict = dict()
        total_score_dict = dict()
        
        for query in set(self.query_list):
            query_frequency = self.query_frequence_dict[query]
            query_normalization_vector[query] = query_frequency/self.get_query_normalization(self.query_list)  #query_normalization    
    
            if query in self.word_dict.keys():      
                for docID, inner_dict in self.word_dict[query].items():
                    doc_normalization_vector[docID] = {query: inner_dict}
                    # dict{"docID": {"tf-idf":float,"line_num":[int],"cite":int}
            
                for docID, inner_dict in doc_normalization_vector.items():   #term_normalization
                    total_score = 0
                    cosine_score = 0
                    for term in inner_dict.keys():
                        total_score += inner_dict[term]["tf-idf"]**2
                    tf_idf_score_normalization = math.sqrt(total_score)
                    for term in inner_dict.keys():
                        inner_dict[term]["tf-idf-normal"] = inner_dict[term]["tf-idf"]/tf_idf_score_normalization
                        cosine_score += inner_dict[term]["tf-idf-normal"] * query_normalization_vector[term]
                    cosine_score_dict[docID] = cosine_score
                    # dict {"docID": cosine_score}
############################################# cosine score ############################################
        
        for docID, inner_dict in doc_normalization_vector.items():
            line_num_list = []
            temp = 0
            cite = 0
            
            for term in inner_dict.keys():
                if temp == 0:
                    cite = doc_normalization_vector[docID][term]["cite"]  #get cite for one time
                line_num_list.append(doc_normalization_vector[docID][term]["line_num"])  #get list of list_num
            line_num_score = self.get_line_num_score(line_num_list)
            cite_score = self.get_cite_score(cite)
            total_score_dict[docID] = cosine_score_dict[docID] + line_num_score + cite_score
        #return sorted(total_score_dict.keys(), key=lambda x: total_score_dict[x], reverse=True)
        return total_score_dict
    
    def tokenize_query_list(self, query_list)->list:
        new_list = []
        for query in query_list:
            if (query not in STOPWORDS):
                new_list.append(query)
        
        for query in new_list:
            re.sub("[^A-Za-z0-9]","",query)
            query.lower()
            
        return new_list
    
    def get_query_frequency(self):
        frequency_dict = defaultdict(int)
        for query in self.query_list:
            frequency_dict[query] += 1
        for key, value in frequency_dict.items():
            df = 1
            if key in self.word_dict.keys():
                df += len(self.word_dict[key].keys())
            frequency_dict[key] = WordList.tfidf(value,df,37497)
        return frequency_dict

    def get_query_normalization(self, query_frequency: int):
        total_num = 0
        for query in self.query_frequence_dict.values():
            total_num += query**2
        return math.sqrt(total_num)
    
    def get_line_num_score(self, number_list: list):
        data = common_line_num(number_list)
        return data[0] / len(self.query_list) 
    
    def get_cite_score(self, cite: int):
        return cite * 0.05
        