# Phase 2 Report

## Review of Business Questions
## Data Processing
The original dataset mentioned in Phase 1 turned out to be too big to run on the local machine. Also, we failed to find a low-cost way to translate ```.pst``` to common files. Therefore, we chose the alternative [Enron dataset](http://www.cs.cmu.edu/~enron/), which contains plain text of translated ```.pst``` data, to continue our analysis.

In this dataset, each employee has a folder for himself/herself. Each folder contains several sub-folders, including ```all_documents```, ```contacts```, ```deleted_items```, ```sent```, ```inbox```, etc. We only extract data in ```sent_mail```, ```sent```, ```sent_items```. The reasons of selecting these three folders are listed below:

- We try to minimize redundant data and maximize the range of useful data
	- In this project, we only care about emails sent and received from Enron employees, and we do not care about data like TODO list, calendar updates, the project files. Therefore those three folders provide the most wanted data.
	- Also, tracking only *sent* emails can help us to reduce unnecessary data storage. It will significant reduce the data size that we need to reduce.

### Attribute Selection
As discussed above, we only care about the email sent and received by Enron employees, therefore we need to extract several attributes as listed below:

- Type: *sender* or *receiver*, which can be distinguished based on ```To: ...``` and ```From:...```
- Email: the email address of *sender* or *receiver*
- Message ID: uniquely defined in the dataset
- Subject: email subject
- Employee: the employee folder where the email is found
- Date: message sent/received date
- Body length: the total content length of email

Note that we did not extract employee's name as one of the attributes. During the data cleaning process, we found that there are too many variant version of names, for example, Philip Allen and P. A or P. Allen. Given the number of Enron employees, we don't have a valid method to classify names correctly. For example, P. A could be Philip Allen, or Paul Allison. Therefore, we do not keep names as one of the attributes.

Also, since the dataset is in plain text form, we cannot track attachment data either.

### Data Cleaning
First, the [files](https://github.com/palooney/NoSQL_UseCase/blob/master/file_path.txt) that need to be processed are recorded [here](https://github.com/palooney/NoSQL_UseCase/blob/master/parser.py), which as discussed above, only files in *sent*, *sent_mails* and *sent_items* are considered as qualified.

[Data cleaning](https://github.com/palooney/NoSQL_UseCase/blob/master/cleanser.py) follows the rules discussed above, and parses all qualified files to extract the attributes mentioned above in to JSON. [edge.json](https://github.com/palooney/NoSQL_UseCase/blob/master/edge.json) contains all directed edges information, with *sender* and *receiver* dedicating the direction of edge.

Node information is inside of [email_unique.json](https://github.com/palooney/NoSQL_UseCase/blob/master/email_unique.json), which includes all unique email addresses found from qualified files.

### Data Loading
[driver.py](https://github.com/palooney/NoSQL_UseCase/blob/master/driver.py) is the driver we used to load data into ArangoDB. [edge.json](https://github.com/palooney/NoSQL_UseCase/blob/master/edge.json) is loaded as edge collection, *email* in ArangoDB, whereas  [email_unique.json](https://github.com/palooney/NoSQL_UseCase/blob/master/email_unique.json) is loaded as vertex collection, *people* in ArangoDB. Also, the graph object, *enron_group* is created based on *email* and *people*.

## Data Analysis
### Statistics Summary of the data
### Easy Questions' Solution
### Medium Questions' Solution
### Hard Questions' Solution
## Conclusion
### What we did
### What we like
### What we learned
### What's the Challenge
## Appendix


