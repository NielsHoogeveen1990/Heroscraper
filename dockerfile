# Image that we are using
FROM python:3.6

WORKDIR /app

# Copy file to workdir
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all file in this dir to workdir
COPY . .

# Build the app
RUN python setup.py develop

# Let know that we want to use port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_APP heroes_app/app.py
ENV FLASK_DEBUG True

# Use double quotes
# Entrypoint is run always
# ENTRYPOINT ["flask"]

# This is executed if no other command is specified
CMD ["flask", "run", "--host=0.0.0.0"]

