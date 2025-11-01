from python:3.13
RUN pip install requests
RUN pip install CherryPy
COPY signalWebhook.py .
EXPOSE 8080
ENTRYPOINT ["python", "signalWebhook.py"]