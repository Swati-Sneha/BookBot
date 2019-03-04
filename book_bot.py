<<<<<<< HEAD
'''This chatbot is meant to serve following use cases: 
a.suggest upto three books for asked genre
b.give the name of the author of the book
c.give the url of the book by appending the isbn no. to https:/openlibrary.org/
d.list few genres from the data

Type bye or its synonyms to exit'''

'''The data has been scraped from https://fbookshelf.herokuapp.com/ and converted to pickle format'''

#coding: utf-8


from fuzzywuzzy import fuzz, process
import nltk
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys, random
from nltk.corpus import wordnet as wn
import pickle
import json
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='temp/book_chatbot.log',
                    filemode='w')



def genrebook(genre, book_dict):
	
	"""Checks if books of the genre are available or not and if present they are greater than 3 or less.
	If less than 3, outputs any one recommendation"""
	
	
	if (genre in book_dict):
		logging.info("Genre %s is present" %(genre))
		genre_books = book_dict[genre]
		books = ""
		book_details = []
		if (len(genre_books)<3):
			book = genre_books[0]
			books= book['name']
			book_details.append(book)
			logging.info('Less than three books of genre %s is present. Suggested book for the genre %s' %(genre, book_details))
		else:
			for i in range(3):
				book = np.random.choice(genre_books)
				if (i<2):
					books+= book['name']+","
				elif(i==2):
					books+= book['name']+"."
				book_details.append(book)
				genre_books.remove(book)
				logging.info("three books of genre %s is present. Suggested book for the genre %s" %(genre, book_details))
		response ="For genre "+genre+" I found books:: "+books
	else:
		response= "Could not find any book for genre "+genre
		logging.info('Genre %s not found' %(genre))
	return response, book_details

	
def greet(greeting, greet_list):

	'''Handles salutations-hellos and byes. Returns responds for salutations'''
	
	salutations = ["How may I help you?", "What can I do for you?", "What genre book would you like me to search for you?"]
	bye_sals = ["Nice talking to you", "Happy reading", "Come again soon" ]
	try:
		if (greeting == "hi"):
			response = np.random.choice(greet_list)+"! I am book assistant. I can recommend books on genre. "+np.random.choice(salutations)
		elif (greeting == "bye"):
			response = np.random.choice(greet_list)+"! "+np.random.choice(bye_sals)
	except:
		logging.info("Greeting %s not handled in the function greet" %(greeting))
		response="I am extremely sorry but I am not feeling well at all. Come again some other time please. Hope you understand!"
		exit(0)
	finally:
		return (response)
	
def get_synList(word):

	'''Returns list of synonymous words for the passed word'''
	
	wordsynset = wn.synsets(word)
	wordList = []
	for words in wordsynset:
		for lemma in words.lemmas():
			wordList.append(lemma.name())
	return (wordList)
	
