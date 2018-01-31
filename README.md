# NanomineViz
visualization for nanomine project

# Pre-request
- satoru
    - [installation](http://tetherless-world.github.io/satoru/install): (bash < <(curl -skL https://raw.githubusercontent.com/tetherless-world/satoru/master/install.sh))
- ubuntu 14.04 LTS or 16.04 LTS

# Installation
- install satoru, its default installation directory is /apps/satoru
- make sure the virtual environment is activated. (venv) before the prompt indicates that it's on. Otherwise type ```source /apps/satoru/venv/bin/activate``` to activate it.
- configure satoru
  ```
  sudo su - satoru
  cd /apps/satoru
  python manage.py configue
  project_name [My Knowledge Graph]: Nanomineviz 
  project_short_description [An example knowledge graph configuration.]: a visualization web app for nanomine project
  project_slug [my_knowledge_graph]: nv
  location [/apps/my_knowledge_graph]: /apps/NanomineViz
  author [J. Doe]: Rui Yan
  email [j.doe@example.com]: yanr2@rpi.edu 
  linked_data_prefix [http://localhost]: 
  version [0.1]: 
  packages []: 
  SECRET_KEY [J00F5f80rGSbvpUo9oBFAtksmrd7ef8u]: 
  SECURITY_PASSWORD_SALT [JDyCyPu0KEu/fdJr4CbG65VhCtGugwCu]: 
  ```
  This will create a project folder named NanomineViz and all its necessary files:
    - config.py --> main configuration file for NanomineViz app within satoru
    - vocab.ttl --> vocabulary file for configuring custom Satoru views
    - templates/ --> directory for storing Satoru view templates
    - Nanomineviz/ --> project source directory, put any python code in here
        - agent.py --> an empty inference agent module
    - static/ --> files that are served up at {linked_data_prefix}/cdn/ as static files
        - css/ --> project-specific CSS files
            - Nanomineviz.css --> default empty project-specific CSS file
        - html/ --> project-specific static HTML files, like for Angular.js templates
        - js/ --> project-specific javascript files
            - NanomineViz.js --> default empty project-specific javascript file
    - setup.py --> file for installation using pip
- configure loading data directory
    - edit config.py file, change the following values:
  ```
    nanopub_archive = {
        'depot.storage_path' : "/apps/NanomineVizNanopub/nanopublications",
    },

    file_archive = {
        'depot.storage_path' : '/apps/NanomineViz/data',
        'cache_max_age' : 3600*24*7,
    },
  ```
     in this way, Satoru will load the data from /apps/NanomineViz/data directory.
- install NanomineViz app
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