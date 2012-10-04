EasyBlog
========

:Author: Toni Haka-Risku
:Version: 0.1-dev

Introduction
------------
EasyBlog is a webpage created with pyramid. Main goal is to test different features of pyramid. During development I was asked to create a webpage that contains Authorization-policy, user-management, blogging and news. So I let this project to fulfill those requirements. After a little bit of refactoring it's not a test-project anymore but a webpage for Saapas RY.

EasyBlog uses ZODB and traversal. Main reason for that is my experience from Plone and Zope. And yes, I like OO-databases. 

Products I've used for developing:
    * pyramid_simpleform 
    * compass
    * Twitter Bootstrap for layout


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
sivuston painoarvo itsessään on jo hyvin suuri. Seuraavassa listaus vaatimuksista, jotka sivujen tulisi toteuttaa:

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
      niin testit kirjoitetaan ennen varsinaista toteutusta.
    - Ohjelmakoodia tulee refaktoroida kokoajan.
    - Epäselvältä vaikuttava ohjelmakoodi on kommentoitava selkeästi. 
    - Liika ohjelmakoodin opimointi ja "tuijottelu" jätettävä pois. Tähän sorrun itse hyvin usein ja se syö turhaa aikaa. Jossain vaiheessa
      ratkaisut on kuitenkin tehtävä, jotta päästään eteenpäin.
    - Asiakkaalle tulee näyttää "prototyypin" omaisesti sivuja mahdollisimman usein.


Välineet ja menetelmät
----------------------
Sivuston toteutukseen käytetään Pyramid-sovelluskehystä, joka käyttää ohjelmointikielenä Pythonia. Pyramid on hyvin minimaalinen sovelluskehys, joka
tarjoaa valmiita ratkaisuja usein toistuviin ongelmiin web-kehityksessä. Pyramidin tarkoitus on kuitenkin olla mahdollisimman helposti laannettevissa erilaisiin
käyttötarkoituksiin, joten se tarjoaa vain välttämättömät välineet web-sovelluksien toteutuksille. Pyramid ei ota kantaa mihinkään erityiseen tekniikkaan
millä web-sovellus tulisi toteuttaa. Tämä on jätetty ohjelmoijalle päätettäväksi. Yksinkertaisuudessaan Pyramidin päälle rakennetuissa sovelluksissa tulee löytää itse
sopivat Pyramid-laajennokset, jotka auttavat jonkun tietyn ongelman ratkaisussa. Pyramidia voi hyvin verrata "Ruby On Rails" -sovelluskehykseen, mutta se on tätäkin
paljon minimaalisempi. Pyramid soveltuu siis hyvin myös pienien sivustojen toteutuksessa, koska siinä ei ole mitään "ylimääräistä".

