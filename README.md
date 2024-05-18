# CITS3403 Project: Ecohub

## Description

EcoHUB is developed to provide a robust, user-friendly platform that aligns with sustainable development goals by promoting the reuse and recycling of products. It enables sellers to list their second-hand or recyclable products and manage their inventories efficiently. Buyers can browse, filter, and order products with ease. The platform supports essential functionalities like email verification, profile management, and comprehensive order handling, ensuring a secure and smooth transaction experience.
## Purpose
EcoHUB's primary goal is to provide an easy-to-use platform for Australians to buy and sell second-hand and recyclable products. This initiative aims to support sustainable development by reducing waste, promoting recycling, and fostering economic opportunities in line with specific Sustainable Development Goals.
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

To run tests for the application, follow these steps:

1. Ensure you are in the root directory of the project:
```sh
   cd your-repo-name
```
2. Run the test command:
```sh
   python -m unittest discover tests
```
Test results will be displayed in the terminal window.

## Deliverables
The "deliverables" folder contains progress updates captured as short screen-capture videos (.mp4) or image files (.jpeg, .png). Each file corresponds to a specific milestone in the project.
