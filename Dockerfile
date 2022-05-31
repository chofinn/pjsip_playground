FROM ubuntu:20.04
COPY ./myrecorder.py ./
COPY ./pjsip-install.sh ./
RUN chmod +x pjsip-install.sh
RUN ./pjsip-install.sh
CMD python3 myrecorder.py
