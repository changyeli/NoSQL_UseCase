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
First, the [files](https://github.com/palooney/NoSQL_UseCase/blob/master/file_path.txt) that need to be processed are recorded [here](https://github.com/palooney/NoSQL_UseCase/blob/master/parser.py), which as discussed above, only files in *sent*, *sent_mails* and *sent_items* are considered as qualified. Also, we filter out those emails who did not have any receiver. For example, if ```TO:``` is empty, so we will skip this document and continue to parse next document.

[Data cleaning](https://github.com/palooney/NoSQL_UseCase/blob/master/cleanser.py) follows the rules discussed above, and parses all qualified files to extract the attributes mentioned above in to JSON. [edge.json](https://github.com/palooney/NoSQL_UseCase/blob/master/edge.json) contains all directed edges information, with *sender* and *receiver* dedicating the direction of edge.

Node information is inside of [email_unique.json](https://github.com/palooney/NoSQL_UseCase/blob/master/email_unique.json), which includes all unique email addresses found from qualified files.

### Data Loading
[driver.py](https://github.com/palooney/NoSQL_UseCase/blob/master/driver.py) is the driver we used to load data into ArangoDB. [edge.json](https://github.com/palooney/NoSQL_UseCase/blob/master/edge.json) is loaded as edge collection, *email* in ArangoDB, whereas  [email_unique.json](https://github.com/palooney/NoSQL_UseCase/blob/master/email_unique.json) is loaded as vertex collection, *people* in ArangoDB. Also, the graph object, *enron_group* is created based on *email* and *people*.

## Data Analysis
For the entire AQL queries, please check [AQL_Query.txt](https://github.com/palooney/NoSQL_UseCase/blob/master/AQL_Query.txt) for more details.
### Statistics Summary of the Data

- Total number of vertex: 12,938
- Total number of edge: 126, 484

### Easy Questions' Solution
#### Verify number of custodians and emails
Please refer the ```Statistics Summary of the Data``` section. Note that the null values are filtered out during data cleaning process.
#### Representing custodians as nodes and at least one existing email between custodians as edges
Please refer [1degree.json](https://github.com/palooney/NoSQL_UseCase/blob/master/1degree.json) file for detail. In this file we choose ```kay.mann@enron.com``` as our center node.

The AQL used for the result is listed below:

```
FOR v,e,p IN 1..1 OUTBOUND 'people/kay.mann@enron.com' 
GRAPH 'enron_graph'
RETURN  e
```

#### Which custodians have the minimum, maximum, and median in-degrees and out-degrees

The AQL used for this question is listed below:

```
FOR x IN email 
COLLECT people = x._to WITH COUNT INTO counter 
SORT counter DESC
RETURN {people: people, number: counter}

FOR x IN email 
COLLECT people = x._from WITH COUNT INTO counter 
SORT counter DESC
RETURN {people: people, number: counter}
```

- For received emails:
	- Email received from 315 identical email addresses
	- ```kay.mann@enron.com``` received the most emails, 8924 in total
	- 79 identical users receive only 1 email, which is the minimum
	- The mean of received emails is 402.133
	- The median of received emails is 73
- For sent emails:
	- Email sent by 1000 identical email addresses
	- ```vkaminski@aol.com``` sent the most emails, 2722 in total
	- 14 identical users sent 26 emails, which is the minimum
	- The mean of sent emails is 80.667
	- The median of sent emails is 51

### Medium Questions' Solution
#### What group was in communication with the CEO

The AQL used in this question is listed below:

```
/*Find emails that relative to a specific person*/
FOR x IN ANY 'people/kay.mann@enron.com' email
OPTIONS {bfs: true, uniqueVertices: 'global'} 
RETURN x._id
```

Please check [Appendix_A.json](https://github.com/palooney/NoSQL_UseCase/blob/master/Appendix_A.json) for query results.

#### Find two degree away from a specific person who wrote long email

We choose ```kay.mann@enron.com``` as our central node.

The AQL used for this question is listed below:

```
FOR v,e,p IN 1..2 OUTBOUND 'people/kay.mann@enron.com' 
GRAPH 'enron_graph'
FILTER e.body_len > 1000
RETURN v._key
```

Please check [2degree_long.json](https://github.com/palooney/NoSQL_UseCase/blob/master/2degree_long.json) for query results.

#### Shortest Path between Two Nodes
We choose ```kay.mann@enron.com``` and ```vince.kaminski@enron.com``` as our nodes.

The AQL used for this question is listed below:

```
FOR v, e IN OUTBOUND SHORTEST_PATH 
'people/kay.mann@enron.com' TO 'people/vince.kaminski@enron.com' 
email
RETURN [v._key, e._key]
```

The result of above AQL is: ```kay.mann@enron.com``` -> ```carol.clair@enron.com``` -> ```mark.haedicke@enron.com``` -> ```vince.kaminski@enron.com```

### Hard Questions' Solution
## Conclusion
### What we did
We did data identification, selection, cleaning and loading. We visualize data with ArangoDB built-in tool
### What we like
ArangoDB has its own visualization tool, which is very convenient for us to show the graph and present the demo.
### What we learned
We learned AQL, a SQL-like language to help us query based on graph. We also learned some new data cleaning technique, including regular expression.
### What's the Challenge
First, the data is super complex, such as typos, duplications, irregular employee names, missing receiver email addresses. Also, compared to SQL, AQL is somehow limited, which increases our difficulty to query. Moreover, it seems longest path traversal is not supported in ArangoDB, therefore we cannot answer some questions which we raised in Phase 1.
## Appendix
Please check our [github repo](https://github.com/palooney/NoSQL_UseCase) for more details.


