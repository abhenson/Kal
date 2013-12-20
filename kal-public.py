
#kal-public.py writen by A.B.Henson January 2013.
#the script goes to the economist website, gets the redirect url of that week's issue, then it extracts the locating of the Kal's cartoon image and saves it. It uses gmail as the SMTP server to email the cartoon to my email address.
#script has been altered to remove private data like username and password so it can be placed online, renamed kal-public.py
from bs4 import BeautifulSoup
import re
import requests
import urllib.request
from email.mime.image import MIMEImage
import smtplib
#the url to begin with, it will automatically redirect to the url for the current issue
firstURL='http://www.economist.com/printedition'
response1 = requests.get(firstURL)
#send the text of the response to Beautiful soup, creates an object to work with
soup = BeautifulSoup(response1.text)
#getting the date of the issue to use for the file name from the first soup object
currentIssue=soup.find("h1").find_all('span')[1].get_text()
#open last issue.txt and then check if this is a new issue or not
f=open('/home/alon/python/Kal/last issue.txt','r+')
oldIssue=f.read().strip()
if oldIssue!=currentIssue:
	#have to run a for so that the object found is a tab, if i just use a find without the
	#for i'll get a result set which doesn't have the get method i need
	for i in soup.findAll('a',text=re.compile('KAL\'s cartoon')):
		i.findAll('a',{'class':'node-link'})
	#getting the url link
	iURL=i.get('href')
	#creating the full path i need
	thirdURL='http://www.economist.com'
	thirdURL += iURL

	response3=requests.get(thirdURL)
	soup2=BeautifulSoup(response3.text)
	#run the for this time to get the location of the image
	for i in soup2.findAll('div',{'class':'content-image-full'}):
    		i.findAll('img')
	#get the src/url of the image
	imgURL=i.contents[1].get('src')
        #location of directory where images are saved	
	imgName='/home/user/python/Kal/images/'
	imgName+=currentIssue
	imgName+='.jpg'
	urllib.request.urlretrieve(imgURL, imgName)

	#create an email message to send
	msg = MIMEImage(open(imgName,'rb').read())
	msg['Subject'] = 'Kal\'s cartoon'
	msg['From'] = 'your script'
	msg['To'] = 'mail@domain.com'
	#user name and password for a gmail account i made especially for this
	username = 'username@domain.com'
	password = 'password'
	#using gmail as my SMTP server
	server = smtplib.SMTP('smtp.gmail.com:587')
	#must have this extended hello as part of setting up the connection
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.send_message(msg)
	server.quit()
	#clear file and then save current issue to it
	f=open('/home/user/python/Kal/last issue.txt','r+')
	f.truncate()
	f.write(currentIssue)
	f.close()
else:
	f.close()