Työssä käytetään Pyramidin ja sen lisäosien lisäksi myös paljon muita erilaisia tekniikoita, jotka helpottavat suuresti sovelluskehitystä. Esimerkiksi ulkoasun toteutukseen
käytetään valmista CSS- ja javascript-kirjastoa nimeltä "Twitter Bootstrap". Bootstrap-kirjasto antaa helpotusta yleisesti käytettävien ulkoasu-komponenttejen toteutukseen.  Näistä hyvänä esimerkinä ovat erilaiset valikot ja painikkeet. Seuraavaksi listataan tärkeimmät tekniikat ja välineet, joita tässä työssä käytetään:

    ZODB (Zope Object Data Base)
        Työssä käytetään Zope-oliotietokantaa, jossa oliot tallennetaa kantaan juuri sellaisena, kun ne on ohjelmakoodiin määritelty. 
    Traversal
        Yksinkertaisuudessaan oliotietokannan sisältämää puuta käydään läpi samalla kuin osoiteriville syötetään jokin tietty polku. Esimerkiksi,
        jos olio tietokannassa kitarat-olio, joka sisältää "fender" -nimisen kitara-olion, löydetään fender polusta "/kitarat/fender". Kyseiseen
        osoitteeseen mentäessä saadaan vastauksena fender-olio, jolle yleensä on määritelty jokin näkymä sovelluksessa. Yksityiskohtaiseen
        selvitykseen ei kuitenkaan tässä raportissa tämän enempää oteta kantaa.
    Twitter Bootstrap
        Twitterin kehittäjien toteuttama avoimen lähdekoodin kirjasto, joka on tarkoitettu apuvälineeksi web-kehittäjille. Kirjasto sisältää yleisimmät
        web-sivustoilla käytetyt komponentit, kuten esimerkiksi painikkeet ja valikot. Samalla se tarjoaa apuja yksinkertaisen ulkoasun toteuttamiseen, 
        joka on mahdollisimman käyttäjäystävällinen.
    CoffeeScript
        Ohjelmointikieli, joka tekee Javascriptin kirjoittamisesta "helpompaa". Tarkoituksena kirjoittaa javascriptiä, joka on syntaksiltaan hyvin lähellä Pythonin ja
        Rubyn kaltaisia kieliä. CoffeeScriptillä kirjoitettu ohjelmakoodi generoidaan lopulta tavalliseksi Javascriptiksi, jota selaimet ymmärtävät.
    Less
        Less on CSS-tyylejen kirjoitukseen käytetty kehys, joka laajentaa tavallista CSS:ssää tuomalla tähän muuttujia, funktioita sekä muita ohjelmointikielistä tuttuja
        tekniikoita.
    ZCA (Zope Component Architecture)
        ZCA on sovelluskehys, joka tuo sovellukseen komponenttipohjaisen lähestymistavan. Komponenttipohjainen suunnittelu tuo erityisesti apuja massiivisten sovelluksien toteutukselle,
        mutta antaa myös paljon pienemmille sovelluksille. Hyvänä esimerkkinä on Javasta tutut rajapinnat, joita ei ole Python-kielessä itsessään valmiiksi. ZCA tuo esimerkiksi nämä
        mukanaan sovellukseen.
    MVC (Model-View-Controller)
        Sovellus-arkkitehtuuri, joka tuo sovellukselle tason, jonka mukaan komponentit tulisi jakaa kolmeen osaan: Malli, Näkymä ja Ohjain. Pyramid käyttää MVC-arkkitehtuuria, joissain
        määrin, mutta ei kuitenkaan toteuta tätä sellaisena kuin se on tarkoitettu. Tätä on käsitelty tarkemmin omassa Kandidaatintutkielmassani. Tämän työn kannalta tärkeintä on 
        huomata, että malleja toteuttamalla voidaan rakentaa koko sovelluksen runko. Mallejen ohjelmakoodit löytyvät "models.py" -moduulista.

        
Työ sisältää myös paljon muita erilaisia kehitystekniikoita, mutta nämä tekniikat ovat hyvin yksityiskohtaisia ohjelmistoteknisiä ratkaisuja, joten niiden tarkempaa
käsittelyä ei tässä raportissa toteuteta.


Sovelluksen rakenne
-------------------

Oliotietokannan ansiosta pystytään sovelluksen rakenne kuvaamaan selkeästi luokkakaaviona. Tämä siksi, koska sovellukseen luodut "mallit" kuvaavat sovelluksen rakennetta ja sen ylläpitämää
tietoa. Mallit pitävät siis yllä sovelluksen tilaa ja tallentuvat näin oliotietokantaan. Seuraavassa kuvassa on määritelty tämän työn luokkakaavio, joissa kaikki sovelluksen mallit on esitelty.

.. image:: https://github.com/tojuhaka/easyblog/raw/master/class_diagram.png


