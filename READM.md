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
                tmp2.append(choice(["vermelho", "verde", "amarelo"]))
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
