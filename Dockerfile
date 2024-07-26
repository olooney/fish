FROM debian:stable-slim

# Recommended Python options for running in short-lived containers.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

RUN apt update && \
    apt install -y --no-install-recommends \
        python3 \
        python3-pip

WORKDIR /app
COPY . .

# this scary looking option bypasses the debian "managed packages" feature
# which encourages people to use venv for local python packages. That's not
# important here because we're installing python from scratch and it will only
# ever be used to run this one command.
RUN pip install --break-system-packages -r requirements.txt
RUN pip install . --break-system-packages

# Create a non-root user
RUN groupadd -r model_user && \
    useradd -r -g model_user -d /app -s /sbin/nologin \
        -c "Non-privileged docker user to run the app." model_user
RUN chown -R model_user:model_user /app

# Expose the port the app runs on
EXPOSE $PORT

# run as model_user
USER model_user
CMD [ "python3", "scripts/run_server.py"]
