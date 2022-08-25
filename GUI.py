import tkinter
from SearchEngine import start_search
from SearchEngine import load_dict
import webbrowser


WORD_DICT = load_dict("WordList.txt")

class Gui(object):
    def __init__(self):
        self.root = tkinter.Tk()
        
        # set the title
        self.root.title("ICS Search Engine")
        
        # create a search/input bar
        self.user_input = tkinter.Entry(self.root, width = 70)

        # create a display list
        self.display_info = tkinter.Listbox(self.root, width = 100, height = 50)
        self.display_info.bind("<Double-Button-1>" , self.CallOn)

        # create a search button
        self.search_button = tkinter.Button(self.root, command = self.get_result, text = "Search")

    def gui_arrang(self):
        self.user_input.pack()
        self.search_button.pack()
        self.display_info.pack()

    def get_result(self)->None:
        # get input
        self.search_query = self.user_input.get()
        top_url_and_descrip_list = start_search(self.search_query, WORD_DICT)
        # clear the display list
        self.display_info.delete(0,'end')

        # print the result
        line = 0
        for i in top_url_and_descrip_list:
            self.display_info.insert(line, i[0])
            self.display_info.insert(line + 1, i[1])
            self.display_info.insert(line + 2, "")
            line += 3

    def CallOn(self, event):
        url = self.display_info.get(self.display_info.curselection())
        webbrowser.open_new(url)

def main():
    # initialize
    FL = Gui()
    # make arrangment
    FL.gui_arrang()
    # run main process
    tkinter.mainloop()
    pass


if __name__ == "__main__":
    main()
