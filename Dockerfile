FROM fedora:28

RUN dnf -y install git python python2-pip cairo pango && yum clean all
COPY requirements.txt /
RUN pip install -U --user -r /requirements.txt
COPY scrapper.py template.html style.css /

ENTRYPOINT ["python", "/scrapper.py"]
CMD ["--help"]
