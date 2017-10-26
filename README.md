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

- Type: sender or receiver, which can be distinguished based on ```To: ...``` and ```From:...```
- Message ID: uniquely defined in the dataset
- Subject: email subject
- Employee: the employee folder where the email is found
- Date: message sent/received date
- Body length: the total content length of email

### Data Cleaning
[Data cleaning]() is 

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


