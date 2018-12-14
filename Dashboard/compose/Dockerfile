FROM python:3.6 as base
ENV PYTHONUNBUFFERED 1
RUN mkdir /pyfaas
COPY compose/requirements.txt /pyfaas
RUN pip3.6 install -r /pyfaas/requirements.txt

FROM base
COPY . /pyfaas
WORKDIR /pyfaas
RUN ls
EXPOSE 9000
RUN chmod +x server.py
ENTRYPOINT [ "python3.6" , "server.py" ]