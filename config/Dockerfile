FROM python:3.10-buster as base

RUN echo "deb http://deb.debian.org/debian/ buster contrib non-free\ndeb-src https://deb.debian.org/debian buster contrib non-free" >> /etc/apt/sources.list \
    && apt-get -y update \
    && apt-get install -y \
        ttf-mscorefonts-installer \
        wkhtmltopdf \
    && apt-get -y clean

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb \
    ; apt-get -y --fix-broken install

# Uncomment if you need Google fonts
#RUN wget https://github.com/google/fonts/archive/main.tar.gz -O gf.tar.gz && \
#  tar -xf gf.tar.gz && \
#  mkdir -p /usr/share/fonts/truetype/google-fonts && \
#  find $PWD/fonts-main/ -name "*.ttf" -exec install -m644 {} /usr/share/fonts/truetype/google-fonts/ \; || return 1 && \
#  rm -f gf.tar.gz && \
#  # Remove the extracted fonts directory
#  rm -rf $PWD/fonts-main && \
#  # Remove the following line if you're installing more applications after this RUN command and you have errors while installing them
#  rm -rf /var/cache/* && \
#  fc-cache -f

RUN mkdir /app
COPY requirements.txt /app/

WORKDIR /app
RUN ls /app && pip install -U pip setuptools wheel pylint  && \
  pip install -r requirements.txt

COPY . .