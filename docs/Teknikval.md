# Teknikval

Följande dokument är en lista på alla de teknik val som gjorts, vad de används till och varför.



## Språk

 - Python.
 - HTML5
 - CSS
 - Javascript

 Eftersom django är skrivet i python och det är det språket som Johan kan bäst så blir det bästa valet.



## Webbramverk

 - Django

Även här är valet uppenbart för django är det som Johan har mest erfarenhet av och det är det största webbramverket inom python världen.



## Databas

Det finns 2 alternativ här som vi kan välja mellan, MySQL och PostgreSQL men i slutändan så kommer det att bli PostgreSQL för att den är mycket enklare att arbeta med och "bara funkar" i jämförelse mot MySQL. En annan stor anledning är att PG har bra stöd för GIS (Geographical Information Services) och kan göra map querries som vi kan ha behov av i framtiden när google maps integration görs klart.



## Sök motor

Även här finns det 2 stora alternativ som måste tas ställning till. De 2 som vi kan använda oss av är Apache Solr och ElasticSearch. Fördelen med Solr är att Johan har en hel del erfarenhet genom fyndiq i setup/funktionalitet/drift osv men Solr har lite prestanda problem i vissa fall och då skulle ES vara en bättre kandidat.  Men på andra sidan så är ES ett sämre alternativ pga för lite erfarenhet av den. Det kan vara så att vi byter längre in i utvecklingen men till en början så bör det vara Solr.



## Msg queue

Vi har behov av async msg queue och här är det enkelt att välja för RabbitMq broker och celery worker är defakto standard och det finns inte någon stor annan kandidat som vi kan använda för produktion. Vi skulle kunna använda en enklare lösning i dev där man inte har rabbitmq utan man kör med redis som broken men det finns egentligen ingen vinst med att göra detta.
Våran Msg queue kommer i största del användas för att indexera information från databasen ner till sök motorn och att skicka email för olika events.



## Virtiualisering

Den enda supportade lösningen skall vara Docker. Eventuellt att man bygger in stödet i fabric så att man kan deploya samma sak på olika plattformar. Docker är ett bra alternativ för att det fungerar på alla plattformar out of the box och det är enkelt att testa med. Ett problem som kan uppstå är om produktions deploy fungerar eller inte med docker och det kan tvinga oss till fabric lösningen. Docker bör utvecklas under development och när det blir dags för produktions deployment så får vi ta en funderare då.



## Frontend design/libs

Libs och liknande som vi använder oss av just nu är

- Django suit
- jQuery
- DateTimePicker (jQuery)
- django-datetime-widget (Hjälp för DateTimePicker)
- Bootstraped 2 (Pga django suit) [Bootstrapped 3 bör användas i slutändan]



## Loggnings

Vi måste ha system för logg aggregering av fel och aktivitets loggar i något system som kan klara av lasten och våra behov.

För exceptions och problem så skall vi använda oss av Sentry. Det är en applikation som hanterar exceptions i django och klarar av stora mängder utan problem. Innan detta kommer på plats så kan vi använda oss av den vanliga standarden att skicka email.

ELK stacken kan vi anävnda oss av för att sköta vanlig server och client loggning.
