# Locksley 
A web-based annotation tool for relation extraction.

## Annotation data
The sentences in the `data` folder are all part of the 10kGNAD corpus that is released under a Creative Commons BY-NC-SA 4.0 license (www.github.com/tblock/10kGNAD). As a result, the sentences here are equally made available under CC BY-NC-SA 4.0 (https://www.creativecommons.org/licenses/by-nc-sa/4.0/). 

## How to load annotation data into the database
You can do so by using the scripts in the `django-unchained/annotation/management/commands` directory.
First, you need to add the `data` directory as a volume to the annotation service in your docker-compose file (cf. example docker-compose.yml in the root folder).
Afterwards, you can execute the scripts as follows:
```
$ docker-compose run annotation [name_of_the_script]
```

Please note that the order in which the different types of data points are loaded matters:
1. `load_corpora.py`
2. `load_relation_types.py`
3. `load_testruns.py`
4. `load_sentences.py`
5. `load_batches.py`
