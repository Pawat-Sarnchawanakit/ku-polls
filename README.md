## KU Polls: A Django-based web application for creating and participating in polls.
[![tests](https://github.com/Pawat-Sarnchawanakit/ku-polls/actions/workflows/tests.yml/badge.svg)](https://github.com/Pawat-Sarnchawanakit/ku-polls/actions/workflows/tests.yml)  
Based on the [Django Tutorial project](https://docs.djangoproject.com/en/5.1/intro/tutorial01/), with additional features.  
This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).
### Key Features
- Poll creation with YAML preview
- Authenticated poll viewing and voting
- Poll results display
- Polls publication and end dates
- User authentication and authorization
- Event logging
- User-friendly interface
### Appearance
![UI Preview](./images/UI.png)  
### Installation
For installation instructions, please refer to the [Installation Guide](./Installation.md) located in this repository.

### Running the Application
**After following the installation instructions above**,
to run the KU Polls app, follow these steps:

1. Activate the virtual environment:
   - `$ source ./.venv/bin/activate` (Linux/Mac) or `.\venv\Scripts\activate` (Windows)
2. Install the required packages:
   - `$ pip install -r requirements.txt`
3. Run database migrations:
   - `$ python manage.py migrate`
4. Set environment (Optional):
   - `$ cat sample.env > .env` (Linux/Mac) or `type sample.env > .env` (Windows)
   - Edit the `.env` file with the editor of your choice.  
   `$ nvim .env`
5. Load initial data (Optional):
   - `$ python manage.py loaddata data/users.json`
   - `$ python manage.py loaddata data/polls-v4.json`
   - `$ python manage.py loaddata data/votes-v4.json`
6. Start the development server:
   - `$ python manage.py runserver`

Access the application at <http://127.0.0.1:8000/>.

### Demo Users
The following demo users are available for testing the app:

| Username | Password  |
|----------|-----------|
| demo1    | hackme11   |
| demo2    | hackme22   |
| demo3    | hackme33   |

### Project Documents
The project documents below are all available in the [Wiki](../../wiki/Home).
- [Vision Statement](../../wiki/Vision)  
- [Requirements](../../wiki/Requirements)  
- [Project Plan](../../wiki/KU-Polls-Project-Plan)  
- [Iteration 1 Plan](../../wiki/Iteration-1-Plan)  
- [Iteration 2 Plan](../../wiki/Iteration-2-Plan)  
- [Iteration 3 Plan](../../wiki/Iteration-3-Plan)  
- [Iteration 4 Plan](../../wiki/Iteration-4-Plan)  