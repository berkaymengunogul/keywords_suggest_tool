import re
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from tkinter import *
from stop_words import get_stop_words
for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'News', 'com', 'div', 'script', 'tiktok', 'twitter']:
    get_stop_words('english').append(month.lower())


class GUI:
    def __init__(self, master):
        self.master = master
        master.title('Virallinq Tool')
        master.configure(background='#F4F6F6')
        self.scrapper = Scrapper()

        self.link_variable = StringVar()
        self.entry_box_link = Entry(self.master, width=105, textvariable=self.link_variable).grid(row=0, column=1, columnspan=3, padx=2, pady=(2, 12))
        self.get_results_button = Button(self.master, text='Load Keywords', width=10, height=1, command=self.get_results).grid(row=0, column=0, padx=(8, 4))

        self.label_keywords = Label(self.master, text='Keywords: ', bg='#F4F6F6').grid(row=1, column=0, padx=2, sticky=N)
        self.list_box_keywords = Listbox(self.master, width=76, height=8)
        self.list_box_keywords.grid(row=1, column=1, padx=2, pady=(4, 0), sticky=N + S + W)
        self.scrollbar_keywords = Scrollbar(self.master, orient="vertical")
        self.scrollbar_keywords.config(command=self.list_box_keywords.yview)
        self.scrollbar_keywords.grid(row=1, column=2, sticky=N + S + W)
        self.list_box_keywords.config(yscrollcommand=self.scrollbar_keywords.set)

        self.search_variable = StringVar()
        self.search_button = Button(self.master, text='Load Keywords', width=10, height=1, command=self.search).grid(row=2, column=0, padx=(8, 0))
        self.search_button = Button(self.master, text='Search', width=10, height=1, command=self.search).grid(row=2, column=0, padx=(8, 0))
        self.entry_box_search = Entry(self.master, width=75, textvariable=self.search_variable).grid(row=2, column=1, columnspan=3, padx=(2, 0), pady=(1, 0), sticky=W)

        self.label_sources = Label(self.master, text='Sources: ', bg='#F4F6F6').grid(row=1, column=3, padx=2, sticky=N)
        self.list_box_sources = Listbox(self.master, width=25, height=25)
        self.list_box_sources.grid(row=1, column=3, rowspan=4, padx=2, pady=(4, 10), sticky=S)
        self.scrollbar_sources = Scrollbar(self.master, orient="vertical")
        self.scrollbar_sources.config(command=self.list_box_keywords.yview)
        self.scrollbar_sources.grid(row=1, column=5, rowspan=4, sticky=N + S + W)
        self.list_box_sources.config(yscrollcommand=self.scrollbar_sources.set)

        self.label_process = Label(self.master, text='Process: ', bg='#F4F6F6').grid(row=3, column=0, padx=2, sticky=N)
        self.text_box_process = Text(self.master, width=97, height=10)
        self.text_box_process.grid(row=3, column=1, columnspan=2, padx=2, pady=(4, 0), sticky=W + N + S)
        self.scrollbar_process = Scrollbar(self.master, orient="vertical")
        self.scrollbar_process.config(command=self.list_box_keywords.yview)
        self.scrollbar_process.grid(row=3, column=2, sticky=N + S + W)
        self.text_box_process.config(yscrollcommand=self.scrollbar_process.set)

        self.label_results = Label(self.master, text='Results: ', bg='#F4F6F6').grid(row=4, column=0, padx=2, sticky=N)
        self.text_box_results = Text(self.master, width=97, height=10)
        self.text_box_results.grid(row=4, column=1, columnspan=2, padx=2, pady=(4, 10), sticky=W + N + S)
        self.scrollbar_results = Scrollbar(self.master, orient="vertical")
        self.scrollbar_results.config(command=self.list_box_keywords.yview)
        self.scrollbar_results.grid(row=4, column=2, sticky=N + S + W)
        self.text_box_results.config(yscrollcommand=self.scrollbar_results.set)

        master.grid()

    def search(self):
        self.scrapper.top_five = list()
        self.scrapper.sources = list(set())
        self.scrapper.links = list(set())
        self.scrapper.counter = {}
        self.scrapper.snippets = list(set())
        self.scrapper.titles = list(set())
        if len(self.search_variable.get()) < 1:
            self.text_box_process.delete('1.0', END)
            self.text_box_results.delete('1.0', END)
            self.list_box_sources.delete(0, END)
            self.scrapper.query = self.list_box_keywords.get(self.list_box_keywords.curselection())
            self.scrapper.search()
            self.scrapper.scrap()
        else:
            self.text_box_process.delete('1.0', END)
            self.text_box_results.delete('1.0', END)
            self.list_box_sources.delete(0, END)
            self.scrapper.query = self.search_variable.get()
            self.scrapper.search()
            self.scrapper.scrap()

    def get_results(self):
        self.text_box_process.delete('1.0', END)
        self.text_box_results.delete('1.0', END)
        self.list_box_sources.delete(0, END)
        self.list_box_keywords.delete(0, END)
        keywords = KeyWords()
        keywords.scrap_keywords()


