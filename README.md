# CITS3403 Project: Ecohub

## Description

EcoHUB is developed to provide a robust, user-friendly platform that aligns with sustainable development goals by promoting the reuse and recycling of products. It enables sellers to list their second-hand or recyclable products and manage their inventories efficiently. Buyers can browse, filter, and order products with ease. The platform supports essential functionalities like email verification, profile management, and comprehensive order handling, ensuring a secure and smooth transaction experience.
## Purpose
EcoHUB's primary goal is to provide an easy-to-use platform for Australians to buy and sell second-hand and recyclable products. This initiative aims to support sustainable development by reducing waste, promoting recycling, and fostering economic opportunities in line with specific Sustainable Development Goals.
## Feature
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
## Group members
| UWA ID | Name | GitHub Username |
|:--------:|:------------:|:-----------:|
| 23696808 | Wenbo Li     | lwb611266   |
| 23192082 | Juan Lakonawa| sleepadept  |
| 23171563 | Yiu Xuan Lok | loklokyx    |
| 23792058 | Jiayang Ying | JiayangYing |

## Installation

#### Setting Up the Project
Follow these steps to clone the repository, set up a virtual environment, and install dependencies:

**1. Clone the Repository**

- First, clone the repository to your local machine:
```sh
git clone https://github.com/JiayangYing/CITS3403_PRO.git
cd <repository_directory>
```

**2. Set Up a Virtual Environment**

We recommend using venv to create a virtual environment. Detailed instructions can be found in the official [Python documentation](https://docs.python.org/3/library/venv.html).

**Create the Virtual Environment**

In the root directory of the cloned repository, execute the following command:
```sh
python3 -m venv venv
```
This command creates a virtual environment named venv.

**Activate the Virtual Environment**

Activate the virtual environment using the command specific to your operating system:

- **For Linux and macOS:**
```sh
source venv/bin/activate
```

- **For Linux and macOS:**
```sh
.\venv\Scripts\activate
```
You'll know the virtual environment is active when `(venv)` appears at the beginning of your command line prompt.

**3. Install Dependencies**

With the virtual environment activated, install the required dependencies:
``` sh
pip install flask
pip install flask-sqlalchemy
pip install flask-wtf
pip install flask-login
pip install flask-mail
```
If still having problem please install all dependency from requirment.txt
```sh
pip install -r requirements.txt
```

**4. Configure Environment Variables**

Create a `.env` file in the root directory of your project to configure environment variables. The `.env` file should contain key-value pairs for your environment-specific settings.
Here’s an example of what the `.env` file might look like:
``` sh
ELASTICSEARCH_URL = http://localhost:9200
MAIL_SERVER = smtp.googlemail.com
MAIL_PORT = 587
MAIL_USE_TLS = 1
MAIL_EMAIL = <your_email>
MAIL_USERNAME = <your_username>
MAIL_PASSWORD = <email_password>
```
You should now have a fully set up development environment with all dependencies installed.

## Troubleshooting

If you encounter issues with `app.db` such as database schema or you need to reset it, the following commands might be useful:
```sh
flask db downgrade base
flask db upgrade
```

## Initialisation

To start the application, run following command:
```sh
python3 flask run
```
The application should now be running at http://localhost:5000

## Run tests

To run tests for the application, follow these steps to run tests using `selenium` and `unittest`.

**1. Selenium Testing**

**Install Selenium**

Make sure you have Selenium installed:
```sh
   pip install selenium
```

**Running Selenium Tests**

**Run Selenium Tests in PowerShell:**

Open PowerShell and use the following command to run your Selenium tests:
```sh
   python3 -m unittest tests/selenium.py
```
This will open the Chrome browser and perform the actions defined in the `selenium.py`

**2. Unittest**

**Install Unittest**

`unittest` is a built-in Python module used for writing and running tests. It is included with Python, but if for some reason it is not installed, you can install it via pip:
```sh
   pip install unittest
```

**Running Unittest**

**Run Unittests in `WSL`/`venv`:**

Open `WSL` and activate your virtual environment, then use the following command to run your unittests:
```sh
   python3 -m unittest tests/unit.py
```
Test results will be displayed in the terminal window.

## Deliverables
The "deliverables" folder contains progress updates organised by specific topics, such as Product Implementation and SignUp Page Workflow. Each topic includes videos and images that showcase progress and provide prototypes related to that topic. This structured approach makes it easy to locate and review the relevant videos and prototypes for each aspect of the project.
