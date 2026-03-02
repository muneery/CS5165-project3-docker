FROM python:3.11-slim

WORKDIR /app

# Copy script
COPY scripts.py /app/scripts.py

# Copy data into required container path
RUN mkdir -p /home/data/output
COPY data/IF.txt /home/data/IF.txt
COPY data/AlwaysRememberUsThisWay.txt /home/data/AlwaysRememberUsThisWay.txt

# Run script automatically when container starts
CMD ["python", "/app/scripts.py"]
