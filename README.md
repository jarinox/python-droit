# python-droit
Droit is a simple library for creating bots.  

## At a glance
```
TEXT!my:TEXT!name:TEXT!is:INP*name!->TEXT!Hi :VAR!inp.name
```
A bot using the above Droit Database Script will create the following output:
```
My name is John -> Hi John
My name is Ellie -> Hi Ellie
```

Droit Database Script comes with many possible condition-blocks like "TEXT" (a word has to be included in the text), "INP" (reads a word or several words) and "SIMT*80" (a sentence similar to up to in this case 80 percent has to be given). They make it easy to create complex question-to-answer rules. You can extend python-droit by easily writing your own condition-blocks (= plugins).

## Features
- Advanced definition of question-to-answer rules using Droit Database Script
- Multiple users supported
- Integrated history functionallity to understand references to previous inputs
- Extendable: create your own sub-rules ("plugins")

## Learn
- [Wiki > Introduction to Droit v1.1](https://github.com/jarinox/python-droit/wiki/Introduction-to-Droit-v1.1)
- [Documentation](https://github.com/jarinox/python-droit/blob/master/docs/droit.md)
- [Examples](https://github.com/jarinox/python-droit/blob/master/sample/)

## Installation
Easy installation using pip:
```
pip install droit
```
Alternatively you can clone this repository and install it to get the most recent version of `droit`:
```
git clone https://github.com/jarinox/python-droit
cd python-droit
pip install .
```

## License
This library is published under the terms of the GNU LESSER GENERAL PUBLIC LICENSE. Please see LICENSE for more information.  
Copyright 2019-2021 Jakob Stolze
