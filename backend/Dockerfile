FROM python:3.12
WORKDIR /app

COPY requirements.txt requirements.txt
ARG PIP_EXTRA_ARGS
RUN pip install -r requirements.txt ${PIP_EXTRA_ARGS}
COPY . .
RUN python manage.py collectstatic --noinput

CMD ["bash", "entrypoint.sh"]
EXPOSE 8000
