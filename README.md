# NanomineViz
visualization for nanomine project

# Pre-request
- satoru
    - [installation](http://tetherless-world.github.io/satoru/install): (bash < <(curl -skL https://raw.githubusercontent.com/tetherless-world/satoru/master/install.sh))
- ubuntu 14.04 LTS or 16.04 LTS

# Installation
- install satoru first
    - its installation directory: /apps/satoru
- make sure the virtual environment is activated. (venv) before the prompt indicates that it's on. Otherwise type ```source /apps/satoru/venv/bin/activate``` to activate it): 
  ```
  cd /apps
  sudo git clone https://github.com/raymondino/NanomineViz.git
  sudo chown -R satoru:satoru /apps/NanomineViz
  sudo su - satoru
  cd /apps/NanomineViz
  pip install -e .
  exit
  sudo service apache2 restart
  sudo service celeryd restart
  sudo su - satoru
  cd /apps/satoru
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
  cd /apps/satoru
  python manage.py load -i /apps/NanomineViz/data/ontology.setl.ttl -f turtle
  python manage.py load -i /apps/NanomineViz/data/xml_ingest.setl.ttl -f turtle
  ```
- go to http://localhost/ to login with your credentials during "createuser" command
- go to http://localhost/viz to access the visualization