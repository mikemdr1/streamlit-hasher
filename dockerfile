FROM python:3.11.6-slim-bullseye

LABEL author="Miguel Hinojosa"
LABEL description="Application built in Streamlit for demostrate the use of bcrypt"

COPY app.py /home/app/app.py
COPY pyproject.toml /home/app/pyproject.toml
COPY .streamlit /home/app/.streamlit

WORKDIR /home/app

RUN pip install poetry
RUN poetry install

EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "app.py"]