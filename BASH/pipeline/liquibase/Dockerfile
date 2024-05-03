ARG AWS_ACCOUNT
FROM ${AWS_ACCOUNT}.dkr.ecr.us-east-1.amazonaws.com/dna-ad/tdv-liquibase:1.0.0

COPY ./changelog/. /liquibase/changelog/
COPY ./classpath/. /liquibase/classpath/

COPY ./config/. /liquibase/config/

USER root
RUN chown -R liquibase:liquibase /liquibase
USER liquibase
