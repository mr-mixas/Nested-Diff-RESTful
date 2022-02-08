FROM python:3.10-alpine

ARG workdir=/app

ADD static ${workdir}/static
ADD templates ${workdir}/templates
COPY api.py requirements.txt run.sh ${workdir}/

WORKDIR ${workdir}

ENV VIRTUAL_ENV=${workdir}/venv
RUN python -m venv ${VIRTUAL_ENV}
ENV PATH=${VIRTUAL_ENV}/bin:${PATH}

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/sh"]
CMD ["run.sh"]
