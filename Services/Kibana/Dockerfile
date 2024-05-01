FROM docker.elastic.co/kibana/kibana:8.13.2

# Définir le répertoire de travail
WORKDIR /usr/share/kibana

# Copier le fichier de configuration kibana.yml dans le conteneur
# Assurez-vous que le fichier kibana.yml est dans le même répertoire que votre Dockerfile
COPY kibana.yml /usr/share/kibana/config/kibana.yml

# Exposer le port par défaut de Kibana
EXPOSE 5601

# Lancer Kibana
CMD ["kibana"]
