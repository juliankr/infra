from python:3.12
RUN pip install -r requirements.txt
COPY static .
COPY main.py
EXPOSE 8080
ENTRYPOINT ["python", "main.py"]