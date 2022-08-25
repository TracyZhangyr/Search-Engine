from bs4 import BeautifulSoup
from bs4.element import Comment
import nltk


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'meta']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    result = u" ".join(t.strip() for t in visible_texts)
    return result.splitlines()


class Document:
    def __init__(self, docID: int, url: str):
        self.docID = docID
        self.url = url
        self.num_of_cites = 0
        self.content = self.get_content_from_path(docID)
        
    
    def get_content_from_path(self, docID) -> ["string"]:
        list_of_string = []
        
        try:
            directory_path = self.change_to_directory_path(docID)
            with open(directory_path, 'rb') as file:
                list_of_string = text_from_html(file)
        except Exception as ex:
            print(ex)
        finally:
            if file is not None:
                file.close()
        return list_of_string
  
                
    def change_to_directory_path(self, docID: int) -> str:
        directory_path = "WEBPAGES_RAW\\" + docID.replace('/', '\\')
        return directory_path
    
    
    def find_number_of_citation(self, soup):
        cite_list = soup.find_all("cite")
        if (cite_list):
            self.num_of_cites = len(soup.find_all("cite"))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    