FROM python:3.12
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["bash", "entrypoint.sh"]
EXPOSE 8000
