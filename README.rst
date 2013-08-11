EasyBlog
========

:Author: Toni Haka-Risku
:Version: 0.1-dev

Introduction
------------
EasyBlog is a webpage created with pyramid. Main goal is to test different features of pyramid. During development I was asked to create a webpage that contains Authorization-policy, user-management, blogging and news. So I let this project to fulfill those requirements. After a little bit of refactoring it's not a test-project anymore but a webpage for Saapas RY.

EasyBlog uses ZODB and traversal. Main reason for that is my experience from Plone and Zope. And yes, I like OO-databases. 

Products I've used for developing:
- pyramid_simpleform 
- compass
- Twitter Bootstrap for layout

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

Asiakaalla ei suoraan ollut selkeä kuvaa mitä sivun tulisi heille tarjota. Yllä esitellyistä
vaatimuksista eivät kaikki tulleet suoraan projektin alussa, vaan ne lisääntyivät
pikkuhiljaa projektin edetessä.


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

Oliotietokannan ansiosta pystytään sovelluksen rakenne kuvaamaan selkeästi luokkakaaviona. Tämä siksi, koska sovellukseen luodut mallit (model) kuvaavat sovelluksen rakennetta ja sen ylläpitämää
tietoa. Mallit pitävät siis yllä sovelluksen tilaa ja tallentuvat näin oliotietokantaan. Luokkien rakenne toimii siten, että tietyt luokat toimivat säiliöinä ja muut tavallisina sisältöinä/objekteina. Oliotietokannassa hierarkia on tallennettu puuna, jossa on vanhempi- sekä lapsielementtjä.
Esimerkiksi yksi blogikirjoitus kuuluu Blog -oliolle, joka toimii säiliönä jokaiselle blogikirjoitus-oliolle. Oliotietokannassa on aina juuri (root), josta lähdetään sanastoperiaatteella käymään
puuta läpi. Jos menemme vaikka sivustolla "/blogs/blog-1/kirjoitus-1", menemme myös tietokannassa kyseiseen kohtaan. Jos tietokannasta löytyy kyseinen blogikirjoitus-olio, tarjotaan olion sisältö halutussa
muodossa selaimelle. Tässä tapauksessa HTML-sivuna. Tätä toiminnallisuutta kutsutaan "Traversal" -nimellä. Vaikka kutsumme alla olevaa kaaviota luokkakaavioksi, ei se kuvaa sovelluksen kaikkien luokkien ja suhdetta. Useita
"epäolennaisia" luokkia on jätetty pois kaavion selkeyttämiseksi. Samalla notaatio on hyvin pelkistetty. Kaaviossa siis esitellään ainoastaan oliotietokannassa mallina esiintyvät luokat.

.. image:: https://github.com/tojuhaka/easyblog/raw/master/class_diagram.png

Kaaviossa kulmasulkeet kuvaavat perittyä "abstraktia" luokkaa. Pythonissa ei ole abstraktin luokan määritelmää kuten esimerkiski Javassa, mutta tätä ajattelutapaa voidaan hyödyntää. Content ja Container
luokat pitävät huolen siitä, että ne tallentuvat oliotietokantaan eivätkä katoa sieltä requestin aikana. Nuolet kuvaavat lapsisuhdetta, jossa nuoli osoittaa aikuisesta lapsielementtiin. Esimerkisi Main-luokka 
sisältää Blogs-luokan, joka taas sisältää monta Blog-luokkaa. Tähti(*) kuvaa sitä, että luokan instansseja voi olla useita. Jos tähteä ei ole on luokasta vain yksi instanssi. 

Testilähtöinen kehitys
----------------------
Sovellus toteutettiin käyttäen testilähtöistä kehitystä. Tämä toteutettiin siten, että testit kirjoitettiin ennen itse varsinaisen ohjelmakoodin kirjoittamista. Täydelliseen testilähtöiseen 
toteutukseen ei kuitenkaan päästy, koska välineiden opettelussa täytyi kokeilla erilaisia asioita ja tämä sujui nopeammin, kun testit kirjoitettiin jälkikäteen. Suurin osa koodista on kuitenkin 
toteutettu testilähtöisesti. Testejen kirjoittamiseen käytettiin Pyramidin testikirjastoa sekä Webtest-kirjastoa. Kyseinen kirjasto on tarkoitettu erityisesti funktionaalisia testejä varten.:w

