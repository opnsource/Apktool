# coding:UTF-8
import ConfigParser
import os
import re
import shutil
import subprocess
from xml.etree.ElementTree import parse, register_namespace

import RezipApk

tempApk = "signed.apk"
zipApk = "zip."
androidName = "{http://schemas.android.com/apk/res/android}name"


def __init__():
    return


def decompile(decompile_fileApk):
    command = "java  -jar  apktool.jar d -f %s " % decompile_fileApk
    subprocess.check_call(command, shell=True)
    return


def compile(compile_file, channel):
    command = "java -jar  apktool.jar b %s " % compile_file
    subprocess.check_call(command, shell=True)
    ____signature(compile_file)
    souceApk = ____alignzip(compile_file, channel)
    ____reZip(souceApk, compile_file + "_channel_" + channel + ".apk")
    if (os.path.exists(souceApk)):
        os.remove(souceApk)
    return


def ____reZip(sourceApk, destApk):
    RezipApk.rezip(sourceApk, destApk)


def clean(compile_file):
    if os.path.exists(compile_file):
        shutil.rmtree(compile_file, False, None)
    if os.path.exists(tempApk):
        os.remove(tempApk)


def ____alignzip(complie_file, channel):
    destApk = complie_file + "_" + channel + "_align.apk";
    if (os.path.exists(destApk)):
        os.remove(destApk)
    command = " zipalign -v 4 %s %s " % (tempApk, destApk)
    subprocess.check_call(command, shell=True)
    return destApk


def ____signature(complie_file):
    cf = ConfigParser.ConfigParser()
    cf.read("build.conf")
    keystore = cf.get("config", "key.store")
    keystorePass = cf.get("config", "key.store.password")
    alias = cf.get("config", "key.alias")
    aliasPass = cf.get("config""", "key.alias.password")
    sysComand = "jarsigner -digestalg SHA1 -sigalg MD5withRSA -verbose -keystore  %s -storepass %s " \
                " -keypass %s -signedjar %s  %s/dist/%s.apk %s " % (
                    keystore, keystorePass, aliasPass, tempApk, complie_file, complie_file, alias)
    subprocess.check_call(sysComand, shell=True)
    return


'''修改包名'''


def ____modifyManifest(complie_file):
    cf = ConfigParser.ConfigParser()
    cf.read("build.conf")
    packageName = cf.get("modify", "app.package")
    modifyName = cf.get("modify", "modify.package")
    out = complie_file + "/AndroidManifest.xml"
    manifest = open(out, 'r')
    tmp = complie_file + "/AndroidManifest1.xml"
    if (os.path.exists(tmp)):
        os.remove(tmp)
    content = ""
    manifestNew = open(tmp, 'wb')
    while True:
        line = manifest.readline()
        if (len(line) == 0):
            break
        content += line
    findStr = "package=\"%s\"" % (packageName)
    replaceStr = "package=\"%s\"" % (modifyName)
    content = re.sub(findStr, replaceStr, content)
    manifestNew.writelines(content)
    manifestNew.flush()
    manifestNew.close()
    manifest.close()
    if (os.path.exists(out)):
        os.remove(out)
    os.rename(tmp, out)
    ____modifyAttr(out, packageName)
    return


def ____modifyAttr(manifest, packageName):
    # 防止namespace变更
    register_namespace('android', "http://schemas.android.com/apk/res/android")
    doc = parse(manifest)
    root = doc.getroot()
    application = root.find('application')
    # 修改activity
    activitys = application.findall('activity')
    ____updateFramework(activitys, packageName)
    # 修改service
    services = application.findall('service')
    ____updateFramework(services, packageName)
    # 修改provide
    providers = application.findall('provider')
    ____updateFramework(providers, packageName)
    # 修改广播器
    receivers = application.findall('receiver');
    ____updateFramework(receivers, packageName)
    doc.write(manifest)
    return


def ____updateFramework(framework_list, packageName):
    for framework in framework_list:
        name = ____replaceAndroidName(packageName, framework.attrib[androidName])
        framework.set(androidName, name)


def ____modifyLayout(compile_file):
    cf = ConfigParser.ConfigParser()
    cf.read("build.conf")
    packageName = cf.get("modify", "app.package")
    resFile = compile_file + "/res";
    files = os.listdir(resFile)
    for file in files:
        if os.path.isdir(os.path.join(resFile, file)):
            if str(file).startswith("layout"):
                ____modifyLayoutInner(packageName, os.path.join(resFile, file))
    return


def ____modifyLayoutInner(packageName, rootFile):
    if not os.path.isdir(rootFile):
        return
    files = os.listdir(rootFile)
    for file in files:
        file = os.path.join(rootFile, file);
        if not os.path.isfile(file):
            continue
        input = open(file, 'r')
        lines = ""
        while True:
            line = input.readline()
            if len(line) == 0:
                break;
            lines += line
        pattern = "http://schemas.android.com/apk/res/" + packageName
        replace = "http://schemas.android.com/apk/res-auto"
        lines = re.sub(pattern, replace, lines)
        input.close()
        out = open(file, 'w')
        out.writelines(lines)
        out.flush()
        out.close()
    return


def ____modifyVersion(complie_file, versionCode, versionName):
    out = complie_file + "/apktool.yml"
    files = open(out, 'r')
    tmp = complie_file + "/apktool1.yml"
    if (os.path.exists(tmp)):
        os.remove(tmp)
    output = open(tmp, 'wb')
    lines = "";
    while True:
        line = files.readline()
        if (len(line) == 0):
            break;
        lines += line
    lines = re.sub("versionCode:[\d\S'\. ]*", "versionCode:  %s" % (versionCode), lines)
    lines = re.sub("versionName:[\d\S'\. ]*", "versionName:  %s" % (versionName), lines)
    output.writelines(lines)
    output.flush()
    output.close()
    files.close()
    if (os.path.exists(out)):
        os.remove(out)
    os.rename(tmp, out)
    return


def installFrameworkRes():
    if (os.path.exists("framework-res.apk")):
        command = "java -jar apktool.jar if framework-res.apk"
        subprocess.call(command, shell=True)


def ____modifyChannel(complie_file, channel):
    cf = ConfigParser.ConfigParser()
    cf.read("build.conf")
    channelFile = cf.get("modify", "app.channel")
    file = str(complie_file) + str(channelFile);
    cFile = open(file, 'w')
    cFile.writelines(channel)
    cFile.flush()
    cFile.close()


def modify(complie_file, channel=None, versionCode=None, versionName=None):
    if versionCode and versionName and ((len(versionCode) != 0 and len(versionName) != 0)):
        if (str(versionCode).isdigit()):
            versionCode = "'" + versionCode + "'"
        ____modifyVersion(complie_file, versionCode, versionName)
    if channel and (len(channel) != 0):
        ____modifyChannel(complie_file, channel)
    ____modifyManifest(complie_file)
    ____modifyLayout(complie_file)


def ____replaceAndroidName(packageName, value):
    value = str(value)
    if (value.startswith(".")):
        value = packageName + value
    return value
