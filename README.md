
<h1> preplyteacherbot </h1>
<br>
<p> are you too lazy to reply to student messages on preply? this bot will answer every chat with ai so you can be lazy asl </p>
<h1> what you need:</h1>
<li> install pytesseract as an exe to default path </li>
<li>scale windows to 125% </li> 
<li> create a google gemini api key </li>
<li> if you want to start and stop bot via telegram, create tg bot with botfather and a tg token </li>


---

**first clone the repo**

```bash
git clone https://github.com/JXR0N/Preply-Teacher-Bot.git
```

**then get all requirements**

```bash
pip install -r requirements.txt
```

then you have to create a gemini api key and put it into the .env file.
if you want remote control via telegram, you can create a tg bot with botfather (optional)
in src/prompt change the teachers prompt to the one you desire



**now start the script**
```bash
py running.py
```

**or with the telegram-addon**

```bash
py tgbot.py
```
