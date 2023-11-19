FROM python:3.11.4

ENV HOME /src/
WORKDIR ${HOME}

COPY . .

RUN pip install --upgrade pip
RUN pip install poetry
ENV PATH="${PATH}:$HOME/.poetry/bin"

RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 8000
