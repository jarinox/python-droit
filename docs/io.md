# Documentation - droit.io
Your can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).


## Class
- **DroitIO**()

### Class documentation
#### DroitIO()
Contains functions to output an answer or ask for an input. Plugins should always use these functions to get an input or put an output because depending on it's configuration it uses the console, a graphical userinterface or Text-To-Speech and Speech-Recognition

**Functions**

- output(text) - output some text
- binaryQuestion(question) - output a question and ask for Yes or No as an answer
- input(question) - await an input on a given question
- activateModule(name) - activates another output-module