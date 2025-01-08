FROM python:3.9-slim
RUN apt-get update && apt-get install -y openssh-server && rm -rf /var/lib/apt/lists/*
RUN pip install paramiko
WORKDIR /honeypot
COPY . .
RUN useradd -m honeypot && mkdir /honeypot/logs && chown -R honeypot:honeypot /honeypot
RUN chmod 755 /honeypot && chmod -R 755 /honeypot/logs
EXPOSE 2222
CMD ["python3", "Honeypot-SSH.py"]