Projektin alussa kirjoitettiin jonkin verran yksikkötestejä, mutta ne osoittautuivat omasta mielestäni hyvin aikaa vieviksi. Yksikkötestit siis jätettiin suurimmalta osalta pois ja siirryttiin 
käyttämään funktionaalisia testejä sekä integraatiotestejä. Funktionaaliset testit ovat korkeamman tason testejä, jotka testaavat jonkun isomman kokonaisuuden. Yksikkötestit testaavat usein jonkun tietyn algoritmin toimivuutta, mutta 
funktionaaliset testit taas testaavat esimerkiksi napin painallusta sivustolla. Tätä varten funktionaalisissa testeissä "rakennetaan" aina ympäristö testaamista varten. Tässä tilanteessa siis kyseinen sivusto. 
Funktionaaliset testit osoittautuivat hyvin mielekkäiksi kirjoittaa. Ne myös kävivät suuren osan koodia kerralla läpi sekä vastasivat suoraan asiakkaan vaatimuksia. Samalla ne kuvasivat sovelluksen yleistä
toiminnallisuutta. Testit pystyttiin myös usein kuvaamaan suoraan asiakkaiden tarpeiden pohjalta ja ne helpottivat samalla seuraamaan projektin etenemistä ominaisuuksian näkökulmasta. 

Funktionaalisissa testeissä oli myös seassa integraatiotestejä. Näiden kahden raja oli sovelluksen kehityksen aikana häilyvä, koska testeissä käytettiin kumpaakin sekaisin. Näitä ei siis jaoteltu erikseen, koska päämääränä oli testauslähtöinen kehitys,
jossa kantaa ei niinkään otettu siihen onko kyseessä yksikkötestejä, funktionaalisia testejeä vai integraatiotestejä. Kuitenkin jälkiviisaana voisi sanoa, että testejä olisi voinut jaotella myös integraatiotesteihin. Tästä asiasta en Kuitenkaan välittänyt
kehityksen aikana, vaan esittelin kummatkin "funktionaalisina testeinä". 

Testauksessa oli myös vivahteita ATDD:n (Acceptance Test Driven Development) suuntaan, mutta todellisuudessa tätä testaus ei ollut. ATDD:hen kuuluu yleensä se, että asiakas määrittelee jollain tasolla ominaisuuksia testeinä. Tähän ei kuitenkaan missään vaiheessa
päästy, vaan testit kirjoitettiin aina täysin kehittäjän toimesta. Asiakas ei myöskään ollut täysin varma mitä haluamistaan ominaisuuksista, joten tämän puolesta ATDD:n oikeaoppinen käyttäminen olisi tullut vastaan. Testejä kirjoitettin myös aina yksi kerrallaan ja 
tämän jälkeen kirjoitettiin toiminnallisuus, jotta testi menisi läpi. ATDD:ssä yleensä kirjoitetaan kerralla useita testejä, jotka käyvät läpi sovelluksen toimintaa. Tämän jälkeen ohjelmakoodi kirjoitetaan siten, että kaikki testit menevät läpi. 
Tässä projektissa testit kirjoitettiin kuitenkin usein kehittäjän toimesta siten, että ne vastaavat asiakkaan kanssa sovittuja toiminnallisuuksia, joten tältä osin päästiin lähelle ATDD:tä.

Vaikka testit helpottivat suuresti projektin ohjelmakoodin hallintaa, osoittautuivat ne myös varsin työllistäviksin. Erityisesti tämä tuli esiin siinä vaiheessa, kun projektin hallinnan osalta oltiin liian
ketteriä ja ennakoitiin asiakkaan vaatimuksia. Liika ketteryys johti välillä ominaisuuksien tekemiseen, joita ei lopulta tarvittukkaan. Tässä vaiheessa testit työllistivät runsaasti, koska
erilaisten ominaisuuksien postuessa tai muuttuessa jouduttiin samalla päivittämään testit ajantasalle  Tähän oli kuitenkin usein syynä liika ennakointi, sekä asiakkaan vaatimusten epämääräisyys, ei siis 
ohjelmointitekniikka itsessään.

Testilähtöinen kehitys osoittautui tietenkin työlääksi itse koodia kirjottaessa, mutta todellisuudessa se maksoi itsensä takaisin moneen kertaan kun sovellusta refaktoroitiin. Kattavat testit pitivät
huolen siitä, että tehdyt virheet tulivat esiin välittömästi koodia muuttaessa. 

