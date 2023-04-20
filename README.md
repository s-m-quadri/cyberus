# Cyberus :anger: risk status

Cyberus is a tool to check the generic and sentimental legitimacy of the message, and it gives an approximate idea of the risk, based on the dataset, on which it has trained, and some machine learning models for predicting the risk quantitatively.

## Details

> `Category:` Safety in e-commerce
>
> `Team Members`
> 1. Shreyash Ravindra Kendre
> 2. Shaikh Abu Hayyan Muneeb
> 3. Syed Minnatullah Quadri
>
> `Class:` TY-CSE-B (B1 Batch)
>
> `Course:` Machine Learning
>
> `Date:` 25th April 2023
>
> `Guided by:` Dr. Smita S. Ponde

<br/>

## 1. Background

Consider a **scenario**, where a person receives SMS regarding a special offer. Also, an email for the enrollment procedure and a notification regarding the pending payments. At first glance, these all seem to be legitimate. Since the deadline for all this stuff is near, thus, the person is biased by the environment and the situation and doesn't have enough time to analyze the message.
	
## 2. Problem

The person doesn't know the legitimacy of the message, unsure whether to proceed or not and wants to find out the legitimacy of the message as quickly as possible. We are trying to help the person to give the risk status and make him comfortable without manual analysis of hundreds of words.

## 3. Understanding

One among the authentic and genuine methods for  decision making is to first go through the statistics, it will help us to make more objective decisions. That’s why, we'll look at statistics before even trying to solve the problem.

**Statistics -** Email spam costs businesses $20.5 billion every year. Nearly **85%** of all emails are spam. Nearly **one-third** of all data breaches in 2018 involved phishing. A new phishing site is created on the internet **every 20 seconds**. More than **70%** of phishing emails are opened by their targets. **90%** of security breaches in companies is a result of phishing attacks. Note that phishing attacks are **innocent-looking** emails, pop-ups, ads, and company communications that tempt you to click so they can install spyware, viruses, and other malware on your computer or phone.

Source:
 
1. https://dataprot.net/statistics/spam-statistics/ 
2. https://dataprot.net/statistics/phishing-statistics/

## 4. Solution

We need to somehow recognize the lexical structure of the message, analyze the link embedded in the message and figure out the legitimacy of the message.
 
Introducing **Cyberus**, a tool to check the generic and sentimental legitimacy of the message, and gives an approximate idea of the risk, based on the dataset, on which it has trained and the machine learning model.

## 5. Working

There are 3-step involved in knowing the working of Cyberus.

1. First we'll **build** two machine learning model, 

	* **Lexical analysis** of body of message
		
		Trained on spam mail and sms datasets from Kaggle, using Naive Bayes (Bag-of-words) Machine Learning Model approach with more than 75% estimated accuracy. Following are the links to datasets from Kaggle.
		
		1. https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
		2. https://www.kaggle.com/datasets/venky73/spam-mails-dataset
		
	* **URL analysis** for links embedded in the message

		Trained on malicious URL datasets from Kaggle, using the Decision Tree Machine Learning approach with more than 80% estimated accuracy. Following are the links to the dataset from Kaggle.

		1. https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset

2. Take a message from the user as **input**, and split it into
	
	* **Body** - i.e. text without links

		The body text will be passed through a Lexical analyzer and the Cyberus Risk Status for the body will be calculated quantitatively.

	* **URL** - i.e. links embedded inside the message

		The URL will be passed through URL analysis and the Cyberus Risk Status for the URL will be calculated quantitatively.

3. Based on Risk Status, Cyberus will take an average with some weight of each Status, and **outputs** Overall Cyberus Risk on the scale with a range from 0 to 100, as the illegitimacy of message, or Cyber Risk Status.

## Disclaimer

Cyberus is under development, the information may not be relevant w.r.t. the final product.
