FROM docker.elastic.co/elasticsearch/elasticsearch:8.13.2

# Copier le fichier de configuration elasticsearch.yml dans le conteneur
# Assurez-vous que le fichier elasticsearch.yml est dans le même répertoire que votre Dockerfile
COPY --chown=elasticsearch:elasticsearch elasticsearch.yml /usr/share/elasticsearch/config/

COPY --chmod=777 --chown=elasticsearch:elasticsearch init-elastic.sh /usr/local/bin/

# Exposer les ports par défaut d'Elasticsearch
EXPOSE 9200 9300

# Lancer Elasticsearch
# CMD ["sh", "-c", "elasticsearch & /usr/local/bin/init-elastic.sh"]

CMD ["elasticsearch"]