def main():
	
	
	'''Reading pkl file'''
	
	try:
		f = open('book_data.pkl', 'rb') 
		book_dict = pickle.load(f)
		f.close()
	except Exception as e:
		logging.info(e)
		exit(0)
	
	'''Final list of possible inputs for use cases-salutations, author details, link details, genre_books'''
	
	
	hellos = [x.replace("_", " ").replace("-"," ")  for x in set(get_synList("Hello"))]+['hi there', 'hello there']
	byes = [x.replace("_", " ").replace("-"," ")  for x in set(get_synList("Bye"))]
	show_author_details = ["author details", "who is the author", "who are authors", "show me authors"]
	show_link_details = ["link to read the book", "link of the book", "link for the book", "link for reading book"]
	show_genres_books=["show me books on", "read book on", "list me books for", "suggest me books on", "recommend me book on", "get me book from", "list some books on", "list a few books on", "list books on genre"]
	list_genres=["list me some genres", "show me some genres", "list me a few genres", "show me a few genres", "suggest some genres", "suggest a few genres"]
	thankyou = [x.replace("_", " ").replace("-"," ")  for x in set(get_synList("Thanks"))]+["thank you","thanku"]

	book_genres = [k.lower() for k in book_dict]  

	print('Welcome to chatbot')
	while True:
		input_res = input('You:').lower()
		
		'''Calculating the match score of input with the use cases, to handle any possible deviation of the input'''
		
		thankyou_scores = [fuzz.partial_ratio(input_res, x) for x in thankyou]
		hello_scores = [fuzz.partial_ratio(input_res, x) for x in hellos]
		show_Author_scores = [fuzz.partial_ratio(input_res, x) for x in show_author_details]
		show_genres_scores = [fuzz.partial_ratio(input_res, x) for x in show_genres_books]
		show_link_scores = [fuzz.partial_ratio(input_res, x) for x in show_link_details]
		list_genre_score= [fuzz.partial_ratio(input_res, x) for x in list_genres]
		
		
		'''Handling the expected use cases'''
		
		if input_res in byes:
			print ('Book Asst:'+greet('bye', byes))
			logging.info('Exiting as input received is %s' %(input_res))
			exit(0)

		elif any(x >= 80 for x in hello_scores):
			logging.info("Hello score is greater than 80")
			print ('Book Asst:'+ greet('hi', hellos))

		elif any(x >= 80 for x in show_genres_scores):
			logging.info("Genre is greater than 80")
			words = input_res.split(" ")
			genre  = [word for word in words if word in book_genres]
			try:
				genre  = [word for word in words if word in book_genres]
				response, book_details = genrebook(genre[0].capitalize(), book_dict)
				print('Book Asst:'+response)
			except Exception as e:
				logging.info(e)
				print('Book Asst: Your genre is not listed with me. Come again another time')

		elif any(x >= 80 for x in show_Author_scores):
			logging.info("show_Author_scores greater than 80")
			try: 
				book_authors = [book_detail['author'] for book_detail in book_details]
				print('Book Asst: Author for your latest search is '+book_authors[-1])
			except Exception as e:
				logging.info(e)
				print('Book Asst: Please search for books in suitable genre first')

		elif any(x >= 80 for x in show_link_scores):
			logging.info("show_link_scores greater than 80")
			try:
				book_links = [book_detail['isbn'] for book_detail in book_details]
				print('Book Asst: Link for your latest search is https:/openlibrary.org/'+book_links[2])
			except Exception as e:
				print(e)
				logging.info(e)
				print('Book Asst: Please search for books in suitable genre first')

		elif any(x >= 80 for x in list_genre_score):
			logging.info("list_genre_score greater than 80")
			try:
				complete_genre=[word for word in book_genres if word not in ['none']]
				genres = random.sample(complete_genre, 5)
				print("Book Asst: Few genres that we have are: %s, %s, %s, %s, %s"%(genres[0], genres[1], genres[2], genres[3], genres[4]))
				logging.info("Genres listed")
			except Exception as e:
				print(e)
				logging.info(e)
				print("I am sorry, I am not able to understand your question. Please try again")
				
		elif any(x >= 80 for x in thankyou_scores):
			logging.info("Thank you score greater than 80")
			response = ["Welcome", "Happy to help", "See you soon", "My pleasure", "Mention not"]
			print('Book Asst:'+np.random.choice(response))
			
			'''Handling out of the box use cases, by calculating the sentiment polarity of input as positive, negative or neutral'''
			
			
		else:
			sid = SentimentIntensityAnalyzer()
			ss = sid.polarity_scores(input_res)
			logging.info("%s has a polarity score of %s"%(input_res, ss))
			if(ss['neg']>0.6):																							#negative
				response= ["I am sorry", "That's sad", "Pathetic!"]

			elif(ss['pos']>0.6):																						#positive
				response = ["Wow", "That's a good news", "Great!"]

			else:																										#neutral
				response = ["Hmm", "That's interesting", "I did not know that", "I see"]

			print('Book Asst:'+np.random.choice(response))


if __name__=="__main__":		
	main()