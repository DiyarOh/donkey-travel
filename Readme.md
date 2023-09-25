Hoe zet je het project op.
Op MacOS:
docker compose run web django-admin startproject donkeytravel .
Op Windows: is het mogelijk dat je sudo nodig heb
docker compose run web django-admin startproject donkeytravel .


Om docker te installeren op Windows is het makkelijkste om deze tutorial te volgen om een sample project te maken.

https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/

Vervolgens als dit gelukt is pull je deze repository en volg je de stappen hierboven

Update READme

Om andere functies uit te voeren in de docker terwijl deze runt
docker exec -t -i b65d457ff653 bash

docker-compose run web python {en dan wat je wilt doen}