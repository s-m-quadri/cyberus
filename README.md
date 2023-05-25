![Intro](https://github.com/s-m-quadri/cyberus/assets/88645248/e0067c1d-4f90-4cbd-ac93-1065c900cf1c)

<br/>

# Cyberus - measuring risk

Cyberus is a tool that checks the generic and sentimental legitimacy of a message and provides an approximate idea of the risk based on the dataset on which it has been trained, along with machine learning models for quantitatively predicting the risk.

## Important Links
1. [Official GitHub Repository](https://github.com/s-m-quadri/cyberus)
2. [Live Demo on Google Colab](https://colab.research.google.com/drive/1J_3JlpL9DHryn6nlHMCr4JqvgNGI21-n?usp=share_link)
3. [Presentation, poster and even more...](https://drive.google.com/drive/folders/1CEb8xgVjot8ixARXqxRpRWmdF381Sxgp?usp=share_link) 

## Project Details

`Category:` Safety in e-commerce

`Team Members`
1. Shreyash Ravindra Kendre
2. Shaikh Abu Hayyan Muneeb
3. Syed Minnatullah Quadri

`Class:` TY-CSE-B (B1 Batch)

`Course:` Machine Learning

`Date:` May 2023

`Guided by:` Dr. Smita S. Ponde

<br/>

## Project Description

### 1. Background

Consider a **scenario** where a person receives an SMS regarding a special offer, an email for the enrollment procedure, and a notification regarding pending payments. At first glance, all of these messages appear to be legitimate. However, due to the proximity of the deadline and the individual's limited time, they may be influenced by their environment and the situation, making it difficult to thoroughly analyze the messages.

### 2. Problem

The person is uncertain about the legitimacy of the message and unsure whether to proceed or not. They want to quickly determine the legitimacy of the message and seek a risk status to make an informed decision. Our aim is to assist the person by providing a risk assessment that allows them to feel comfortable without the need for manual analysis of lengthy text passages.

### 3. Understanding

One of the authentic and genuine methods for decision-making is to analyze statistics, as it helps us make more objective decisions. Therefore, before attempting to solve the problem at hand, we will first examine relevant statistics. Here are some notable statistics to consider: 

- Email spam costs businesses $20.5 billion every year.
- Approximately 85% of all emails are classified as spam.
- Around one-third of all data breaches in 2018 were a result of phishing attacks.
- A new phishing site is created on the internet every 20 seconds.
- More than 70% of phishing emails are opened by their targets.
- Approximately 90% of security breaches in companies occur due to phishing attacks.

It is important to note that phishing attacks involve innocent-looking emails, pop-ups, ads, and company communications that lure users into clicking on them, leading to the installation of spyware, viruses, and other malicious software on their devices.

Sources:

1. [Spam Statistics](https://dataprot.net/statistics/spam-statistics/)
2. [Phishing Statistics](https://dataprot.net/statistics/phishing-statistics/)

### 4. Solution

We need to accurately recognize the lexical structure of the message, analyze any embedded links, and determine the legitimacy of the message. Introducing **Cyberus**, a tool designed to assess the generic and sentimental legitimacy of messages and provide an approximate risk assessment. Cyberus utilizes a dataset on which it has been trained, along with machine learning models, to analyze messages and determine their level of risk.

### 5. Working

There are 3-step involved in knowing the working of Cyberus.

1. First, we will **build** two machine learning models:

   - The **Lexical analysis** model focuses on the body of the message. It will be trained on spam mail and SMS datasets from Kaggle using the Support Vector Machine (SVM) machine learning model approach. The estimated accuracy of this model is more than 75%. Here are the links to the datasets from Kaggle:

     1. [SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)
     2. [Spam Mails Dataset](https://www.kaggle.com/datasets/venky73/spam-mails-dataset)

   - The **URL analysis** model is responsible for analyzing links embedded in the message. It will be trained on malicious URL datasets from Kaggle, utilizing the Decision Tree machine learning approach. The estimated accuracy of this model is more than 80%. Here is the link to the dataset from Kaggle:

     1. [Malicious URLs Dataset](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset)

Please note that the provided links lead to the respective datasets on Kaggle.

2. The system will take a message from the user as **input** and split it into two components:

   - **Body**: This refers to the text without any embedded links. The body text will undergo lexical analysis using the Lexical analyzer. The Cyberus Risk Status for the body will be calculated quantitatively.

   - **URL**: This refers to the links embedded within the message. The URL will be subjected to URL analysis. The Cyberus Risk Status for the URL will be calculated quantitatively.

3. Based on the Risk Status obtained from the body and URL analyses, Cyberus will calculate an overall Cyberus Risk. This will involve taking an average of each Risk Status, with some weights assigned to each component. The resulting Overall Cyberus Risk will be provided as an output, ranging from 0 to 100, indicating the level of message illegitimacy or Cyber Risk Status.

## Contribution

We welcome contributions to the development of Cyberus. If you would like to contribute to the project, please follow the guidelines outlined in the official documentation or reach out to the development team for more information. Contributions can include but are not limited to bug fixes, feature enhancements, documentation improvements, and feedback on the existing functionalities. By contributing to Cyberus, you can help improve the tool's effectiveness and make a positive impact on its overall development. Together, we can create a robust and reliable tool for checking the legitimacy and risk assessment of messages.
