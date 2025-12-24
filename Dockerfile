FROM python:3.14
# Python'a diyoruz ki: "Logları saklama, hemen yüzüme vur." (Hata ayıklama için şart)
ENV PYTHONUNBUFFERED=1
# "Gereksiz .pyc dosyaları oluşturup konteyneri şişirme."
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /okuldayiz

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY okulproj/requirements.txt /okuldayiz/

RUN pip install -r requirements.txt

COPY . /okuldayiz/

CMD ["python", "okulproj/manage.py", "runserver", "0.0.0.0:8000"]