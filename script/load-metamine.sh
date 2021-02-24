python manage.py load -i ../nanomine-graph/setl/materialsmine.ttl -f turtle
python manage.py load -i 'http://vocab.deri.ie/void' -f xml
python manage.py load -i 'http://purl.org/dc/terms' -f xml
python manage.py load -i ../SemanticDataDictionary/sdd-ontology.ttl -f turtle
python manage.py load -f xml -i https://github.com/MaastrichtU-IDS/semanticscience/raw/master/ontology/sio/release/sio-subset-labels.owl
