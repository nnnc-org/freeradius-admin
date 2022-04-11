FROM python:3.10-alpine as base

# Build psycopg2 from source & install npm modules
FROM base as builder
                                                                                                                              
RUN mkdir /install && apk --update add \
        libffi-dev \
        postgresql-dev \
        gcc \
        python3-dev \
        musl-dev
WORKDIR /install
RUN echo -e "psycopg2-binary==2.8.6\nmozilla-django-oidc==2.0.0" > /requirements.txt && \
    pip install --upgrade pip && \
    pip install --user -r /requirements.txt

FROM base

# Copy compiled python modules from other container
COPY --from=builder /root/.local /root/.local

# Setup Environment
ENV PYTHONUNBUFFERED 1

# Tmp Env Vars for Django to run
ENV DEBUG False
ENV DB_NAME 'postgres'
ENV DB_USER 'postgres'
ENV DB_PWD 'postgres'

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

# Install Packages
RUN mkdir /project && apk --no-cache add libpq
WORKDIR /project

# Install dependencies via pip
ADD requirements.txt /project/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Add code
ADD ./src/ /project/

ADD entrypoint.sh /
CMD [ "/entrypoint.sh" ]
