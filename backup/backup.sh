
FROM mysql:5.7

WORKDIR /app
COPY backup.sh .

RUN chmod +x backup.sh

CMD ["./backup.sh"]