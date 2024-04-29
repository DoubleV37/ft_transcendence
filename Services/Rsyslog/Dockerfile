FROM alpine:3.18

# Mise à jour des paquets et installation de rsyslog
RUN apk update && \
    apk add --no-cache rsyslog

# Copie de la configuration rsyslog personnalisée
COPY rsyslog.conf /etc/rsyslog.conf

# Démarrage de rsyslog
CMD ["rsyslogd", "-n"]
