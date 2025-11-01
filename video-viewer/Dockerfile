from python:3.13
COPY static/ ./static/
COPY main.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python", "main.py"]