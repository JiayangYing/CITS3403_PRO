# CITS3403 Project: Ecohub
 
# EcoHUB

EcoHUB is a platform dedicated to connecting sellers and buyers within Australia, focusing on Sustainable Development Goals (SDG-17) and incorporating SDG-8, SDG-10, SDG-12, and SDG-13. EcoHUB enables the sale and purchase of second-hand or recyclable products, fostering a community-driven marketplace that promotes sustainability and economic inclusiveness.

## Description

EcoHUB is developed to provide a robust, user-friendly platform that aligns with sustainable development goals by promoting the reuse and recycling of products. It enables sellers to list their second-hand or recyclable products and manage their inventories efficiently. Buyers can browse, filter, and order products with ease. The platform supports essential functionalities like email verification, profile management, and comprehensive order handling, ensuring a secure and smooth transaction experience.

The backend is powered by Flask, ensuring efficient handling of user requests and interactions, while the frontend uses Bootstrap for a responsive and visually appealing design. Elasticsearch enhances the search capabilities, and thorough testing with unit and Selenium tests ensures system reliability.

## Purpose

EcoHUB's primary goal is to provide an easy-to-use platform for Australians to buy and sell second-hand and recyclable products. This initiative aims to support sustainable development by reducing waste, promoting recycling, and fostering economic opportunities in line with specific Sustainable Development Goals.
## Group members

| UWA ID | Name          | GitHub Username |
|--------|---------------|-----------------|
| [23696808] | [wenbo li]        | [lwb611266]|
|[23192082] | [Juan Lakonawa]        | [sleepadept] |
| [23171563] | [Yiu Xuan Lok]        | [loklokyx] |
| [23792058] | [Jiayang Ying]        | [JiayangYing] |

## Features

### User Features
- **Signup/Login**: Users can sign up as either sellers or buyers. Sellers must provide a shop name.
- **Email Verification**: Upon successful registration, users receive an email verification link with a 3-day expiry. Users can resend the verification email from their profile page.
- **Profile Management**: Users can edit their profile details, change their password, and deactivate their account.

### Seller Features
- **Product Management**: Sellers can add and edit products. Instead of deleting, products can be marked as inactive.
- **Image Upload**: Product images can be uploaded in jpg, jpeg, or png formats, with content verification.
- **Order Management**: Sellers can approve or reject orders from buyers and cannot order their own products.

### Buyer Features
- **Order Products**: Buyers can order active products and cancel orders from their order listing page.
- **Explore Products**: Buyers can explore product categories with filtering options for categories, conditions, and price ranges.
- **Product Details**: Detailed product pages with a contact seller option and auto-filled order details.

### General Features
- **Product Categories**: Clothing & Accessories, Home & Garden, Electronics, Books & Media, Sport & Leisure, and Others.
- **Responsive Design**: Filtering panel transforms to dropdowns on smaller screens; products can be viewed in grid or list format.
- **Elastic Search**: Integrated search functionality using Elasticsearch within a Docker container.
- **Dark/Light Theme**: Users can switch between dark and light themes for better user experience.

## Technologies

- **Frontend**: HTML, CSS, Bootstrap V5.3, Jinja2, jQuery, AJAX
- **Backend**: Flask, SQLite3, Elasticsearch (via Docker), email integration, JWT for token verification
- **Testing**: Unit tests, Selenium tests

## Installation
To run EcoHub locally, follow these steps:

## Before anything make sure python and pip are installed in your system/wsl
Clone the repo and set up your preferred virtual environment. We have used venv. Refer to https://docs.python.org/3/library/venv.html for detailed instructions. The easiest way is to locate the clone repo in your terminal/wsl, and in the main directory execute: python3 -m venv venv
This will create the target directory for your virtual env. Next you need to activate it. This is done via:
**source venv/bin/activate**
You'll know it is active when (venv) appears on the command line before your username.
Inside your virtual env all dependancies need to be installed, to do this run:
pip install -r requirements.txt
## To run tests use:
**pytest**

The following tests are included:
All routes defined in routes.py are checked for status 200
User account creation and login
User applying for a job, poster receiving application
Jobs being returned from search
User profile page displaying relevant data
Multiple db queries
## To launch app use:
 **flask run**
 
The application has been built to automatically create a db for you and perform all migrations in the background before the app launch
Once the flask development server is running follow the link provided
Initially the db will be empty. In order to simulate user interactions the /populate page has been created. This will allow you to populate the db with dummy data. To use this feature, add /populate  to the end of your development server ip. Then Follow the prompts displayed on the webpage to create dummy data. This might include options to specify the amount or type of data to generate.
Once the database is populated, you can interact with the application using the provided features such as login, signup, buying and selling, ordering, and product listing，explore the different functionalities and simulate user interactions as needed.
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


