# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install tensorflow uvicorn gunicorn fastapi scikit-learn numpy scipy

COPY . .

EXPOSE 3100

CMD ["gunicorn", "main:app"]