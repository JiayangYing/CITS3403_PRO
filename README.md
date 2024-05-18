# CITS3403 Project: Ecohub

## Description

EcoHUB is developed to provide a robust, user-friendly platform that aligns with sustainable development goals by promoting the reuse and recycling of products. It enables sellers to list their second-hand or recyclable products and manage their inventories efficiently. Buyers can browse, filter, and order products with ease. The platform supports essential functionalities like email verification, profile management, and comprehensive order handling, ensuring a secure and smooth transaction experience.

The backend is powered by Flask, ensuring efficient handling of user requests and interactions, while the frontend uses Bootstrap for a responsive and visually appealing design. Elasticsearch enhances the search capabilities, and thorough testing with unit and Selenium tests ensures system reliability.

## Purpose

EcoHUB's primary goal is to provide an easy-to-use platform for Australians to buy and sell second-hand and recyclable products. This initiative aims to support sustainable development by reducing waste, promoting recycling, and fostering economic opportunities in line with specific Sustainable Development Goals.

## Technologies

- **Frontend**: HTML, CSS, Bootstrap V5.3, Jinja2, jQuery, AJAX
- **Backend**: Flask, SQLite3, Elasticsearch (via Docker), email integration, JWT for token verification
- **Testing**: Unit tests, Selenium tests

## Group members

| UWA ID | Name          | GitHub Username |
|--------|---------------|-----------------|
| [23696808] | [wenbo li]        | [lwb611266]|
|[23192082] | [Juan Lakonawa]        | [sleepadept] |
| [23171563] | [Yiu Xuan Lok]        | [loklokyx] |
| [23792058] | [Jiayang Ying]        | [JiayangYing] |

## Installation

### Requirements
- pip3 install flask
- pip3 install flask-sqlalchemy
- pip3 install flask-wtf
- pip3 install flask-login (used for session)
- pip3 install flask-mail
If still having problem please install all dependency from requirment.txt
python3 flask run
## Initialization
To start the application, follow these steps:

1. Clone this repository to your local machine:
```bash
git clone https://github.com/your-repo-name.git


2. Navigate to the project directory:
```bash
   cd your-repo-name

3. Install the required dependencies:
   npm install

4. Start the application:
   npm start

The application should now be running at http://localhost:5000
## Run tests
To run tests for the application, follow these steps:

1. Ensure you are in the root directory of the project:
   cd your-repo-name

2. Run the test command:
   npm test

Test results will be displayed in the terminal window.

## Deliverables
The "deliverables" folder contains progress updates captured as short screen-capture videos (.mp4) or image files (.jpeg, .png). Each file corresponds to a specific milestone in the project.

### [Tag 1.0.0] - Initial Setup
## Description: 

This milestone marks the initial setup of the project, including creating the repository, setting up the development environment, and configuring basic project structure.
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
Includes configurations for user login,signup,profile,as well as product listing and order form.
## Database Schema: 
Display the database schema or model structure representing different entities in the application, such as users, products, orders, etc.
## Data Population: 
If applicable, demonstrate the use of the /populate feature to populate the database with dummy data, showing the creation of records in the database tables.
## Data Retrieval:
Optionally, showcase querying the database to retrieve and display data on relevant application pages, such as product listings or user profiles.


