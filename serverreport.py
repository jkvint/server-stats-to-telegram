#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import requests
import psutil

# configs: 
servername = "BACKUP WITNESS"      # Give a name so you recognise your server in the chat
diskmountedon = "/home"            # Do a `df -h` to discover which HDD you want to monitor the space of           
telegram_token = ""                # Create your Telegram bot at @BotFather (https://telegram.me/botfather)
telegram_id    = ""                # Get your telegram id at @MyTelegramID_bot (https://telegram.me/mytelegramid_bot)

# Telegram barebones apicall
def telegram(method, params=None):
    url = "https://api.telegram.org/bot"+telegram_token+"/"
    params = params
    r = requests.get(url+method, params = params).json()
    return r

# Telegram notifyer
def alert_witness(msg):
    # Send TELEGRAM NOTIFICATION
    payload = {"chat_id":telegram_id, "text":msg,"parse_mode":"HTML"}
    m = telegram("sendMessage", payload)

disk = os.statvfs(diskmountedon)

totalBytes = float(disk.f_bsize*disk.f_blocks)
totalUsedSpace = float(disk.f_bsize*(disk.f_blocks-disk.f_bfree))
totalAvailSpaceNonRoot = float(disk.f_bsize*disk.f_bavail)
pctuse = totalUsedSpace/totalBytes * 100

# using psutil for disk usage...
cpu = (psutil.cpu_percent(interval=1, percpu=True))
mem = psutil.virtual_memory()

cputext = ""
i = 0
for res in cpu:
    i = i+1
    cputext = cputext + "Core "+str(i)+": "+str(res)+"%\n"

pctram = (mem.total - mem.available) / mem.total * 100

witnesstext = "📋  <b>"+servername+"</b> 📋\n\n<b>DiskSpace:</b>\nAvailable: %.2f GB.\nUsed: %.2f GB (%.1f%%)\n\n<b>CPU</b>\n%s\n<b>RAM</b>\nAvailable: %.2f GB\nUsed: %.2f GB (%.1f%%)" % (totalAvailSpaceNonRoot/1024/1024/1024, totalUsedSpace/1024/1024/1024, pctuse, cputext, mem.available/1024/1024/1024,(mem.total-mem.available)/1024/1024/1024, pctram)

alert_witness(witnesstext)
