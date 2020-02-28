FROM postgres:12.2-alpine
COPY init.sql /docker-entrypoint-initdb.d
ENV POSTGRES_USER=docker
ENV POSTGRES_HOST_AUTH_METHOD=trust
ENV POSTGRES_DB=trafficflow
EXPOSE 5432
CMD ["postgres"]
