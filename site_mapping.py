"""
Muhammad Sadeq Esmaeilian
Project
"""


from urllib.request import urlopen,FancyURLopener
import bs4
import re
import networkx as nx
import tld
import time
import numpy as np
import matplotlib.pyplot as plt



class MyOpener(FancyURLopener):
    version = 'My new User-Agent'
myopener = MyOpener()

def url():
    while True:
        url = str(input('Please Enter the URL :'))
        # run_time = int(input('Enter the runtime period that you want to crawl;? :'))

        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', re.IGNORECASE)

        regex2 = re.compile(r'(?:.com|.net|.org|.ac|.uk|.us|.ca|.ir|.fr|.it|.gr|)$', re.IGNORECASE)

        if re.match(regex, url) is not None:
            if re.match(regex2, url) is not None:
                return [url]
            else:
                ans = input(
                    'You Entered the tld that is not in our list (.com|.net|.org|.ac|.uk|.us|.ca|.ir|.fr|.it|.gr)\n'
                    'If you want to continue Type <<Y>> or for Entering the URL once again Type <<A>> : ')
                if ans.upper() == 'Y':
                    return [url]
                else:
                    continue
        else:
            print('You Must Enter The URL in this format : http(s)://xxx.xxxxxx.xxx')
            continue




list_of_links = []
connection = []
def crawler(links):
    global list_of_links
    global connection
    global started_time
    lst = []
    connection_lst = []
    finish_time = time.time()
    while int(finish_time - started_time) < 2000:
        print(int(finish_time - started_time))
        for link in links:
            if link not in list_of_links:
                list_of_links.append(link)
                connection_lst.append(link)
                main_domain = tld.get_fld(link)
                time.sleep(1)
                try:
                    response = urlopen(link)
                except:
                    response = myopener.open(link)
                soup = bs4.BeautifulSoup(response)
                for link_1 in soup.findAll('a', attrs={'href': re.compile("^(/)")}):
                    a = link_1.get('href')
                    if '//' not in a:
                        m_url = link + a
                        lst.append(m_url)
                for link_1 in soup.findAll('a', attrs={'href': re.compile('^https://')}):
                    a = link_1.get('href')
                    if main_domain in a:
                        lst.append(a)
                for link_1 in soup.findAll('a', attrs={'href': re.compile('^http://')}):
                    a = link_1.get('href')
                    if main_domain in a:
                        lst.append(a)
            else:
                pass
        connection_lst.extend(lst)
        connection.append(connection_lst)
        return crawler(lst)

def index_cal(url,lst):
    for index, value in enumerate(lst):
        if url == value:
            return index

def adjajency_matrix_builder(url_list,connection_matrix):
    adjajency_matrix = []
    for i in range(len(url_list)):
        adjajency_matrix.append([])
    for w in adjajency_matrix:
        for s in range(len(adjajency_matrix)):
            w.append(0)
    for j in connection_matrix:
        row_index = index_cal(j[0],url_list)
        for q in j[1:]:
            column_index = index_cal(q,url_list)
            connection_matrix[row_index][column_index] = 1
    return adjajency_matrix

def graph_draw(adjajency_matrix):
    numpy_matrix = np.matrix(adjajency_matrix)
    graph = nx.from_numpy_matrix(numpy_matrix)
    nx.draw_random(graph)
    plt.show()

started_time = time.time()
m_url = url()
crawler(m_url)


# adjajency_matrix = adjajency_matrix_builder(list_of_links,connection)
# graph_draw(adjajency_matrix)





# print(a)
# def crawler(links):
#     counter = 0
#     main_lst = []
#     for link in links:
#         if link[1] == 'F':
#             url = link[0]
#             main_domain = tld.get_fld(url)
#             response = urlopen(url)
#             soup = bs4.BeautifulSoup(response)
#             counter += 1
#             lst = []
#             for link in soup.findAll('a', attrs={'href': re.compile("^(/)")}):
#                 a = link.get('href')
#                 if '//' not in a:
#                     created_url = url + a
#                     description = [created_url, 'F']
#                     lst.append(description)
#             for link in soup.findAll('a', attrs={'href': re.compile('^https://')}):
#                 a = link.get('href')
#                 if main_domain in a:
#                     description = [a, 'F']
#                     lst.append(description)
#             for link in soup.findAll('a', attrs={'href': re.compile('^http://')}):
#                 a = link.get('href')
#                 if main_domain in a:
#                     description = [a, 'F']
#                     lst.append(description)
#             link[1] = 'T'
#             main_des = str(counter) + link[0] + 'T'
#             main_lst.append(main_des)
#             print("Main_lst :", main_lst, '\n lst :', lst)
#             return main_des, lst, crawler(lst)
#         else:
#             pass

#
# list_of_links = []
# adjajency_matrix = [[]]
# def crawler(links):
#     lst = []
#     counter = 0
#     global list_of_links, adjajency_matrix
#     for link in links:
#         if link not in list_of_links:
#             list_of_links.append(link)
#             adjajency_matrix[counter].append(1)
#             for i in adjajency_matrix:
#                 i.append(0)
#
            # main_domain = tld.get_fld(link)
            # response = urlopen(link)
            # # soup = bs4.BeautifulSoup(response)
            # for link in soup.findAll('a', attrs={'href': re.compile("^(/)")}):
            #     a = link.get('href')
            #     if '//' not in a:
            #         m_url = link + a
            #         lst.append(m_url)
            # for link in soup.findAll('a', attrs={'href': re.compile('^https://')}):
            #     a = link.get('href')
            #     if main_domain in a:
            #         lst.append(a)
            # for link in soup.findAll('a', attrs={'href': re.compile('^http://')}):
            #     a = link.get('href')
            #     if main_domain in a:
            #         lst.append(a)
#         else:




