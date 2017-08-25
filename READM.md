# Logical Markup Language


The logml is a markup language for logical programming. The goal of the language
is the possibility to organize facts and rules in a more object oriented, and, semantic way.

The language is based in XML and inspired in AIML (Artificial Intelligence Markup Language, see <http://www.alicebot.org/aiml.html>) and Prolog language (<http://www.swi-prolog.org/>).

The basic structure of logml file is:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<logml>
    <axiom>
        <head>
            <pred class="">
                <li></li>
            </pred>
        </head>
        <body>
            <pred class="">
                <li></li>
            </pred>
        </body>
    </axiom>
</logml>
```

Where `<logml></logml>` delimite the root of program, between `<axiom></axiom>` is written the rules, `<head></head>` define the head and `<body></body>` the body of rule. Axiom without body is a fact. The command `<pred class=""></pred>` define a predicate, and the `class` is the name of predicate. It is possible to have more than one group of constants or variables, using `<li></li>`.


## Basic Example

Consider the fact that all human is mortal. Now we create a facts contain a list of humans.

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<logml>
    <axiom>
        <head>
            <!--Facts -->
            <pred class="humam">
                <!--List of humans -->
                <li>sócrates</li>
                <li>maria</li>
                <li>josé</li>
                <li>marcelina</li>
                <li>joarez</li>
            </pred>
        </head>
    </axiom>
    <axiom>
        <head>
            <pred class="mortal">
                <li>x</li>
            </pred>
        </head>
        <body>
            <pred class="humam">
                <li>x</li>
            </pred>
        </body>
    </axiom>
</logml>
```


In the first axiom we define a list of humans. In the second axiom we define the rule `mortal(X) <--- human(X)`.
Note that, in rules, the values inside `<li></li>` is assumed as variable and not constants.

Also in the body is accept only predicates that was defined in some moment in a head of an axiom.

## Generating a prolog file.

It is possible to convert a logm file in prolog (pl) file.

```bash
python translater.py teste.logml teste.pl
```

The output will be:

```pl
humam(sócrates).
humam(maria).
humam(josé).
humam(marcelina).
humam(joarez).

mortal(X):- humam(X).
```

In this way, we keep the compatibility between logml and Prolog.


## TO DO:

Implement a python logical search using the logml file.
