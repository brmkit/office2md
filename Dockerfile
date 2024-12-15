# Use Python base image
FROM python:3.12-slim

WORKDIR /src
COPY src/ /src/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9000

CMD ["python", "main.py"]