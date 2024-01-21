FROM python:3.12-alpine

ARG workdir=/app
WORKDIR ${workdir}

ENV VIRTUAL_ENV=${workdir}/venv
RUN python -m venv ${VIRTUAL_ENV}
ENV PATH=${VIRTUAL_ENV}/bin:${PATH}

RUN pip install --upgrade pip
RUN pip install nested_diff_restful

ENTRYPOINT ["nested_diff_restful"]
