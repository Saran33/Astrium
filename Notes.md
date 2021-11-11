#### Get full list of all tickers:

1. Create venv:
`pip install virtualenv`
`virtualenv astenv`
Move contents to parent folder.
2. Launch venv:
windows:
`./astenv/scripts/activate`
unix:
`source astenv/bin/activate`

3. install dependencies:
`pip install django`
`pip install git+git://github.com/Saran33/pwe_analysis.git`

4. Create project:
`django-admin startproject astrium`
`cd astrium`
`django-admin startapp main_app`
Install Djano for VS code extension.
Add this to VS Code settings.JSON:
`"emmet.includeLanguages": {"django-html": "html"}`

5. interpreter path (VS Code):
Choose path > browse > ./astenv/bin/python

# Initial Front-End Dev
1. urls.py:
2. settings.py > add app
3. In main_app, create: urls.py, views.py
Copy content from outer urls.py to main_app urls.py, and remove unecessary code.
4. Create templates folder in main_app dir. Create mainapp folder in templates.
5. Create basic.html in templates/mainapp dir.
6. In views.py, define a view.
7. Create securityselector.html in templates/mainapp dir.
8. Add it to main_app/urls.py
9. Create basic.html file with [Bootstrap](https://getbootstrap.com/docs/5.1/getting-started/introduction/)
- Components > Starter template > copy the code to basic.html, delete title tags and hello world text from h1 tags.
- Add a nav bar: Navbar > copy the first snippet to basic.html (replace h1 tags)
- Change NAV to dark mode, add django tags.
10. Extend template in the securityselector.html file.
11. Create static folder in main_app dir. Create main_app folder in static dir.
12. In main_app create folders: css, js, and images.
13. In css create basic.css, securitytracker.css
14. Link basic.css to basic.html
15. Link some stuff, add some stuff etc...
15. Test it:
`python manage.py runserver`
16. In Bootstrap docs, Forms > Select > Multipleselect, copy it to securitselector.html block body (wrap it in a div. 
```html<div class="container">
<h1>Security Analysis</h1><p>Select securities</p><form action=""><select class="form-select form-select-lg mb-3" multiple aria-label="multiple select example">
```

17. Make securiytracker template.
- Bootstrap Conent > tables > table > copy it to tracker. Wrap in:
18. Add securiytracker to views.
19. Add it to urls.py
20. Go to: http://127.0.0.1:8000/securitytracker
21. Change Navbar title in basic.html

# Initial Back End Dev
1. Use Yahoo Finance and Alpha Vantage initially for testing. 
http://theautomatic.net/yahoo_fin-documentation/
https://github.com/atreadw1492/yahoo_fin
https://www.alphavantage.co/premium/
https://iexcloud.io/pricing/
`pip install yahoo-fin`
2. Import data source into views.py
3. Add the tickers into the securityselector.py file with a fot loop to display in table.
4. From Bootstrap > Components > Buttons > Block Buttons , paste it into form on securityselector
5. Get live data
- In views.py add details to SecurityTracker.
6. Add it to the securityselector.html form action.
7. Pass data to the front end, using a loop in the securityselector.html template
8. In main_app dir, create a templatetags folder with `__init__.py` and a a `myfilters.py` for passing the dict values.
9. In `myfilters.py`, create a custom filter.
10. Load the the template into securityselector.html
11. Add JS to calculate change from previous close.
12. CSS for green and red price changes.

# Automatic Updating
Use [celery](https://github.com/celery/celery) to call API at intervals, create web socket connection between user and server.
1. `pip install celery`
Create requirements.txt:
`pip freeze > requirements.txt`
2. Add celery settings to settings.py
3. Use [redis](https://github.com/redis/redis) as the broker for the queue. Django will send redis tasks to manage in a FIFO order. Redis will pass tasks to the celery worker.
- Install redis:
#### OSX:
```zzh
mkdir redis && cd redis
curl -O http://download.redis.io/redis-stable.tar.gz
tar xzvf redis-stable.tar.gz
cd redis-stable
make
make test
sudo make install
```
#### Windows:
https://github.com/tporadowski/redis/releases

- test redis works by running:
#### OSX:
```zzh
redis-server
```
In a new shell:
```zzh
redis-cli ping
```
(should return PONG)
#### Windows:
Navigate to the redis directory and launch the client.exe and in the newly opened CLI, run: `PING` command (should return PONG).

4. Install [django-celery-results](https://github.com/celery/django-celery-results) to monitor the status of tasks allocated to celery:
`pip install -U django-celery-results`
- add `'django_celery_results'` to settings.py INSTALLED_APPS.
5. Install [django-celery-beat(https://github.com/celery/django-celery-beat) to allocate tasks to celery (redis will stand in between as broker to enforce the rules)
`pip install -U django-celery-beat`
- add `'django_celery_beat'` to settings.py INSTALLED_APPS, and beat settings.
6. Create celery.py in astrium folder
9. reate tasks.py in mainapp folder.
After user selects stocks, the task will be added in celery, which will call it every n seconds. Then it will call 3rd party API and use the web sockets to update the securities.
If multiple users are selecting stocks on the site, it will combine the selections into one task, to reduce the number of server calls. If the stocks are common to both, it will add those, but if the selections are not common, then celery will call the 3rd party API by passing the other selections as new arguements.
The data will be filtered to send the correct stocks to the correct user. It reduces API calls.
Celery is independent of users, so it could also be configured to call the API periodically in one go and store all the data in a database.
(but currently in this dev version, the tasks will only run when a user makes a call)
In production version, we could use web sockets to make calls from our own database and update the front end using web sockets.
10. Copy `available_securities` code from views.py to tasks.py
11. Check if celery is working: add task to celery.py, pass all the desired security (arguements dynamically allocated to the scheduler).
If task is added directly inside beat scheduler, the task would automatically be allocated to celery every n seconds, even if no user is on the front-end. This is not desired functionality, so custom code for web sockets will be used later.
12. Add code to __init__.py of astrium dir. And add `app.autodiscover` to celery.py
13. Apply migrations:
`python manage.py migrate`
`python manage.py makemigrations`
`python manage.py migrate`
14. Create a superuser:
`python manage.py createsuperuser` (pweadmin)
15. Test the server: `python manage.py runserver`
http://127.0.0.1:8000/admin/
16. Install redis:
`pip install redis`
17. Start new celery task: Open new terminal (if using windows, need to use either eventlet, gevent, or pool=solo).
OSX or Linux server:
`redis-cli shutdown`
`redis-server` (in new shells)
- Start worker:
`celery -A astrium.celery worker --pool=solo -l info`
18. Start celery_beat:
`celery -A astrium beat -l INFO`
- In site admin, click "Periodic tasks", to see the task added. Click on the task, click arguments tab to see the args.

# Use websockets to auto update front end
Server automatically sends a response.
1. Install django channels:
`pip install channels`
2. Switch from wsgi server to asgi server:
- Add `channels` to installed apps in settings.py.
- Copy below code to asgi.py:
https://channels.readthedocs.io/en/stable/installation.html
- Add `ASGI_APPLICATION = "myproject.asgi.application"` to settings.py
4. In main_app dir, create consumers.py, routing.py
5. Paste django channels [chat/routing.py code](https://channels.readthedocs.io/en/stable/tutorial/part_2.html) in routing.py and replace 'chat' with security in the regex path. Change consumer to SecurityConsumer.
In django channels when making a web socket connection it consists of a group and channel. Channel is specific to a user who wants to make a socket connection with the server. A unique channel ID will be assigned to the user, and the user is added to a group. Multiple users can be added to a group.
- Make a common group called securitygroup. The group will rcieve the live price updates.
- In consumers.py, make new consumer with code from: https://channels.readthedocs.io/en/stable/tutorial/part_3.html
- create `send_security_update` in the consumer and rename chat. It will call the function to send the data to the web socket. Celery will use one broadcast method and send the data to the group, to which all the users will be connected. Then, the send_security_update function will be used, because for each user, a seperate object will be created, specific to each user socket connection. The send_security_update function will be called from the object to send the data to the user.
As soon as someone selects securities on our website, then a web socket connection will be established between user and server, for as long as the connection persists. During that time, the selected securities will be added in the celery worker task, and celery will call the third-party APIs to retrieve the data for the socks.
6. Make a socket connection between user and server:
- add socket connection in securitytracker.html with JS.
7. Set group name in context data, within views.py. Add the room name too.
8. Add AuthMiddlewareStack to asgi.py, to handle websockets protocol.
9. Add redis as a channel layer to settings.py. It will store details on groups and channels. And:
`pip install channels-redis`
- Refresh the page and it should return a websocket handshake (check in the chrome console or shell).
10. Configuration for how the server sends data to front end:
- Task was previousy in celery beat, but we don't want it to schedule automatically. We want it to dynamically schedule, so that we can add and delete tasks from the periodic task table within our database.
- Add tasks inside connect method, inside celery beat schedule, so it can tell celery to perform that task. Add:
a. Parse query_string.
b. Add to celery beat - Create a new task for performing a django ORM operation to add a new record in the db table. We can't perform it directly within the async function, so need to create a sync function, addToCeleryBeat().
11. In tasks.py, send data to group.
`pip install asyncio`
12. Set recieve function in consumers.py - broadcast to all users for now, to check it is working on client side.
13. Start server, but before starting celery server, delete existing task to avoid errors. In django admin, delete the task from periodic tasks, and from intervals.
Also delete all task results. Then  run and check:
- `celery -A astrium.celery worker --pool=solo -l info`
- `celery -A astrium beat -l INFO`
It should return a socket connection and the sheduler should be updated.
14. In the stocktracker.html, create another event to log output to console when data is recieved from web socket.
```python
stockSocket.onmessage = function (e)...
```
15. In tasks.py, 
- Restart workers and check.
16. Convert nans to NULLS in backend so they can be parsed as JSON.
`pip install simplejson`
-Add it to tasks.py and amend the get_quote_table call with `for (const [key, value] of Object.entries(data)) {...` for loop to iterate over the parsed object using JSON.parse. In JS, there is no dict data structure, its an object. GetElementById and give the id to every element that is stored in the table. Add the id to all fields.

# Make data specific to each user
1. pass data to table:
- Update JS script in securitytracker.py to use web socket to update table every n seconds.





# Run server for testing
source astenv/bin/activate
cd astrium
python manage.py runserver






https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash
https://github.com/frederickvandenberg/crypto-dashboard
https://github.com/bendgame/MediumFinance/pulse
https://medium.com/swlh/how-to-create-a-dashboard-to-dominate-the-stock-market-using-python-and-dash-c35a12108c93
https://github.com/Hiteshhegde/dash-stock-app/blob/main/ticks.csv
