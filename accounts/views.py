from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
# Create your views here.
from django.contrib import messages
from urllib.request import urlopen
from bs4 import BeautifulSoup
from .models import Article



def home(request):
	return render(request,'home.html')

def register(request):

	if request.method == 'POST' :
		first_name = request.POST['first_name']	
		second_name = request.POST['second_name']	
		username = request.POST['username']	
		email = request.POST['email']
		password1 = request.POST['password1']	
		password2 = request.POST['password2']

		if password1 == password2:
			if User.objects.filter(username=username).exists():
				messages.info(request,'username taken')
				return redirect('register')
			elif User.objects.filter(email=email).exists():
				messages.info(request,'email taken')
				return redirect('register')
			else:
				user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=second_name)
				user.save()
				print('user_created')
				return redirect('login')
		else:
			messages.info(request,'password not matching')
			return redirect('register')

		return redirect('/')
		
	else:
		return render(request,'register.html')

def login(request):
	if request.method == 'POST':
		username = request.POST['username']	
		password = request.POST['password']

		user = auth.authenticate(username=username,password = password)	
		
		if user is not None:
			auth.login(request,user)
			return redirect ('dashboard')
		else:
			messages.info(request,'invalid login')
			return redirect('login')
	else:
		return render(request,'login.html')

def logout(request):
	auth.logout(request)
	return redirect('/')

def read(request):
	if request.method == 'POST':
		read_url = request.POST['read_button']
		username = read_url.split(' ')[1]
		read_url = read_url.split(' ')[0]
		url_obj = Article.objects.get(url=read_url)
		user_read = url_obj.user_read
		print(type(user_read))
		user_read.append(username)
		Article.objects.filter(url=read_url).update(user_read= user_read)
		return redirect('dashboard')
	else:
		return redirect('dashboard')

def delete(request):
	if request.method == 'POST':
		del_url = request.POST['delete_button']
		username = del_url.split(' ')[1]
		del_url = del_url.split(' ')[0]
		url_obj = Article.objects.get(url=del_url)
		user_deleted = url_obj.user_deleted
		print(type(user_deleted))
		user_deleted.append(username)
		Article.objects.filter(url=del_url).update(user_deleted= user_deleted)
		return redirect('dashboard')
	else:
		return redirect('dashboard')

def dashboard(request):

	for page in range(1,4):
		my_url = 'https://news.ycombinator.com/news?p=' + str(page)
		uClient = urlopen(my_url)
		page_html = uClient.read()
		uClient.close()
		page_soup = BeautifulSoup(page_html,'html.parser')
		containers_1 = page_soup.findAll('tr',{"class": 'athing'})
		containers_2 = page_soup.findAll('td',{"class": 'subtext'})
		for i in range(0,30):
			title = containers_1[i].findAll('td',{'class':'title'})
			url = title[1].a['href']
			if not Article.objects.filter(url=url).exists():
				try:
					hacker_news_url = 'https://news.ycombinator.com/item?id=' + containers_1[i].a['id'].split('_')[1]
				except:
					hacker_news_url = ''
				dummy = containers_2[i].findAll('span',{})
				try:
					upvotes = dummy[0].text
					posted_on = dummy[1].text
				except:
					upvotes = '0 points'
					posted_on = dummy[0].text
				dummy = containers_2[i].findAll('a',{})
				try:
					comments = dummy[-1].text
				except:
					comments = '0 comments'
				if comments=='discuss' or comments=='hide':
					comments = '0 comments'
				if upvotes.split(' ')[-1] != 'points' and upvotes.split(' ')[-1] != 'point':
					upvotes = '0 points'	
				
				age_split = posted_on.split(' ')
				age = 0
				if age_split[1] == 'minutes':
					age = int(age_split[0])
				elif age_split[1] == 'hours' or age_split[1] == 'hour':
					age = int(age_split[0])*60
				elif age_split[1] == 'day' or age_split[1] == 'days' :
					age = int(age_split[0])*60*24

				a = Article(url=url,hacker_news_url= hacker_news_url,posted_on= posted_on,upvotes= upvotes ,comments= comments, age = age)
				a.save()
			else:
				dummy = containers_2[i].findAll('span',{})
				try:
					upvotes = dummy[0].text
				except:
					upvotes = '0 points'
				dummy = containers_2[i].findAll('a',{})
				try:
					comments = dummy[-1].text
				except:
					comments = '0 comments'
				if comments=='discuss' or comments=='hide':
					comments = '0 comments'
				if upvotes.split(' ')[-1] != 'points' and upvotes.split(' ')[-1] != 'point':
					upvotes = '0 points'	
				Article.objects.filter(url=url).update(upvotes= upvotes ,comments= comments)

	articles = Article.objects.all().order_by('age')
	return render(request,'dashboard.html',{'articles': articles})
