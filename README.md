# Auto-Health-Report

***CAUTION: This repo is only for learning purposes, DO NOT use this repo for real health status reports. The author(s) will not be responsible if anything bad happens.***

***First, you NEED to REGISTER A GITHUB ACCOUNT and LOG IN.***

**You need to report manually on** ***WECHAT WORK*** **at least once before using this tool.**

## How to use

- ~~Fork my repo. (Give me a star if you like this. lol)~~
1. Use my repo template and create your own repo.
2. Open your own repo and choose `Settings`.
3. In the left sidebar, click `Secrets`.
4. Click `New repository secret`.
5. Type `NUM` and `PWD` for your secret in the Name input box and enter the Value for your secret.
6. Commit anything or wait actions auto run.

## Attention

1. Please edit your own cron table in report.yml.
2. Action's cron table runs in ***UTC***.

### How to create your own cron table

1. Open the xxx.yml fill. (Normally is "/.github/workflows/report.yml")
2. Change this to any time you want:
```
  schedule:
    - cron: "15 0 * * *"
    - cron: "20 1 * * *" 
    - cron: "25 6 * * *" 
    - cron: "30 7 * * *" 
```
3. `cron: "20 1 * * *" ` means it runs at 01:20 ***UTC*** every day.

   1. *P.S. UTC is eight hours later than CST.*
   2. *P.P.S. CST – China Standard Time.*
   3. *P.P.P.S. To ensure the report is successful, please set more than 4 times.*

## To Do List

- [x] Fix bug
- [x] Add Webvpn Support
- [ ] Auto Rerun(When failed)

## Credits

[zsqw123/Automatic-Health-Card](https://github.com/zsqw123/Automatic-Health-Card)

[JLUZHAnalytica/Automatic-Health-Card](https://github.com/JLUZHAnalytica/Automatic-Health-Card)(Original Author)

[eternnoir/pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

### Special thanks

[**Hyneman**](https://github.com/HynemanKan)