class KeyWords:
    def __init__(self):
        self.indian_express_url_trending = 'https://indianexpress.com/section/trending/'
        self.keywords = list(set())

    def scrap_keywords(self):
        app.text_box_process.insert(END, 'Scrapping keywords from indianexpress.com/section/trending/ ... \n\n')
        app.text_box_process.update()
        req_trending = requests.get(self.indian_express_url_trending)
        soup = BeautifulSoup(req_trending.text, 'html.parser')
        for title in soup.find_all('h3'):
            self.keywords.append(title.get_text())
            app.list_box_keywords.insert(END, title.get_text())


class Search:
    def __init__(self):
        self.api_key = 'AIzaSyDApXO7ns8DR8P9-5uy80iuysPnkxjPVDk'
        self.search_engine_id = '000933269616900363427:bsvgchcdoyw'
        self.query = ''
        self.links = list(set())
        self.sources = list(set())
        self.snippets = list(set())
        self.titles = list(set())

    def search(self):
        app.text_box_process.insert(END, 'Searching %s on google ... \n\n' % self.query)
        app.text_box_process.insert(END, 'Collecting sources ... \n\n')
        app.text_box_process.update()
        resource = build("customsearch", 'v1', developerKey=self.api_key).cse()
        result = resource.list(q=self.query, cx=self.search_engine_id).execute()
        for item in result['items']:
            print(item)
            if 'yahoo' in item['displayLink']:
                pass
            else:
                self.links.append(item['link'])
                self.sources.append(item['displayLink'])
                self.snippets.append(item['snippet'])
                self.titles.append(item['title'])
        for source in self.sources:
            app.list_box_sources.insert(END, source)


class Scrapper(Search):
    def __init__(self):
        Search.__init__(self)
        self.counter = {}
        self.top_five = list()

    def scrap(self):
        for snippet in self.snippets:
            app.text_box_process.insert(END, 'Scrapping %s  ... \n\n' % 'snippet')
            app.text_box_process.see('end')
            app.text_box_process.update()
            # req_link = requests.get(link)
            # soup = BeautifulSoup(req_link.text, 'html.parser')
            # blacklist = ['style', 'script']
            # page = ' '.join(t for t in soup.find_all(text=True) if t.parent.name not in blacklist)
            # page = re.sub(r'\W', ' ', page)
            # page = re.sub(r'\d', ' ', page)
            # page = re.sub(r"\b[a-zA-Z]\b", "", page)
            new_words = [x.lower() for x in snippet.split()]
            filtered_words = [word for word in new_words if word not in get_stop_words('english')]
            for word in filtered_words:
                if word in self.counter:
                    self.counter[word] += 1
                else:
                    self.counter[word] = 1
        for title in self.titles:
            new_words_2 = [y.lower() for y in title.split()]
            filtered_words_2 = [word for word in new_words_2 if word not in get_stop_words('english')]
            for word in filtered_words_2:
                if word in self.counter:
                    self.counter[word] += 1
                else:
                    self.counter[word] = 1


        app.text_box_process.insert(END, 'Scrapping is done  ... \n\n')
        sorted_dictionary = {k: v for k, v in sorted(self.counter.items(), key=lambda x: x[1], reverse=True)}
        self.top_five = list(sorted_dictionary.keys())[:5]
        app.text_box_process.insert(END, 'Top 5 words:\n  %s ... \n\n' % ', '.join(['%s:%s' % (key, value) for (key, value) in list(sorted_dictionary.items())[:5]]))
        app.text_box_process.see('end')
        print(sorted_dictionary)

        app.text_box_results.insert(END, 'Aliexpress: \n')
        for word in self.top_five:
            app.text_box_results.insert(END, word+': '+'https://tr.aliexpress.com/wholesale?catId=0&initiative_id=SB_20200117012402&SearchText=%s\n\n' % word)


root = Tk()
app = GUI(root)
root.mainloop()

