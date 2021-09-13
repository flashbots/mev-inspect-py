FROM alpine

RUN apk update && apk add expect busybox-extras

ADD ./verify.exp ./verify.exp

ENTRYPOINT expect < verify.exp