Tuotantoon vieminen
-------------------
Sovelluksen kehitys toteutettiin ajamalla sivustoa omalla koneella ja samalla viemällä erilaisia prototyyppejä kehitysversiosta tuotantoon näytettäväksi. Tuotantoa varten käytettiin `WebFactionin
<http://www.webfaction.com/>`_ tarjoamaa hostauspalvelua. Syy tähän oli erittäin selkeä ja hyvä tuki Pyramidille. Sovelluksesta tehtiin yksinkertainen Python-paketti, joka asennettiin erilliseen
virtuaaliseen Python-ympäristöön palvelimelle. Tuotantoon vietiin monesti erilaisia prototyyyppi versioita asiakkaalle näyettäväksi ennen varsinaista julkaisua.

Sivustolle testiin myös yksinkertainen käyettävyyskoe, jossa kaikki sivuston pääkäyttäjät kokeilivat sivustoa ilman ohjeita. Kokeessa seurattiin kuinka nopeasti käyttäjät omaksuvat sisällön luomisen
sivustolla. Samalla kokeen aikana käyttäjät koulutettiin käyttämään sivustoa. Tiivistettynä käyttäjät omaksuivat sivun käyttämisen erittäin nopeasti ilman suurempia käytettävyysongelmia.


Ajankäyttö
----------
Ajankäytössä ei voida tarkkaan sanoa kuinka paljon aikaa meni mihinkin vaiheeseen, koska
erilaisia ongelmia/väärinkäsityksiä ilmeni niin asiakaspuolella kuin kehityspuolellakin. Välineet
olivat myös kehittäjälle tuntemattomia, joten niiden opetteluun meni myös aikaa. Testit kirjoitettiin aina ennen varsinaisen toteutuksen kirjoittamista. 
Testit olivat siis kokoajan mukana ominaisuuksien tekemisessä, joka huomataan ajan käytössä toteutuksessa. Testejen ylläpitoon meni myös oma aikansa, koska 
speksejen muuttuessa jouduttiin muuttamaan testejä. Testit kuitenkin maksoivat itsensä takaisin moninkertaisesti. Erityisesti tilanteissa, joissa ohjelmakoodia tai 
siihen liittyvää arkkitehtuuria muutettiin. Kokonaistuntimäärä pitää paikkansa, mutta eri osa-alueiden tarkat tuntimäärät saattavat vaihdella. Ne vastaavat kuitenkin 
painoarvoltaan todellisuutta, joten ajankäytöstä saa hyvän kuvan alla olevasta selvityksestä.

- Suunnittelu (28h)
    + Asiakkaan kanssa (8h)
    + Arkkitehtuuri (16h)
    + Välineet (4h)

- Välineiden opettelu (23h)
    + pyramid (15h)
    + twitter bootstrap (3h)
    + ZCA (2h)
    + Webfaction (julkaiseminen) (3h)

- Toteutus (120h)
    + ohjelmointi(60h)
    + testikoodit(40h)
    + käyttäjäkokemuksen ja ulkoasun viilaaminen(20h)

- Ongelmatilanteet (sisältyy kaikkeen) (30h)
    + ominaisuuksien toteutus, joita ei tarvinnutkaan (speksejen epätarkkuus)
    + olemassa olevien ominaisuuksien toteutus "väärin" (speksejen epätarkkuus)
    + arkkitehtuurin muokkaus lennosta

- Muu (20h)
    + Lopputestaus (10h)
    + koulutus (5h)
    + ylläpito (5h)

Tavoitteiden toteutuminen
-------------------------

Kehittäjä
~~~~~~~~~

Varsinaiseen suunnitteluun ei käytetty aikaa juurikaan ja näin oli tarkoituskin. Erilaisia ominaisuuksia 
yleensä kirjoitettiin suoraan, koska ne olivat yleensä melko suoraviivaisia ja selkeitä. Jos suunnitelua 
olisi ollut enemmän, uskoisin että projektin kehitys olisi hidastunut huomattavasti, koska projektilla
ei ollut selkeitä vaatimuksia alussa. Vaatimukset lisääntyivät siis projektin aikana. Asiakkaalle oli muutenkin
tärkeää, että sivustoa demottiin aina välillä, jotta heille tulisi selkämpi kuva siitä mitä he haluavat.

