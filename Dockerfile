FROM reskyner/django-luigi-docker

SHELL ["/bin/bash", "-c"]

EXPOSE 5432
EXPOSE 8082

# Git pull pipeline
RUN git clone https://github.com/xchem/pipeline.git
RUN chmod -R 777 pipeline/
WORKDIR pipeline/

RUN adduser postgres

# add settings file for django
RUN chown postgres settings_docker_django.py
RUN chmod 777 settings_docker_django.py
RUN mv settings_docker_django.py settings.py
RUN chmod 777 settings.py
RUN chown postgres run_services.sh
RUN chmod 777 run_services.sh

# mkdir for database files
RUN mkdir database/
RUN mkdir database/db_files
RUN chown postgres database/
RUN chown postgres database/db_files
RUN chmod 777 /tmp

# Run the rest of the commands as the 'postgres' user
USER postgres
WORKDIR /pipeline
