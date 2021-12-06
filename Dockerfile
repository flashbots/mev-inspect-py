FROM python:3.9

RUN pip install -U pip \
    && apt-get update \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH="${PATH}:/root/.poetry/bin"

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock
WORKDIR /app/

RUN poetry config virtualenvs.create false && \
    poetry install

COPY . /app

# easter eggs 😝
RUN echo "PS1='🕵️:\[\033[1;36m\]\h \[\033[1;34m\]\W\[\033[0;35m\]\[\033[1;36m\]$ \[\033[0m\]'" >> ~/.bashrc

ENTRYPOINT [ "poetry" ]
CMD [ "run", "python", "loop.py" ]