Ajankäyttö
----------
Ajankäytössä ei voida tarkkaan sanoa kuinka paljon aikaa meni mihinkin vaiheeseen, koska
erilaisia ongelmia/väärinkäsityksiä ilmeni niin asiakaspuolella kuin kehityspuolellakin. Välineet
olivat myös kehittäjälle tuntemattomia, joten niiden opetteluun meni myös aikaa. Testit kirjoitettiin aina ennen varsinaisen toteutuksen kirjoittamista. Testit olivat siis kokoajan mukana ominaisuuksien tekemisessä, joka huomataan ajan käytössä toteutuksessa. Testejen ylläpitoon meni myös oma aikansa, koska speksejen muuttuessa jouduttiin muuttamaan testejä. Testit kuitenkin maksoivat itsensä takaisin moninkertaisesti. Erityisesti tilanteissa, joissa ohjelmakoodia tai siihen liittyvää arkkitehtuuria muutettiin. Kokonaistuntimäärä pitää paikkansa, mutta eri osa-alueiden tarkat tuntimäärät saattavat vaihdella. Ne vastaavat kuitenkin painoarvoltaan todellisuutta, joten ajankäytöstä saa hyvän kuvan alla olevasta selvityksestä.

- Suunnittelu (28h)
    + Asiakkaan kanssa (8h)
    + Arkkitehtuuri (16h)
    + Välineet (4h)

- Välineiden opettelu (23h)
    + pyramid (15h)
    + twitter bootstrap (3h)
    + ZCA (2h)
    + Webfaction (julkaiseminen) (3h)

- Toteutus (140h)
    + ohjelmointi(80h)
    + testikoodit(60h)

- Ongelmatilanteet (30h)
    + ominaisuuksien toteutus, joita ei tarvinnutkaan (speksejen epätarkkuus)
    + olemassa olevien ominaisuuksien toteutus "väärin" (speksejen epätarkkuus)
    + arkkitehtuurin muokkaus lennosta

- Muu (20h)
    + Lopputestaus (10h)
    + koulutus (5h)
    + ylläpito (5h)




Mitä olisi pitänyt tehdä toisin
-------------------------------
ZCA:ta olisi pitänyt käyttää enemmän jo alusta asti. Tämän huomasi erilaisista arkkitehtuurin
liittyvistä ongelmista, jotka tulivat vastaan sovelluksen kehityksen aikana. Tässä vaiheessa tuli tehtyä turhaa työtä, joka johti hieman suurempaan arkkitehtuurin refaktorointiin. 

Komponentit olisivat voineet olla vielä modulaarisempia. Tätä kuitenkin rajoitti valitut välineet, joten suoraan ei voida sanoa millä tavalla ohjelmakoodi olisi pitänyt toteuttaa toisin. Sama ongelma esiintyi templatejen kirjoittamisessa, jossa jouduttiin usein toistaa samankaltaista pohjaa monessa eri templatessa. Mikään template ei kuitenkaan ollut identtinen, vaan sisälsi osaksi kontekstiriippuvuutta, joten suoraa toisen templaten käyttöä ei voitu toteuttaa. Suurin osa toistosta saatiin kuitenkin kuriin yhden base.pt -templaten avulla. 

Aikaa vei suuresti speksejen epätarkkuus, joka johti ylimääräisten ominaisuuksien turhaan toteutukseen sekä haluttujen ominaisuuksien vääränlaiseen toteutukseen. Tässä olisi pitänyt olla tarkempi alusta asti. 

- Enemmän ZCA:n käyttöä!!
- Modulaarisempia komponentteja!!
- Templateissa koodin toistoa, voisiko jotenkin abstrahoida paremmin?
- Pyytää asiakkaalta tarkemmat speksit ennen vaersinaisen toteuttamisen aloittamista!
- Käännöksien huomioon ottaminen jo siinä vaiheessa kun templateja aletaan tekemään
- Enemmän yhtenäisyyttä ohjelmakoodiin, esim. samojen asioiden nimeämiset välillä erilailla
. Miten saada templaten toisto järkeväksi? Onko mahdollista?

Mikä oli hankalaa, mikä taas suoraviivaista?
--------------------------------------------




