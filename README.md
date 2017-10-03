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


## Define Dynamic facts

For a real time analysis it is necessary to have a way to update a given fact.

Considering a robot that will be cross a road. In this case, the decision must take considering the traffic light in a given moment. So a current fact is the traffic light color in this moment. A decision rule to cross the road can be written as:
```xml
<?xml version="1.0" encoding="UTF-8" ?>
    <axiom>
        <head>
        <pred class="traffic_light" >
            <meta>The #TRAFFIC LIGHT# is *</meta>
            <li type="dynamic">current</li>
        </pred>
        <pred class="collor">
            <meta>* if #collor# is *</meta>
            <li>stop,red</li>
            <li>atention,yellow</li>
            <li>cross,green</li>
        </pred>
        </head>
    </axiom>
    <axiom>
        <head>
            <pred class="cross_road">
                <meta> #CROSS ROAD#  * when *</meta>
                <li>x,y</li>
            </pred>
        </head>
        <body>
            <pred class="collor">
                <li>x,y</li>
            </pred>
            <pred class="traffic_light">
                <li>y</li>
            </pred>
        </body>
    </axiom>
</logml>
```

In this case, it is necessary to pass a object to inference machine that will be update the fact.

For example,

```python
from inferencemachine import InferenceMachine
from myconnector import Connector

OBJ = InferenceMachine("crossroad.logml")
OBJ.set_dynamic_fact_interface("traffic_light", Connector())
```


where ```Connector``` must have the methods ```set_args``` and ```gets_args```. The ```gets_args``` will be used to update the fact.

The following is an example of ```Connector```

```python
from random import choice

from numpy import array


class Connector(object):
    """
    Dynamic update of a fact
    """

    def __init__(self):
        self.pred_args = None

    def set_args(self, args):
        """
        Set the args of Dynamic facts
        """
        self.pred_args = args

    def gets_args(self):
        """
        Return the new args of a fact.
        """
        tmp = []
        for i in self.pred_args:
            tmp2 = []
            for _ in i:
                tmp2.append(choice(["red", "yellow", "green"]))
            tmp.append(tmp2)

        return array(tmp)
```


## Rules and Facts in JSON format

It is possible to write the knowledge in the json format. Below it is a example of valide JSON file for the sample of cross road case.

```json
{
    "logml": {
        "axiom": [
            {
                "head": {
                    "pred": [
                        {
                            "@class": "traffic_light",
                            "li": {
                                "#text": "current",
                                "@type": "dynamic"
                            },
                            "meta": "The #TRAFFIC LIGHT# is *"
                        },
                        {
                            "@class": "collor",
                            "li": [
                                "stop,red",
                                "atention,yellow",
                                "cross,green"
                            ],
                            "meta": "* if #collor# is *"
                        }
                    ]
                }
            },
            {
                "body": {
                    "pred": [
                        {
                            "@class": "collor",
                            "li": "x,y"
                        },
                        {
                            "@class": "traffic_light",
                            "li": "y"
                        }
                    ]
                },
                "head": {
                    "pred": {
                        "@class": "cross_road",
                        "li": "x,y",
                        "meta": "#CROSS ROAD#  * when *"
                    }
                }
            }
        ]
    }
}
```

## Knowledge Graph

Supose that we want to prove that some one is a criminal. In our sample, we assume that a person produce a weapon, and, if this person is american and a enemy nation has this weapon, the person committed a crime.

The logml representing fatcs and rules of the crime is:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<logml>
    <axiom>
        <head>
            <pred class="american">
                <li>west</li>
                <li>jon</li>
            </pred>
            <pred class="nation">
                <li>nono</li>
                <li>xoxo</li>
            </pred>
            <pred class="enemy">
                <li>nono,america</li>
                <li>xoxo,america</li>
            </pred>
            <pred class="missile">
                <li>m1</li>
                <li>m2</li>
            </pred>
            <pred class="weapon">
                <li>m1</li>
                <li>m2</li>
                <li>hk</li>
            </pred>
            <pred class="owns">
                <li>nono,m1</li>
                <li>xoxo,m2</li>
            </pred>
            <pred class="produce">
                <li>west,m1</li>
                <li>jon,hk</li>
            </pred>
        </head>
    </axiom>
    <axiom>
        <head>
            <pred class="sells">
                <li>x,y,z</li>
            </pred>
        </head>
        <body>
            <pred class="produce">
                <li>x,y</li>
            </pred>
            <pred class="weapon">
                <li>y</li>
            </pred>
            <pred class="owns">
                <li>z,y</li>
            </pred>
        </body>
    </axiom>
    <axiom>
        <head>
            <pred class="criminal">
                <li>x</li>
            </pred>
        </head>
        <body>
            <pred class="american">
                <li>x</li>
            </pred>
            <pred class="missile">
                <li>y</li>
            </pred>
            <pred class="enemy">
                <li>z,america</li>
            </pred>
            <pred class="sells">
                <li>x,y,z</li>
            </pred>
        </body>
    </axiom>
</logml>
```


The following python programming query our database to prove who committed a crime:

```python

from logml.inferencemachine import InferenceMachine, plotTree

OBJ = InferenceMachine("./database/criminal.logml")
print(OBJ.question("criminal"))
plotTree(OBJ.graph)
```

The ```plotTree``` function generates a knowledge graph, representing the proof process:

![alt text](imgs/criminal.jpg?raw=true "Title")

Note that, to be criminal a person must be american, the nation must be enemy. Also, the person must have sold a missile to enemy.

For this rules and facts, the answer is ```[west]```
