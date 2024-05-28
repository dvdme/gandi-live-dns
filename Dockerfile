FROM python:3.11

LABEL maintainer=https://github.com/dvdme
LABEL version="1.0.0"

COPY . /usr/src/gandi_live_dns
WORKDIR /usr/src/gandi_live_dns

# Install script requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "gandi_live_dns.py"]

CMD ["python3", "gandi_live_dns.py", "--help"]
