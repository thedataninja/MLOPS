This is the code to implement name entity recognition (NER) system
It can be used a machine learning project in production to implement (NER) system


intent_entity_detection/views.py -- Flask API file which is gets the request call model which makes prediction and returns the json object
Dockerfile --  Creates docker package 
kubernetes/deployment.yaml -- Kubernetes deployment yaml file
kubernetes/service.yaml -- Kubernetes service yaml file
run.py - 
supervisord.conf -- Config for supervisor deamon which runs the tensorflow serving and flask deamon
