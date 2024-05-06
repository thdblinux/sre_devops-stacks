FROM python:3-slim as build
WORKDIR /app
RUN pip install -r /app/requirements.txt

FROM gcr.io/distroless/python3
COPY --from=build /app /app
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages \ FLASK_APP=/app/app.py 

WORKDIR /app
EXPOSE 5000
ENTRYPOINT python -m flask run --host=0.0.0.0