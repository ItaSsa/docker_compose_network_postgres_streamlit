FROM python:3.12
RUN pip install poetry
COPY . /src
WORKDIR /src
RUN poetry install --no-root
EXPOSE 8501
ENTRYPOINT ["poetry","run", "streamlit", "run", "./app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
