# microblog
 Flask Framework Training
from somewhere at chapter five?

# Installation
1) python -m venv venv (to create virtual env)
2) venv\Scripts\activate (for linux source venv/bin/activate)
3) pip install -r requirements.txt (to install dependencies)
4) set FLASK_APP=microblog.py (export FLASK_APP=microblog.py for linux)
5) flask db upgrade (to apply migrations to sqlite3)
7) flask shell (to run application in shell interactive mode)
8) u = User(username=1234) # create db object
9) db.session.add(u) # initiate transaction to save object to database
10) db.session.commit() # finish transcation/session of operating with database, your object is saved
