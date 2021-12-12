from python:3.9.9-slim-buster
RUN pip install requests
RUN pip install CherryPy
COPY signalWebhook.py .
EXPOSE 8080
ENTRYPOINT ["python", "signalWebhook.py"]