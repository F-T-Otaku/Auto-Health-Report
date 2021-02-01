# Auto-Health-Report
Automatically complete SUES daily health report.

***First,You NEED to REGISTER A GITHUB ACCOUNT and LOG IN.***

## How to use

1. Fork my repo. (Give me a star if you like this. lol)
2. Open your own repo and choose "Settings".
3. In the left sidebar, click Secrets.
4. Click New repository secret.
5. Type "NUM" and "PWD" for your secret in the Name input box and enter the Value for your secret.
6. Commit anything or wait actions auto run.

## Attention

1. Pls edit your own cron table in autohealthyreport.yml.
2. Action's cron table runs in UTC.
3. **You need post manually at least 1 time.**

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
   - *P.S. UTC is eight hours later than CST.*
   - *P.P.S. CST – China Standard Time*

## ServerChan Usage

1. Open [ServerChan](http://sc.ftqq.com/) and follow the instructions to get your own SCKEY.
2. Add a secret. Name: sckey, Value: Your SCKEY.
3. Enjoy~

## To Do List

- [ ] Telegram bot support
- [x] ServerChan support
