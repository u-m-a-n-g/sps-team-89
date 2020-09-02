# COVID-19 Visualizer and Query Bot
The objective of our project is to provide the user with a platform which has general information related to the current pandemic in an easy to understand way. Our platform inputs free form covid-19 related queries to extract relevant information to do the following:
- Analyse the trends of various statistics related to covid-19 (for example: active cases, deaths, total cases etc.) by plotting them graphically
- Answer general queries of the user (for examples, precautions, symptoms etc.) through a chatbot 

### Sample queries:
- Visualizer:
    - Plot active cases in Spain, italy and iran
    - Show the active  cases in China and UP from 1st jan to august 15
    - Plot the deaths in India and Maharashtra in last 3 months
- Query Bot:
    - Does it spread through air?
    - Why is it called a novel virus?
    - Is it safe to go to school?

#### Links:
- Website: https://summer20-sps-89.el.r.appspot.com/
- Presentation: https://docs.google.com/presentation/d/1USZ-WYaxTATOrRayZ6dgOQ1F3oRFMp-CE9KtjNPaq1I/present
- Design doc: https://docs.google.com/document/d/1rJb8QwJKcqsX8_vT7gMiABHvp8EPyKCTlS7svkmbVrY/

#### Running

Before starting the program, make sure to set up google authentication here: https://cloud.google.com/docs/authentication/getting-started  
After the `GOOGLE_APPLICATION_CREDENTIALS` variable is set, start the program by running the following from `src` folder.

```sh
$ pip3 install -r requirements.txt 
$ flask main.py
```
