FROM python:3.9-slim-buster

ENV POETRY_VERSION=1.1.12

RUN useradd --create-home flashbot \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential libffi-dev libpq-dev gcc procps \
    && pip install poetry==$POETRY_VERSION \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:/home/flashbot/.local/bin"

COPY --chown=flashbot ./pyproject.toml /app/pyproject.toml
COPY --chown=flashbot ./poetry.lock /app/poetry.lock
WORKDIR /app/

USER flashbot

RUN poetry config virtualenvs.create false \
    && poetry install

COPY --chown=flashbot . /app

# easter eggs 😝
RUN echo "PS1='🕵️:\[\033[1;36m\]\h \[\033[1;34m\]\W\[\033[0;35m\]\[\033[1;36m\]$ \[\033[0m\]'" >> ~/.bashrc

ENTRYPOINT [ "poetry" ]
CMD [ "run", "python", "loop.py" ]
