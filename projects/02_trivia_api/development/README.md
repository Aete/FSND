# Full Stack API Final Project - Full Stack Trivia

## Introduction

### Motivation
<i>from [Udacity FSND repository](https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter)</i> <br>
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Prerequisites & Installation

### How to Install?
Download the repository or Clone this repository by running:
```bash
git clone https://github.com/Aete/FSND
```

#### Installing Dependencies: Frontend
Please install dependencies by naviging to the `/frontend` directory and running:
```bash
npm install
```
#### Installing Dependencies: Backend
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
createdb trivia
psql trivia < trivia.psql
```

## Run
To start the backend server, please navigate to the `/backend` directory and run:
```bash
export FLASK_APP=flaskr
flask run
```
To start the frontend page, please navigate to the `/frontend` directory and run:
```bash
npm start
```
Default address of the backend server is `http://localhost:5000` and the frontend page is `http://localhost:3000`.


## Test
You can test the backend part by running
```bash
python test_trivia.py
```
at the `/backend` directory

## API references
Please check the [backend](https://github.com/Aete/FSND/tree/master/projects/02_trivia_api/development/backend) part.

## Authors and Acknowledgements
A starter code of the repository is written by [Udacity FSND team](https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter). And Seunggyun Han developed this repository to complete.
