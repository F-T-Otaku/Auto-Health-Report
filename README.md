# Auto-Health-Report (MASTER)
Automatically complete SUES daily health report.

***CAUTION: This repo is only for learning purposes, DO NOT use this repo for real health status reports. The author(s) will not be responsible if anything bad happens.***

***In the master vision, serverchan and telegram bot is required options.If you don't need both of these, you can build your own vision by change report.yml and auto-do.py.If you don't know how to do it, please use the main branch vision***

## Attention

1. Please edit your own cron table in report.yml.
2. Action's cron table runs in ***UTC***.

### How to create your own cron table

1. Open the xxx.yml fill. (Normally is "/.github/workflows/report.yml")
2. Change this to any time you want:
```
  schedule:
    - cron: "15 23 * * *" 
    - cron: "25 5 * * *" 
```
3. `cron: "25 5 * * *" ` means it runs at 05:25 ***UTC*** every day.(= 13:25 in China)

   1. *P.S. UTC is eight hours later than CST.*
   2. *P.P.S. CST – China Standard Time.*
   ~~3. *P.P.P.S. To ensure the report is successful, please set more than 4 times.*~~
   3. *Because this version has fail feedback, you can manually rerun the workflow, it's no need to run the job more than twice a day.*

## How to use - Two normal report ways and one fix missing way

### Use Github Actions (Recommend)

#### In this mode, you can receive message through ServerChan(on WeChat) and telegram bot

#### And it will automatically report twice a day 

- ~~Fork my repo. (Give me a star if you like this. lol)~~
1. Use my repo template and create your own repo.
2. Open your own repo and choose `Settings`.
3. In the left sidebar, click `Secrets`.
4. Click `New repository secret`.
5. Type `NUM` and `PWD` for your secret in the Name input box and enter the Value for your secret.
6. Configure your ServerChan and telegrambot by reading the usage below.
7. Commit anything or wait actions auto run, and you will receive the message of run result.

#### Telegram Bot Usage

1. Contact BotFather to create a bot and get your **BOT_TOKEN**.
2. Reply to your bot with any message, then access this link(change TOKEN to your own):
   - `https://api.telegram.org/botTOKEN/getUpdates`
3. In this pages, you'll see your **id**.(Close to *username*, *first_name*)
4. Add two secrets. 
   1. Name: **BOT_TOKEN**, Value: *Your BOT_TOKEN*.
   2. Name: **CHAT_ID**, Value: *Your id*.
5. Enjoy~

#### ServerChan Usage

1. Open [ServerChan](http://sc.ftqq.com/) and follow the instructions to get your own SCKEY.
2. Add a secret. Name: **SCKEY**, Value: *Your SCKEY*.
3. Enjoy~

### Run locally

1. Download *local.py*.
2. Prepare local environment: **Python 3.6+**.
3. Install dependencies:

```python
pip install requests
pip install beautifulsoup4
pip install lxml
```

4. Run this:

```bash
python local-report.py [account] [password]
```

5. Actually you can report any time you want.

#### Change report time(Use with caution)

1. Code **default** execution now time.
2. If you want to change report time, delete these code:

```python
if time_peking.hour % 24 < 12:
        timeType = "上午"
    else:
        timeType = "下午"
    now = time_peking.strftime("%Y-%m-%d %H:%M")
```

3. In the same location, add the time you want in the form of the code below:

```python
    timeType = "下午"
    now = "2021-02-02 17:51"
```

### Fix missing(Multiple)

1. In this mode, you can fix your past missing report(s).
2. This program will auto report from 2021.01.29 to now.
3. Unless there are too much missing reports, this way is not recommended. 
4. The usage is simlilar to *Run locally* part.
>1. Download *fix-missing.py*.
>2. Prepare local environment: **Python 3.6+**.
>3. Install dependencies.
>4. Run.

## To Do List

- [x] Telegram bot support
- [x] ServerChan support
- [x] Fail feedback
- [x] Fix bug
- [ ] Auto Rerun(When failed)

## Credits

[zsqw123/Automatic-Health-Card](https://github.com/zsqw123/Automatic-Health-Card)

[JLUZHAnalytica/Automatic-Health-Card](https://github.com/JLUZHAnalytica/Automatic-Health-Card)(Original Author)

[eternnoir/pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

### Special thanks

[**Hyneman**](https://github.com/HynemanKan)
