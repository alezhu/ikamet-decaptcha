FROM jitesoft/tesseract-ocr:latest-alpine
USER root
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools pytesseract pillow flask

COPY ./src /app
WORKDIR /app
EXPOSE 5000

# USER tesseract
ENTRYPOINT ["python3"]
CMD ["app.py"]
