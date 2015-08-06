# DOCKER-VERSION 1.1.2
FROM python
COPY . /src
RUN pip install pymysql
CMD ["python", "/src/dedupe/dedupe.py"]