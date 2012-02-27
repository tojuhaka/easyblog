EasyBlog
========

:Author: Toni Haka-Risku
:Version: 0.1-dev

Introduction
------------
EasyBlog is just a test for pyramid. Main goal is to test different features of pyramid. During development I was asked to create a webpage that contains Authorization-policy, user-management, blogging and news. So I let this project to fulfill those requirements. After a little bit of refactoring it's not a test-project anymore. 

EasyBlog uses ZODB and traversal. Main reason for that is my experience from Plone and Zope. And yes, I like OO-databases. 

Layout is taken from freewebtemplates.com and is designed by Dcarter Design. So let's give them some credits for that. The layout is integrated to pyramid using compass (CSS-framework that uses SASS). 

Products I've used for developing:
    * pyramid_simpleform 
    * compass


Small code-explanation:
    models.py 
        includes all the models which will act as "resources" in our resource tree.
    views.py 
        all the views goes to here.
    schemas.py 
        schemas for pyramid_simpleform. All the form validation code goes here
    interfaces.py 
        mostly for marker interfaces.
    tests.py 
        all the tests. I'm trying to keep up 100% test-coverage.
    config.py 
        (hardcode stuff. We should remove this after the project is finished)
    __init__.py 
        configuration for our project.
    subscribers.py 
        events goes here
    utilities.py 
        some tools we've created to support views and models
    security.py 
        contains security-related code like permission handling, password hashing etc

Installation
------------

Just clone or use buildout configuration::

    [buildout]
    eggs-directory = ${buildout:directory}/eggs
    parts = easyblog

    extensions = mr.developer
    auto-checkout = easyblog
    sources = sources

    [sources]
    easyblog = git http://github.com/tojuhaka/easyblog.git

    [easyblog]
    recipe = zc.recipe.egg
    eggs = easyblog
    entry-points = pserve=pyramid.scripts.pserve:main


Dokumentaatio (in finnish)
==========================

Alkusanat
---------
Työn tarkoituksena on toteuttaa Jyväskylän Saapas RY:lle web-sivut. Sivujen tarkoituksena
on edistää yhdistyksen ulkoista sekä sisäistä viestintää. Samalla sivujen tulisi kuvata
mahdollisimman tehokkaasti yhdistyksen toimintaa. 

Asiakkaan vaatimukset
---------------------
Kyseessä on hyväntekeväisyys yhdistys, joten taloudellisten rajoitteiden vuoksi sivuston tarkoitus
ei ole olla kovinkaan "massiivinen".  Tämä ei kuitenkaan tarkoita sitä, että sivuston ominaisuudet
toteutettaisiin puutteellisesti. Tärkeintä on priorisoida yhdistyksen tärkeimmät tarpeet ja tuoda ne 
sivustolle mahdollisimman selkeästi ja yksinkertaisesti.  

Lyhyesti tarkasteltuna, yhdistyksen toiminnalle tärkeää on tiedotus erilaisista tapahtumista. Myös
tiettyjen yhdistyksen henkilöiden tulisi pystyä kertomaan omista kokemuksistaan "blogimaisesti". 
Yhdistyksellä ei ole vielä minkäänlaista web-sivustoa, joten lähtötaso on hyvin matala. Tästä syystä
sivuston painoarvo itsessään on jo hyvin suuri.

Seuraavassa listaus vaatimuksista, jotka sivujen tulisi toteuttaa:
    - Sivujen tulee olla yksinkertaiset
    - Mitään web-ohjelmointi taitoa ei tarvita sivustojen ylläpitämiseen
    - Uutisten/tiedotteiden lisääminen/hallinta
    - Blogejen lisääminen/hallinta
    - Uusimmat tiedotteet tulee näkyä etusivulla
    - Etusivun tulee olla mahdollisimman informatiivinen 
    - Tietoturva tulee olla kunnossa
    - Sisältöä pystyy luomaan sivuston ylläpitäjät.
    - Sivuston ylläpitäjien tulee pystyä hallitsemaan muiden
      käyttäjien oikeuksia, jollain tasolla
    - Ulkoasun värimaailma tulisi olla syksyinen (oranssi/musta)


Omat vaatimukset
----------------
Kyseessä on ohjelmointityö, jonka on tarkoitus olla myös oppimiskokemus. Tarkoituksena ei siis ole 
vain tehdä liukuhihnalla web-sivut, jotka ovat asiakkaan mieleen. Niin hauskalta kuin se kuulostaakin,
niin tarkoitus on projektin aikana tehdä jotain väärin ja oppia tästä. Seuraavassa listaus vaatimuksista,
joita projektin aikana itse noudatan:
    - Suunnitteluun käytetyn ajan tulee olla mahdollisimman lyhyttä. Liika suunnittelu tällaisissa projekteissa
      on aina pahasta. Tämä ei kuitenkaan tarkoita, että suunnittelu jätetään väliin.
    - Ohjelmakoodin testaaminen kokonaisvaltaisesti. Testejen tulee kattaa koko ohjelmakoodi ja aina jos on mahdollista,
      niin testit kirjoitetaan ennen ohjelmakoodia.
    - Ohjelmakoodia tulee refaktoroida kokoajan.
    - Epäselvältä vaikuttava ohjelmakoodi on kommentoitava selkeästi. 
    - Liika ohjelmakoodin opimointi ja "tuijottelu" jätettävä pois. Tähän sorrun itse hyvin usein ja se syö turhaa aikaa. Jossain vaiheessa
      ratkaisut on kuitenkin tehtävä, jotta päästään eteenpäin.
    - Asiakkaalle tulee näyttää "prototyypin" omaisesti sivuja mahdollisimman usein.


Välineet ja menetelmät
----------------------

Toteutus
--------



