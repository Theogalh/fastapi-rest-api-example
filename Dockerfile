

# Pull base image
FROM python:3.7
# Install dependencies
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app
ENV PLATFORM=docker
EXPOSE 8080
CMD ["python3", "app/main.py"]