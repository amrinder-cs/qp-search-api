# Previous Question Paper Retriever

 This project is aimed at downloading previous year(s) question papers. I wanted to make it so it can be automatically updated each semester to have the question papers.


### The Source:
- Short URL: https://t.ly/PuJA
- [Original Drive URL](https://drive.google.com/drive/folders/11ywkOKyeixCPihsCzqZDyzy2msLXxx6w)
 This is (probably) maintained by the Examination branch. I got it from somewhere and they constantly upload old question papers aftear each semester.

### The Problem:

 It was tough to search for old question papers there, due to how hard it is to navigate google drive.

 You could not search question papers branch wise/semester wise. Only year wise.

### Initial solution:
 First i downloaded each question paper manually, but that took a lot of space (4 GB). It just wasn't the best solution, but it helped me search for question papers by paper id (i wrote a python script for it but i lost it somewhere)

### Final solution:
 Secondly, I got an idea to directly scrape the google drive using the google drive's API. So i pulled all the data, but that data was humungus (about 10k records) so i needed a database to store it. I could not hardcode it somewhere since that would be inefficient. So i used my favourite database (PostgreSQL) to store the file_name, download_link and folder_name(folder which it came from)

# Working of the project:
<details>
<summary>1. Setting up the database</summary>

 Docs pending
</details>

<details>
<summary>2. Setting up the Enviornment Variables</summary>
 
> Environment variables are dynamic settings external to the code, used to configure software behavior without altering the code itself. Long story short, you don't want to change your credentials in code every time, enviornment variables can be useful in that case.

- Check the .env.example
- copy paste it and rename it to .env
- Put your credentials in it.

> :warning: **WARNING:** Never push environment variables to a public repository. They are meant to be private.
</details>

<details>
<summary>3. Drive Scraping</summary>

 
> It scrapes the data from google drive, and stores it in a PostgreSQL database (hosted on my homeserver)

#### a) Getting the service account key
 A service account is a special kind of account typically used by an application or compute workload, such as a Compute Engine instance, rather than a person. A service account is identified by its email address, which is unique to the account.
[Read more here](https://cloud.google.com/iam/docs/service-account-overview).


This is how to do it step by step:

1. Go [Here](https://console.cloud.google.com/welcome?project=stone-chariot-245102) and make an account on google cloud.
1. Make a new project:![Making first project](https://i.imgur.com/m7D0KvJ.png)
1. go to APIs and Services on https://console.cloud.google.com/ ![API and Services](https://i.imgur.com/YUy62Et.png)
1. Go to Enable APIs and Services: ![Enable API and Services](https://i.imgur.com/BKyUSII.png)
1. Search and Enable google drive API.
1. Create credentials for that api. You make a service account to use google drive API.
1. rename the API key to `service_account_key.json` and save it in same folder as the `drive_scraper.py` script.

#### b) Run the script.
1. You need to make a virtual enviornment for python. Read online what it does. You make it using the following command on windows CMD terminal:
`python -m venv venv`
Search how to do it for your operating system online.
1. Activate the virtual enviornment. For windows: type `venv\scripts\activate` in your terminal  
1. Run the script using python drive_scraper.py
1. At the end it should store the list of files, download links, folder name in the database.
</details>

<details>
<summary>4. Subject scraping</summary>
Till now we got:

- File Name (usually subject code)
- Download link.

> Now it's not user friendly to go to your syllabus, search for subject code, put that subject code to search for question paper.

> To make it better, we will need Subject Code, Semester, Branch etc. Luckily for us, we got https://academics.gndec.ac.in/datesheet as a really good source for getting all that data. This is what i mean:
![Datesheet](https://i.imgur.com/JNKyl7E.png)

> Now we could just copy paste that data into excel directly, but that would be too hard for a lot of branches. Why do manual labor? that's what we are engineers for, to reduce manual labor where it's not necessary.

This is my approach to getting that data:

1. First inspect how the request goes to https://academics.gndec.ac.in/ in the browser console. this is how you do it: ![Request for datesheet](https://i.imgur.com/d5z5ZBH.gif)
1. Now we need to get that "value" field which is being sent as a request. I found that it was in the dropdown menu of Program. Here: ![Subject Values](https://i.imgur.com/zyXkWAp.png)
1. Gotta do the same process now, but programatically. So i used python to do so (see scrape_subjects.py) 
1. Extracted all the \<table elements from the response and used beautifulsoup and pandas to convert it into .csv format, and saved it.
1. Merged all those CSVs into one, and imported them into the database after some processing on CSV files, using this command: 
```sql
COPY paper_ids(branch_id, semester, subject_name, subject_code, paper_id, m_code, scheme) 
FROM '/path/to/your/csv/file.csv' 
WITH (FORMAT csv, HEADER true);
```
</details>

<details>
<summary>5. The API</summary>

 > Now users can't just access database directly, we need API for sending the data to the user's browser. Well server.js explains how the API works. There's more info on it in api.md
</details>

<details>
<summary>6. The Frontend</summary>

> Now the hard part is done. API is complete and database is setup. All what needs to be done is the frontend for the project. May it be someone else, not me who appends to this file.
</details>
