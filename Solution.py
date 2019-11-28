import urllib
import re
import spacy
from spacy import displacy
import en_core_web_sm
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import json
import datetime
import warnings
import re
import os
warnings.filterwarnings('ignore')


def remove_tags(text):
	return ''.join(ET.fromstring(text).itertext())

def get_detailsfromlink(i):
	title='';Qulification='';by='';role='';place=''
	soup = bs(urllib.request.urlopen(i).read().decode("utf-8"))
	title=soup.find_all("h1", class_="job-title")
	role=soup.find_all("div", class_="wysiwyg",itemprop='responsibilities')
	Qulification=soup.find_all("div", class_="wysiwyg",itemprop='qualifications')
	by=soup.find_all("h3", class_="details-title")
	place=soup.find_all("span",class_="job-detail")
	if len(title)!=0 :
	    title=remove_tags(title[0].encode('utf-8'))
	if len(Qulification)!=0:
	    Qulification=remove_tags(Qulification[0].encode('utf-8'))
	if len(role)!=0:
	    role=remove_tags(role[0].encode('utf-8'))
	if len(place)!=0:
	    place=remove_tags(place[0].encode('utf-8'))
	if len(by)!=0:
	    by=remove_tags(by[0].encode('utf-8'))
	return title,Qulification,role,place,by

def process_function(link_data="https://www.cermati.com/karir/"):
	print('Please wait data is geting processed ....!! ')
	response = urllib.request.urlopen('https://www.cermati.com/karir/')
	html = response.read()
	html=html.decode("utf-8")
	html=html.replace('\n','')
	soup = bs(html)

	pat_main ='(?<=\<div class="tab-content">).+?(?=\<div class="row">)'
	op_list=re.findall(pat_main,html)
	pat_Dep = '(?<=\<h4 class="tab-title">).+?(?=\</h4>)'
	op_list_=re.findall(pat_Dep, op_list[0])

	print('I can see your data have ', len(op_list_), 'Department -->')
	print(op_list_)

	each_dip=[]
	for i in range(len(op_list_)):
	    i="tab"+str(i)
	    each_dip.append(soup.find_all("div", {"id": i})[0])

	each_dip_data=[]
	for i in range(len(each_dip)):
	    soup = bs(str(each_dip[i]))
	    each_dip_data.append(soup.find_all("div", class_="dept-label col-sm-7"))

	each_dip_data_link=[[] for i in range(len(op_list_))]
	for i in range(len(op_list_)):
	    soup = bs(str(each_dip[i]))
	    for link in soup.findAll("a"):
	        each_dip_data_link[i].append(link.get("href"))

	full_data={}
	for i in op_list_:
	    full_data[i]=[]
	    print('------------------->')
	    print(datetime.datetime.now())
	    print('Department "'+i+ '" is getting Processed ...!! ')
	    for j in range(len(each_dip_data_link)):
	        for k in each_dip_data_link[j]:
	            k=str(k).replace(' ','%20')
	            try:
	                title,Qulification,role,place,by=get_detailsfromlink(k)
	                temp={"title":title,"location":place,"description":role,"qualification":Qulification,"posted by":by}
	                full_data[i].append(temp)
	            except:
	                
	                print('I can see there was a error with "', end='') 
	                print(k, end='')
	                print('" link')
	                print('<-----------')
	return full_data

def save_data(full_data):
	answer=json.loads(json.dumps(full_data))
	with open('Solution.json', 'w') as outfile:
	    json.dump(answer, outfile)

	print('Your Data has been saved in "',end='')
	print(os.getcwd() +'" Directory with Json File as "Solution.json"')


if __name__=='__main__':
	link_data=input('Please provide the link you want to use:\n')
	save_data(process_function(link_data))