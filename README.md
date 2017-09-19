# Рейтинг выделенных полос

В этом контейнере (виртуальной машине) Docker лежат все скрипты, необходимые чтобы посчитать показатели рейтинга и сверстать страницу сайта. Вы можете взять эти файлы и пользоваться ими только для расчётов.

Для удобства, здесь описано, как работает весь цикл.

# Предварительная подготовка

## Установка Docker

1. Скачайте и установите Docker [Community Edition](https://www.docker.com/community-edition/) (Docker CE).
2. Скачайте и установите [Docker-Compose](https://docs.docker.com/compose/install/)

Теперь можно собирать контейнер.

## Сборка контейнера

Зайдите в командной строке в корневую папку проекта dedicated-lanes (в которой лежит `docker-compose.yml`) и запустите сборку командой:

    docker-compose build

Вы увидите как Docker скачивает образы Ubuntu и устанавливает пакеты для Питона.

# Запуск контейнера

Можно не менять параметров скриптов и сразу запустить выполнение расчётов.

    docker-compose up

Эта команда запустит контейнер и в нём - команду `make`, которая вызовет скрипты, считающие данные. Когда скрипт закончится, контейнер прекратит работу автоматически. Если всё прошло хорошо, файлы с результатами будут лежать в папке `calculator/build`.

Чтобы пересчитать данные, надо просто снова запустить эту команду `docker-compose up`.


# Входные данные

1. Ссылка на скачивание карты находится в `calculator/Makefile`:

      wget https://www.google.com/maps/d/kml?mid=1PWvRWfdKEV4SVs5ONkDgRPLbRiQ -O $@

  Если вы хотите считать по другой карте, скачайте файл kml/kmz, откройте его, и из XML достаньте аналогичный URL и вставьте на это место в Makefile.

  Чтобы обновить файл с векторной картой, достаточно удалить файл `calculator/data/lanes.kmz`. GNU Make заметит, что файл из цепочки сборки исчез и переделает его, а затем, т.к. он обновился - каскадно обновит все следующие.

2. Имена слоёв. В текущей версии имена слоёв написаны прямо в коде, в файле `calculator/parsekml.py`.

      if f.name == 'односторонние сущ.':
          lanes = 1

   Нужно будет вставить сюда имя слоя в кавычках. Если вы поменяете этот файл, все данные будут снова пересчитаны (при этом `lanes.kmz` и `doc.kml` не будут обновляться, т.к. не они зависят от этого скрипта, а наоборот, данные на выходе зависят от них - см. Makefile).

3. Контуры муниципалитетов лежат в файле `calculator/src/muni.geojson`. Его можно редактировать в QGIS или ArcGIS или вставить на его место новый. Новый файл должен иметь систему координат 4326 (WGS84), обратите на это внимание, когда сохраняете файл. Объекты в этом файле должны иметь названия текстом.

4. Численность населения находится в `calculator/src/city-population.csv`. Чтобы скрипт взял отсюда численность населения, имя города в этом файле должно быть в поле имени города в названном выше файле `muni.geojson`, например для строки с именем `Иваново` скрипт `match-cities.py` найдёт объект с названием `городской округ Иваново` (регистр букв не важен). Скрипт `match-cities.py` может найти города, заканчивающиеся на мягкий знак, например, Пермь-Пермский [городской округ].

**Чтобы пересчитать файл, нужно запустить** `docker-compose up`. При запуске GNU Make определит, какие файлы обновились и должны быть перерассчитаны.

# Веб-страница

Скрипт складывает файлы GeoJSON в папку `calculator/build`, и из них данные вставляются в шаблон `calculator/html/index.template.html`. Язык шаблона - [Jinja2](http://jinja.pocoo.org/docs/2.9/).

# Изменения и перерасчёты

Когда файл в цепочке вычислений изменился или исчез, GNU Make решает, что его нужно создать или изменить, и выполняет команды, которые прописаны в файле (см. [Просто о make](https://habrahabr.ru/post/211751/)). Если вы меняете первые файлы, все последующие будут обновлены.

Веб-страница тоже является файлом в этой цепочке и прописана в `Makefile` и обновится при изменении исходных данных или скриптов.

# Публикация на веб-сервере

Если у вас есть хостинг с SSH, можете поправить и использовать скритп `deploy.sh`. В строке

    webfaction:~/webapps/bus_lanes

замените `webfaction` на IP хостинга, а `~/webapps/bus_lanes` на путь к папке, в которой вы выкладываете сайт.


[Дмитрий Лебедев](http://dl.one-giant-leap.info), 2017.
