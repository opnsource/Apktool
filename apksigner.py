#!/usr/bin/env python
# coding:UTF-8
import os
import subprocess
from configparser import ConfigParser
from time import sleep

parent = "D:/jiagu/"
out = "D:/jiaguout/"


def ____signature(sourceApk):
    cf = ConfigParser()
    cf.read("build.conf")
    keystore = cf.get("config", "key.store")
    keystorePass = cf.get("config", "key.store.password")
    alias = cf.get("config", "key.alias")
    aliasPass = cf.get("config""", "key.alias.password")
    targetApk = sourceApk[0:len(sourceApk) - 4] + "_sign.apk"
    apks = targetApk.split("_")
    outapks = "app-release_100"
    count = 0
    for temps in apks:
        if (count >= 2):
            outapks = outapks + "_" + temps
        count = count + 1
    sysComand = " C:/Users/Administrator/AppData/Local/Android/Sdk/build-tools/33.0.1/apksigner.bat sign  --v2-signing-enabled true --ks %s --ks-key-alias %s --ks-pass pass:%s --key-pass pass:%s --v1-signing-enabled true --out %s   %s " % (
        keystore, alias, keystorePass, aliasPass, out + outapks, parent + sourceApk)
    print(sysComand)
    subprocess.check_call(sysComand, shell=True)
    return


if __name__ == '__main__':
    files = os.listdir(parent)
    for file in files:
        ____signature(file)