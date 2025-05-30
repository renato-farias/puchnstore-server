FROM python:3.10-alpine@sha256:0733909561f552d8557618ee738b2a5cbf3fddfddf92c0fb261b293b90a51f12 AS builder

WORKDIR /app

ENV POETRY_VERSION=1.8.3 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_HOME="/opt/poetry" \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

## install system deps
# RUN apk add postgresql-libs
# RUN apk add --virtual .build-deps
RUN python -m pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION" && poetry --version

RUN mkdir -p /build/app/source/
ADD pyproject.toml /build/app/source/

WORKDIR /build/app/source
RUN poetry install --no-interaction --no-ansi
# RUN apk --purge del .build-deps

RUN adduser -D -s /bin/bash -h /home/pushnstore pushnstore

WORKDIR /home/pushnstore/app

RUN mkdir -p uploads

ADD app.py /home/pushnstore/app/

RUN rm -rf /build

FROM scratch

COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group

USER pushnstore

COPY --from=builder --chown=pushnstore:pushnstore /usr/local/lib /usr/local/lib
COPY --from=builder --chown=pushnstore:pushnstore /usr/local/bin /usr/local/bin
COPY --from=builder --chown=pushnstore:pushnstore /usr/lib /usr/lib
COPY --from=builder --chown=pushnstore:pushnstore /lib /lib
COPY --from=builder --chown=pushnstore:pushnstore /home/pushnstore/app /home/pushnstore/app

EXPOSE 8080

WORKDIR /home/pushnstore/app

ENV HTTP_HOST=0.0.0.0

ENTRYPOINT ["/usr/local/bin/python3"]

CMD ["app.py"]