Testejen osalta onnistuttiin varsin mallikkaasti. Testit kulkivat mukana koko projektin toteutuksen ajan ja projektin lopussa
ne kattasivat lähes koko ohjelmakoodin. Kuitenkaan 100% testikattavuuten ei aivan päästy. Testit maksoivat itsensä takaisin 
erityisesti kun ohjelmakoodia lähdettiin refaktoroimaan ja muuttamaan. 

Refaktorointia tapahtui myös koko projektin ajan, mutta tämä koitui välillä hieman ongelmaksikin. Liiallinen "täydellisyyteen" pyrkiminen
toi jonkin verran ylimääräisiä tunteja, joilta olisi voinut välttyä. Ei voida kuitenkaan sanoa, että nämä tunnit olisi ollut hukkaanheitettyä
aikaa. Sorruin muutamaan otteeseen kuitenkin liialliseen ohjelmakoodin refaktorointiin. Sain kuitenkin omalta osaltani vähennettyä tätä verrattaen edellisiin projekteihini, 
joten tässä tapahtui jonkinlaista kehitystä. Ohjelmakoodin dokumentointiin ja kommentointiin olisi voinut panostaa enemmän. Tätäkin on
vaikea mitata, koska tällä hetkellä koodia on lukenut oikeastaan itse sen tekijä, eikä palautetta koodin selkeydestä ja kommentoinnista
ole saatu ulkopuoliselta henkilöltä. Tavoitteena oli kuitenkin kommentoida epäselvät kohdat, joten uskon että tavoitteeseen päästiin. 

Asiakkaalle olisi voinut näyttää vielä enemmän erilaisia prototyyppejä. Sivustoa demottiin asiakkaalle muutamaan otteeseen projektin aikana, mutta tämä ei oikeastaan
koskaan lähtenyt itse asiakkaan suunnasta vaan omasta toimestani. Olisin odottanut asiakkaalta enemmän painostusta tämän suhteen, koska projektin onnistumisen kannalta
on tärkeää, että asiakas on kiinnostunut mihin suuntaan projekti etenee. Prototyyppejen näyttäminen osoittautui erittäin toimivaksi, koska niiden kautta asiakkaalta
saatiin aina selkeimpiä vaatimuksia. Samalla nähtiin myös suoraan, jos jokin ominaisuus ei asiakasta miellyttänyt.

Asiakas
~~~~~~~

Asiakkaan vaatimat ominaisuudet toteutettiin, niinkuin oli ajateltukkin lukuunottamatta etusivun informativiisuutta. Tarkempi info siirrettiin lopulta about-sivulle. Se millä tavalla ominaisuudet
toteutettiin muuttui useita kertoja projektin aikana, mutta tähän ei oltu alunperin otettukkaan sen enempää kantaa.

Asiakkaille tehdyssä koulutuksessa sivut osoittautuivat hyvin yksinkertaisiksi käyttää. Koulutuksessa toteutettiin pienimuotoinen koe, jossa puolelle porukasta
jaettiin ohjeet sivuston käyttämiseen ja toiselle puolelle ei jaettu mitään ohjeita. Tämän jälkeen jokainen toteutti yksinkertaisia sisällönluomistehtäviä. Jokaisen henkilön
kohdalla otettiin aikaa, kuinka kauan tehtävien tekoon meni. Tuloksista nähtiin, että aikaerot eivät olleet mitenkään suuria ryhmien välillä. Itseasiassa kahdella ohjeellisen ryhmän
jäsenellä meni enemmän aikaa toteuttaa tehtävät (ohjeiden lukemiseen meni turhaa aikaa). Sivuston koko käytettävyys perustui siihen, että oikeasta yläkulmasta löytyi "Actions" -nappi,
jonka tarjoamat toiminnot muuttuivat sivukohtaisesti. Koehenkilöt omaksuivat tämän toiminnallisuuden hyvin nopeasti. Eniten aikaa meni kyseisen napin löytämiseen.

