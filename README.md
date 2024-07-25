# grAnalysis
Final Degree Project of Computer Engineering Science degree titled "Web application for the study and analysis of customer comments in the hotel sector" at University of Cádiz - 2024
## Abstract
This project focuses on the development of a web platform in which users will be able to request and compare studies based on accommodation reviews registered in Booking. In this way, the user is granted access to relevant information about the reviews of these accommodations, as well as the results of a sentiment analysis of customer comments and different types of statistical studies.

All this will be carried out through a waterfall methodology through which a system will be formed that will consist of a backend server, composed of a REST API; a module that contemplates the collection, analysis and comparison of information; an SQL database, to store all the information captured and analyzed; and a web interface, through which users will access it.

This project's main objective is to automate the process of analyzing the information corresponding to the reviews of the requested accommodations. Thus making it easier for the platform user, through natural language processing, to draw significant conclusions about the opinion that customers have of the accommodations studied.

## Architecture Diagram

In the following figure, we can see the Architecture Diagram in which we appreciate the two main system roles: administrator and user. These two have access to the main content of the web app grAnalysis. The server will be able to handle all requests related to user tasks, such as requesting new analyses for new accommodations, visualizing an analysis, or comparing two existing analyses. Additionally, the administrator will be able to request maintenance and management tasks from the server, such as processing user requests, controlling user access to the platform, or updating the analysis of an accommodation. All the information required by the system will be stored in the MySQL database.

![Alt text](images/ArchitectureDiagram.png)

## Development

The main operation of the system can be divided into the following two modules:

* **Data collection module** → Using web scraping techniques such as HTTP programming or DOM parsing with BeautifulSoup and the requests library, the system automates the extraction of data related to reviews through the URL of a Booking accommodation. Once we have the requested data, it is normalized using regular expressions.  
 
* **Analysis module** → With all the information related to an accommodation, we apply the selected NLP model for classification, adapting the result to a polarity scale of 0.0 to 1.0, where 0 represents the most negative value and 1 represents the most positive. It is important to note that to increase the model's accuracy, each comment will be divided into sentences. The model will be applied to each sentence individually, evaluating each one separately. Using the NLTK library, the most relevant word from each sentence will be extracted and assigned a polarity relative to the sentence, taking into account its context.


## License
GNU General Public License v3.0 - Copyright (c) 2024 - Pablo Granados
