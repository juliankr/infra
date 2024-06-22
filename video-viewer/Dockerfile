from python:3.12
COPY static .
COPY main.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python", "main.py"]