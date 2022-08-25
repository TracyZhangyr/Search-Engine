from Document import Document
import WordList
from collections import defaultdict
import json
from builtins import input
import Cosine_computation
from queue import PriorityQueue



def get_list_of_document(document_path: str)->list:
    list_of_Document = []
    d = load_dict(document_path)
    for k, v in d.items():
        list_of_Document.append(Document(k, v))
    return list_of_Document


def indexing(index_dict:dict,doc_list:["Document"])->None:
    total_doc_num = len(doc_list)
    for doc in doc_list:
        WordList.update_index_dict(index_dict,doc)
    WordList.calculate_tfidf(index_dict,total_doc_num)

def write_dict(d:dict, file_name:str)->None:
	js = json.dumps(d)   
	file = open(file_name, 'w+')  
	file.write(js)  
	file.close()

def load_dict(file_name:str)->dict:
	file = open(file_name, 'r') 
	js = file.read()
	d = json.loads(js)    
	file.close() 
	return d

#return ["url","description"]
def get_url_and_descrip(docID:str)->["url","descrip"]:
    result = []
    path = "WEBPAGES_RAW\\bookkeeping.json"
    doc_dict = load_dict(path)
    url = doc_dict[docID]
    result.append(url)
    doc = Document(docID,url)
    descrip = ""
    for line in doc.content:
        if len(descrip) < 100:
            line.rstrip()
            if len(descrip) + len(line) < 100:
                descrip = descrip + " " + line
            else:
                line_len = 100 - len(descrip)
                descrip += line[:line_len]
            descrip.lstrip()
        else:
            break
    descrip.strip()
    result.append(descrip)
    return result
            
def generate_top_urls(docIDs:["docID"])->[["url","descrip"]]:
    return [get_url_and_descrip(docID) for docID in docIDs]  

def write_report_part_2(file_name:str,result:[("query",int,["docID"])]):
    output = open(file_name,'w+')
    for pair in result:
        query = pair[0]
        num_of_url_retrieved = pair[1]
        docID_list = pair[2]
        print("Query: {}".format(query),file=output)
        print("Number of URLs retrieved: {}".format(num_of_url_retrieved),file=output)
        print("Top 20 URLs:",file=output)
        for docID in docID_list:
            url = get_url_and_descrip(docID)[0]
            print(url,file=output)
        print("\n",file=output)
    output.close()

#Need to test    
def generate_report_part_2(file_name:str):
    report_query_list = ["Informatics","Mondego","Irvine",
                         "artificial intelligence","computer science"]
    result = []
    WORD_DICT = load_dict("WordList.txt")
    for query in report_query_list:
        query_list = get_user_query(query)
        computation = Cosine_computation.Cosine_computation(query_list, WORD_DICT)
        total_score_dict = computation.total_score_dict
        num_of_url_retrieved = len(total_score_dict.keys())
        score_pq = computation.score_priotiy_queue
        top_k_docs_list = produce_top_K_doc_list(score_pq, 20) #get the top 20 docs
        result.append((query,num_of_url_retrieved,top_k_docs_list))
         
    write_report_part_2(file_name, result)


def get_user_query(query:str) -> list:
    user_input = query.lower()
    query_list = user_input.rstrip().split()
    return query_list

# def get_user_input_query() -> list:
#     query = str(input("Please type your query: "))
#     query_list = get_user_query(query)
#     return query_list

def produce_top_K_doc_list(score_pq:PriorityQueue,K:int)->["docID"]:
    doc_list = []
    for i in range(K):
        if not score_pq.empty():
            doc = score_pq.get_nowait()
            doc_list.append(doc.docID)
    return doc_list

def generate_word_dict()->None:
    new_list = get_list_of_document("WEBPAGES_RAW\\bookkeeping.json")
    #dict{"word":{"docID":{"tf-idf":float,"line_num":[int],"cite":int}}}
    index_dict = defaultdict(dict)
    indexing(index_dict,new_list)
    write_dict(index_dict, "WordList.txt")
    #d = load_dict("WordList.txt")
    print(len(index_dict.keys()))

def start_search(user_input:str, WORD_DICT:dict)->list:
    query_list = get_user_query(user_input)
    computation = Cosine_computation.Cosine_computation(query_list, WORD_DICT)
    total_score_dict = computation.total_score_dict
    score_pq = computation.score_priotiy_queue #priority queue that stores all the docID with score
    top_k_docs_list = produce_top_K_doc_list(score_pq, 20) #e.g. get the top 20 docs
    #[["url","descrip"]]
    top_url_and_descrip_list = generate_top_urls(top_k_docs_list)
    return top_url_and_descrip_list
    

if __name__ == "__main__":
    #generate_word_dict()
   
    
    #Use for test before the GUI done 
    # input_query = str(input("Please type your query: "))
    # query_list = get_user_query(input_query)

    #Create report.pdf part 2 only (not finished)
    generate_report_part_2("Report_Part_2.txt")
    
    

    
    
