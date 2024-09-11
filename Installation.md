## Installation Guide

### Prerequisites
Before installing the KU Polls app, make sure you have the following software installed on your system:

- Python 3.11+
- Git
- pip (Python package installer)

### Installation Steps

1. Clone the repository:
   - `$ git clone https://github.com/Pawat-Sarnchawanakit/ku-polls.git`

2. Navigate to the project directory:
   - `$ cd ku-polls`

3. Create and activate a virtual environment:
   - `$ python -m venv .venv`
   - `$ source ./.venv/bin/activate` (Linux/Mac) or `.\venv\Scripts\activate` (Windows)

4. Install the required packages:
   - `$ pip install -r requirements.txt`

5. Run database migrations:
   - `$ python manage.py migrate`
6. Set environment (Optional):
   - `$ cat sample.env > .env` (Linux/Mac) or `type sample.env > .env` (Windows)
   - Edit the `.env` file with the editor of your choice.  
   The details of how to set each variable is in the .env file.  
   `$ nvim .env`
7. Run tests (Optional):
   - `$ python manage.py test`
8. Load initial data (Optional):
   - `$ python manage.py loaddata data/users.json`
   - `$ python manage.py loaddata data/polls-v4.json`
   - `$ python manage.py loaddata data/votes-v4.json`

### Starting the Development Server
To start the development server, run the following command:

- `$ python manage.py runserver`

Access the application at <http://127.0.0.1:8000/>.

Now the KU Polls app is installed and ready to use.