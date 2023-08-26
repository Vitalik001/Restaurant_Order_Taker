FROM python:3.9

WORKDIR /code

COPY requirements.txt /code/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

COPY . /code/app

CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-dir", "/code/app"]