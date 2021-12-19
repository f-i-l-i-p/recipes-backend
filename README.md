**Run Local**

1. Clone repo

2. Create and activate virtual environment
``` terminal
$ python3 -m venv .venv
$ source .venv/bin/activate
```

3. Install requirements
``` terminal
$ pip install -r requirements.txt
```

4. Add environment variable
``` terminal
$ export SERVER_SECRET={secret}
```

5. Run
``` terminal
$ python3 -m server.main
```

**Deploy to Heroku**

1. Clone repo

2. Create a new Heroku app.

3. Add a Heroku Postgres database.

4. Add these environment variables to heroku

```
SERVER_SECRET={secret}
NAMESPACE="heroku"
```


5. Push to heroku
``` terminal
$ heroku login
$ heroku git:remote -a {app-name}
$ git push heroku master
```

6. Initialize database
``` terminal
$ heroku run init
```

**Heroku logs**
``` terminal
$ heroku logs --tail
```
