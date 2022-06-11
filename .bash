python -m pip install -r requirements.txt
flask db init 
flask db migrate
flask db upgrade
python app.py




# python -m venv venv

# if [ -f venv/Scripts ]; then
#     . venv/Scripts/activate
#     venv/Scripts/python.exe -m pip install -r requirements.txt
# elif [ -f venv/bin ]; then
#     . venv/bin/activate
#     venv/bin/python -m pip install -r requirements.txt
# fi

# flask db init 
# flask db migrate
# flask db upgrade
# python app.py