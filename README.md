# NanomineViz
visualization for nanomine project

# Installation
- install [whyis](http://tetherless-world.github.io/whyis/install) using this command
  ```
  bash < <(curl -skL https://raw.githubusercontent.com/tetherless-world/whyis/release/install.sh)
  ```
- whyis will be installed in /apps/whyis
- install NanomineViz app following:
  ```
  cd /apps
  sudo git clone https://github.com/raymondino/NanomineViz.git
  cd /apps/NanomineViz/data
  sudo wget https://raw.githubusercontent.com/tetherless-world/nanomine-ontology/master/xml_ingest.setl.ttl
  sudo wget https://raw.githubusercontent.com/tetherless-world/nanomine-ontology/master/ontology.setl.ttl
  sudo chown -R whyis:whyis /apps/NanomineViz
  sudo su - whyis
  cd /apps/NanomineViz
  pip install -e .
  exit
  sudo service apache2 restart
  sudo service celeryd restart
  sudo su - whyis
  cd /apps/whyis
  python manage.py createuser -e (email) -p (password) -f (frstname) -l (lastname) -u (username) --roles=admin
  python manage.py load -i /apps/NanomineViz/data/viz.ttl -f turtle
  cd /apps
  touch .netrc
  ```
- after you create the .netrc file under /apps, you need to edit this file.
  ```
  machine some_url (like 129.105.90.149)
  login some_username (like testuser1)
  password some_password (like testpwd1)
  ```
- after you edit the .netrc file, in your terminal type:
  ```
  cd /apps/whyis
  python manage.py load -i /apps/NanomineViz/data/ontology.setl.ttl -f turtle
  python manage.py load -i /apps/NanomineViz/data/xml_ingest.setl.ttl -f turtle
  ```
- go to http://localhost/ to login with your credentials during "createuser" command
- go to http://localhost/viz to access the visualization

# Developing mode
Each time a change is made on the visualization, apache2 and celeryd service have to be restarted manually. 
This is very troublesome. whyis has a developing mode that help you allevate this pain. 
```
sudo su - whyis
cd /app/whyis
python manage.py runserver -h 0.0.0.0
``` 
The visualization then will be accessed on "http://localhost:5000/viz".
Then, you only need to refresh your webpage to see your changes immediately after you make changes to the visualization. 
After you finished the visualization changes, you can shutdown the developing mode with CTRL+c.
Then you have to restart apache2 and celeryd service by
```
sudo service apache2 restart
sudo service celeryd restart
```
After this, the updated visualization app will show up at "http://localhost/viz".
