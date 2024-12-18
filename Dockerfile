FROM python:3.12-slim-bullseye

# Add user docker to the container
RUN useradd -ms /bin/bash docker

# Install dependencies for a python app using requirements.txt
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    build-essential

# Create the /app directory in /home/docker with owner docker \
RUN mkdir -p /home/docker/app && chown -R docker:docker /home/docker/app

# Copy requirements.txt to the container
COPY --chown=docker:docker ./requirements.txt /home/docker/app/requirements.txt

# Install dependencies using existing requirements.txt in /home/docker/app/requirements.txt
RUN pip3 install --no-cache-dir -r /home/docker/app/requirements.txt

RUN python -m spacy download en_core_web_sm

WORKDIR /home/docker/app

# Copy the rest of the files with docker user as owner
COPY --chown=docker:docker . .

# Switch to docker user
USER docker

# Create entrypoint for src/app.py via python
ENTRYPOINT ["python3", "src/app.py"]
