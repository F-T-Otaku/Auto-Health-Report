# Auto-Health-Report
Automatically complete SUES daily health report.

***CAUTION: This repo is only for learning purposes, DO NOT use this repo for real health status reports. The author(s) will not be responsible if anything bad happens.***

***First,You NEED to REGISTER A GITHUB ACCOUNT and LOG IN.***

**You need to report manually on the** ***WECHAT FOR COMPANY*** **at least once before using this tool.**

## How to use

~~1. Fork my repo. (Give me a star if you like this. lol)~~
1. Use my repo template and use your own repo.
2. Open your own repo and choose "Settings".
3. In the left sidebar, click Secrets.
4. Click New repository secret.
5. Type "NUM" and "PWD" for your secret in the Name input box and enter the Value for your secret.
6. Commit anything or wait actions auto run.

## Attention

1. Pls edit your own cron table in report.yml.
2. Action's cron table runs in ***UTC***.

### How to create your own cron table

1. Open the xxx.yml fill. (Normally is "/.github/workflows/report.yml")
2. Change this to any time you want:
```
  schedule:
    - cron: "17 1 * * *" 
    - cron: "40 1 * * *"  
    - cron: "19 7 * * *"
```
3. `cron: "17 1 * * *" ` means it runs at 01:17 ***UTC*** every day.

   1. *P.S. UTC is eight hours later than CST.*
   2. *P.P.S. CST – China Standard Time.*
   3. *P.P.P.S. To ensure the report is successful, pls set more than 4 times.*

## TelegramBot Usage

1. Contact BotFather to create an bot and get your **BOT_TOKEN**.
2. Reply to your bot with any message, then access this link(change TOKEN to your own):
   - `https://api.telegram.org/botTOKEN/getUpdates`
3. In this pages, you'll see your **id**.(Close to *username*, *first_name*)
4. Add two secret. 
   1. Name: **BOT_TOKEN**, Value: *Your BOT_TOKEN*.
   2. Name: **CHAT_ID**, Value: *Your id*.
5. Enjoy~

## ServerChan Usage

1. Open [ServerChan](http://sc.ftqq.com/) and follow the instructions to get your own SCKEY.
2. Add a secret. Name: **SCKRY**, Value: *Your SCKEY*.
3. Enjoy~


## To Do List

- [x] Telegram bot support
- [x] ServerChan support
- [x] Fail feedback
- [ ] Auto Rerun(When failed)

## Special Thanks
Thanks to [zsqw123](https://github.com/zsqw123/Automatic-Health-Card) and [JLUZHAnalytica](https://github.com/JLUZHAnalytica/Automatic-Health-Card)(Original Author).
