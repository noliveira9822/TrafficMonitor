# TrafficMonitor

**Starting the api.**

Change into <u>traffic_monitor</u> directory and follow theses steps:

----
- python3 manage.py makemigrations traffic_segment
- python3 manage.py migrate
- python3 manage.py runserver
----

If you need to feed the database with some values, **traffic_speed.csv** has several records already and you can use them.
In order to fill the database with these values, execute the **fill_db.py** script.

- python3 fill_db.py


#### Note:
**Requirements.txt** has all the dependencies needed for this project. Install them by running:

- pip install -r requirements.txt

