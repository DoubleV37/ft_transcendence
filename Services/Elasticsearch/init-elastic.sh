#!/bin/bash

# Attendre que Elasticsearch soit prêt
until curl --output /dev/null --silent --head --fail http://localhost:9200; do
    echo "Waiting for Elasticsearch..."
    sleep 5
done

# Créer un utilisateur
curl -X POST "localhost:9200/_security/user/elasticW" -H 'Content-Type: application/json' -d'
{
 "password" : "votre_mot_de_passe",
 "roles" : [ "superuser" ],
 "full_name" : "Elastic W",
 "email" : "elasticW@example.com",
 "metadata" : {
    "intelligence" : 10
 },
 "enabled": true
}
'
