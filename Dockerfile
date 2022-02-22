FROM python:3.10-alpine as base

# Build psycopg2 from source & install npm modules
FROM base as builder
                                                                                                                              
RUN mkdir /install
RUN apk --update add \
        libffi-dev \
        postgresql-dev \
        gcc \
        python3-dev \
        musl-dev \
        yarn \
        xmlsec \
        make \
        cmake \
        build-base \
        py3-lxml py3-pillow py3-pybind11-dev python3-dev py3-pybind11 py3-wheel qpdf-dev

WORKDIR /install

#ADD package.json ./
#ADD yarn.lock ./
RUN echo -e "psycopg2-binary==2.8.6\ndjangosaml2==1.3.5" > /requirements.txt && \
    pip install --upgrade pip && \
    pip install --user -r /requirements.txt 
    # && yarn install

FROM base

# Copy compiled python modules from other container
COPY --from=builder /root/.local /root/.local

# Copy NPM Modules
#COPY --from=builder /install/node_modules /node_modules

# Setup Environment
ENV PYTHONUNBUFFERED 1

# Tmp Env Vars for Django to run
ENV DEBUG False
ENV DB_NAME 'postgres'
ENV DB_USER 'postgres'
ENV DB_PWD 'postgres'

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

RUN mkdir /project
WORKDIR /project

# Install Packages
#RUN apk --no-cache add libpq xmlsec qpdf-dev
RUN apk --no-cache add libpq xmlsec

# Install dependencies via pip
ADD requirements.txt /project/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Add code
ADD ./src/ /project/

ADD entrypoint.sh /
CMD [ "/entrypoint.sh" ]
