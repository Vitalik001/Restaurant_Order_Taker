FROM python:3.9

WORKDIR /code/front

COPY requirements.txt /code/front/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/front/requirements.txt

COPY . /code/front

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
