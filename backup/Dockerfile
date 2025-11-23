FROM postgres:13

WORKDIR /app


COPY backup.sh .


RUN chmod +x backup.sh


CMD ["./backup.sh"]