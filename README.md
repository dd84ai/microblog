# microblog
 Flask Framework Training
from somewhere at chapter five?

# Installation
1) python -m venv venv
2) venv\Scripts\activate (for linux source venv/bin/activate)
3) pip install -r requirements.txt
4) set FLASK_APP=microblog.py (export FLASK_APP=microblog.py for linux)
5) flask db upgrade (to apply migrations to sqlite3)
7) flask shell (to run application in shell interactive mode)
8) >>> u = User(username=1234)
9) >>> db.session.add(u)
10) >>> db.session.commit()