Tietoturvan puolesta luotettiin paljon Pyramidiin valmiiksi (ks. http://pyramid.readthedocs.org/en/latest/narr/security.html). Kuitenkin autentikointi jouduttiin
toteuttamaan itse, mutta tämäkin toteutettiin "oikeaoppisesti" käyttämällä Pyramidissa tarkoitettuja autentikaation toteuttamiselle. Tietokantoihin kohdistettuja hyökkäyksiä 
ei juurikaan ole mahdollista tehdä, koska kyseessä on oliotietokanta (esimerkiksi injektiot on tässä jo suljettu pois). Ainut tietoturvaongelma on tällä hetkellä, se että
lähdekoodit näkyvät julkisesti githubissa (esimerkiksi suola näkyy avoimesti tällä hetkellä, mikä ei ole hyvä). Tämän ei pitäisi kuitenkaan tuottaa sivustolle haavoittuvuutta.



Mitä olisi pitänyt tehdä toisin?
-------------------------------
ZCA:ta olisi pitänyt käyttää enemmän jo alusta asti. Tämän huomasi erilaisista arkkitehtuurin
liittyvistä ongelmista, jotka tulivat vastaan sovelluksen kehityksen aikana. Tässä vaiheessa tuli tehtyä turhaa työtä, joka johti hieman suurempaan arkkitehtuurin refaktorointiin. 

Komponentit olisivat voineet olla vielä modulaarisempia. Tätä kuitenkin rajoitti valitut välineet, joten suoraan ei voida sanoa millä tavalla ohjelmakoodi olisi pitänyt toteuttaa toisin. Sama ongelma esiintyi templatejen kirjoittamisessa, jossa jouduttiin usein toistaa samankaltaista pohjaa monessa eri templatessa. Mikään template ei kuitenkaan ollut identtinen, vaan sisälsi osaksi kontekstiriippuvuutta, joten suoraa toisen templaten käyttöä ei voitu toteuttaa. Suurin osa toistosta saatiin kuitenkin kuriin yhden base.pt -templaten avulla. 

Aikaa vei suuresti speksejen epätarkkuus, joka johti ylimääräisten ominaisuuksien turhaan toteutukseen sekä haluttujen ominaisuuksien vääränlaiseen toteutukseen. Tässä olisi pitänyt olla tarkempi alusta asti. Samalla olisi tullut ottaa huomioon käännöksien tarpeellisuus jo kehityksen alussa. Tämä aiheutti myös hieman lisätyötä. Testilähtöinen kehitys kuitenkin piti huolen, että sovellukksen refaktoroinnin aikana
saatiin virheet esiin välittömästi testejä ajettaessa. Tällä säästettiin aikaa huomattavasti.

Erilaisten sovelluksen osien nimeämiskäytäntöjä olisi voinut miettiä tarkemmin. Esimerkiksi joissain tilanteissa sama asia nimettiin kahdella eritavalla. 

Projekti pähkinänkuoressa
-------------------------
Ongelmia tuotti projekin hallinnollinen puoli, jossa asiakkaan speksejen kanssa olisi voinut
olla tiukempi. Tästä koitui paljon lisätyötä, jolta olisi hyvin voinut välttyä. Asiakas olisi voinut myös olla paljon tietoisempi siitä mitä hän haluaa. Prototyyppejen esittely kuitenkin auttoi
paljon selkeyttämään asiakkaan vaatimuksia. Testilähtöinen kehitys osoittautui erittäin tehokkaaksi, mutta samalla myös työlääksi. Silti voi sanoa, että kattavat testit tekivät sovelluksen kehittämisestä nopeaa ja varmaa. Sovellukseen tehtyjen muutoksien tuottamat bugit löytyivät välittömästi testejen avulla, joka taas puolestaan nopeutti kehitystä huomattavasti.

Kehityksen aikana tuli myös huomattua, kuinka suuri osa ajasta menee kaikkeen muuhun kuin ohjelmointiin. Suunnittelu, välineiden opettelu sekä koulutus veivät oman aikansa ohjelmoinnin ohella. Vaikka sivusto ei ollut lopputoteutukseltaan kovin laaja, meni sen tekemiseen paljon odotettua enemmän aikaa. Erityisesti käyttökokemuksen viilaaminen, muutoksiin vastaaminen ja sovelluksen arkkitehtuurin hyvä toteutus veivät runsaasti aikaa. Se, että ohjelmakoodista haluaa tehdä nättiä, tuo erittäin paljon lisätyötä. Vähemmällä olisi luultavasti päässyt, jos ohjelmakoodin olisi jättänyt enemmän "sotkuiseksi". Tulevaisuuden kannalta tämä ei tosin olisi ollut kovinkaan järkevää.

Kaiken kaikkiaan projekti oli hyvin opettavainen ja antoi erittäin paljon lisää kokemusta sovelluskehityksestä ja siihen liittyvistä ongelmista. 





