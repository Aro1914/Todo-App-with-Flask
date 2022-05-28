python -m venv venv
source venv/Scripts/activate
venv/Scripts/python.exe -m pip install -r requirements.txt
flask db init 
flask db migrate
flask db upgrade
python app.py