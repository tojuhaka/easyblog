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
- pyramid_simpleform 
- compass

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


