FROM lgatica/python-alpine:3-onbuild

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN apk update && \
    apk add --update nodejs nodejs-npm

RUN npm install bootstrap jquery popper.js


RUN pip install flask requests

RUN ln -sf /app/node_modules/bootstrap/dist/css/bootstrap.min.css /app/static/css/bootstrap.min.css
RUN ln -sf /app/node_modules/bootstrap/dist/js/bootstrap.min.js /app/static/js/bootstrap.min.js
RUN ln -sf /app/node_modules/jquery/dist/jquery.min.js /app/static/js/jquery.min.js 
RUN ln -sf /app/node_modules/popper.js/dist/popper.min.js /app/static/js/popper.min.js


ENTRYPOINT ["python"]

CMD ["main.py"]