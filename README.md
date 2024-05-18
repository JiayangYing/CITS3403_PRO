# CITS3403 Project:Ecohub

## Purpose
EcoHub is a project aimed at creating a platform that fosters environmental awareness, education, and action. Our goal is to provide a centralized hub where users can access resources, connect with like-minded individuals, and contribute to environmental initiatives,through trading of recylable products.
## Group Members:
| UWA ID | Name          | GitHub Username |
|--------|---------------|-----------------|
| [23696808] | [wenbo li]        | [lwb611266]|
|[23192082] | [Juan Lakonawa]        | [sleepadept] |
| [23171563] | [Yiu Xuan Lok]        | [loklokyx] |
| [23792058] | [Jiayang Ying]        | [JiayangYing] |
## Features
- **Selling of Recyclable Products:** Users can list their recyclable products for sale on the platform, promoting recycling and reducing waste.
- **Buying:** Browse through listings of recyclable products to purchase and contribute to environmental sustainability.
- **User Registration:** Register as a seller or buyer by creating an account on the platform, enabling access to selling and buying functionalities.
- **Product Listings:** Sellers can create listings for their recyclable products, including descriptions, prices, and other relevant details, allowing buyers to find and purchase items easily.
- **Order Form:** Facilitates transactions by providing an order form where buyers can specify quantities, delivery details, and other preferences, streamlining the buying process.
- **Communication:** Enables communication between users, sellers, and buyers through a messaging system, fostering collaboration, addressing inquiries, and facilitating negotiation.


## Technologies Used
- **Frontend:** HTML,CSS,Bootstrap,JQuery,AJAX
- **Backend:** Flask,Websockets,SQLite
- **Authentication:** JSON Web Tokens (JWT)
- **UI Framework:** Bootstrap
- **Version Control:** Git, GitHub
- **Deployment:** Heroku

## Installation
To run EcoHub locally, follow these steps:

## 1.Before anything make sure python and pip are installed in your system/wsl
Clone the repo and set up your preferred virtual environment. We have used venv. Refer to https://docs.python.org/3/library/venv.html for detailed instructions. The easiest way is to locate the clone repo in your terminal/wsl, and in the main directory execute: python3 -m venv venv
This will create the target directory for your virtual env. Next you need to activate it. This is done via:
source venv/bin/activate
You'll know it is active when (venv) appears on the command line before your username.
Inside your virtual env all dependancies need to be installed, to do this run:
pip install -r requirements.txt
To run tests use:
pytest
The following tests are included:
All routes defined in routes.py are checked for status 200
User account creation and login
User applying for a job, poster receiving application
Jobs being returned from search
User profile page displaying relevant data
Multiple db queries
To launch app use:
flask run
The application has been built to automatically create a db for you and perform all migrations in the background before the app launch
Once the flask development server is running follow the link provided
Initially the db will be empty. In order to simulate user interactions the /populate page has been created. This will allow you to populate the db with dummy data. To use this feature, add /populate  to the end of your development server ip. Then Follow the prompts displayed on the webpage to create dummy data. This might include options to specify the amount or type of data to generate.
Once the database is populated, you can interact with the application using the provided features such as login, signup, buying and selling, ordering, and product listing.
Explore the different functionalities and simulate user interactions as needed.
## Deliverables
The "deliverables" folder contains progress updates captured as short screen-capture videos (.mp4) or image files (.jpeg, .png). Each file corresponds to a specific milestone in the project.

### [Tag 1.0.0] - Initial Setup
## Description: 
This milestone marks the initial setup of the project, including creating the repository, setting up the development environment, and configuring basic project structure.

## Deliverable: 
A screenshot or short video showcasing:

## Repository Creation: 
Show the creation of the private GitHub repository with the initial README file.
## Environment Setup:
Demonstrate the installation of necessary dependencies and tools required to run the application.
Basic Project Structure: Display the project directory structure, including any configuration files, folders for source code, and tests.

### [Tag 1.1.0] - User Authentication Implemented
## Description: 
This milestone signifies the completion of implementing user authentication features, allowing users to sign up, log in, and manage their accounts.

Signup Page: 
Show the signup page where users can create new accounts by providing their email and password.
Login Page: 
Demonstrate the login page where registered users can enter their credentials to access their accounts.
Authentication Flow: 
Showcase the flow of user authentication, including error handling for invalid credentials or registration attempts.
Account Management: 
If applicable, display the user profile page where users can update their information or change their passwords.

### [Tag 1.2.0] - Database Integration Complete
## Description: 
This milestone indicates the successful integration of the database with the application, allowing data storage and retrieval.

## Database Configuration: 
Show the database configuration settings, including the type of database used (e.g., SQLite, PostgreSQL) and connection details.
## Database Schema: 
Display the database schema or model structure representing different entities in the application, such as users, products, orders, etc.
## Data Population: 
If applicable, demonstrate the use of the /populate feature to populate the database with dummy data, showing the creation of records in the database tables.
## Data Retrieval:
Optionally, showcase querying the database to retrieve and display data on relevant application pages, such as product listings or user profiles.


