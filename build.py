# coding=UTF-8
import getopt
import sys

import ApkTool

__author__ = 'liushu'

helpRecomplie = " python build.py --recompile -s dest.apk -n 1.0.1 -c 1000 \n" \
                " -s:dest apk\n" \
                " -n:versionNam\n" \
                " -c:versionCode\n"

helpChannel = "  python build.py --channel -s dest.apk -c china,us \n" \
              "  -s:dest.apk \n " \
              "  -c:channellist\n"

helpCommand = helpRecomplie + "\n" + helpChannel


def ____getOpt(arg):
    opts, args = getopt.getopt(arg, "hs:c:n:", ["recompile", "channel"])
    if not opts:
        ____help(helpCommand)
    firstParam = opts[0][0]
    if "--recompile" == firstParam:
        ____recompile(opts)
    if "--channel" == firstParam:
        ____channel(opts)
    return


def ____channel(opts):
    source = ""
    channelist = ""
    for op, value in opts:
        if op == "-s":
            source = value
        elif op == "-c":
            channelist = value
    if (len(channelist) == 0 or len(source) == 0):
        ____help(helpChannel)
    ApkTool.installFrameworkRes()
    ApkTool.decompile(source)
    channelist = channelist.split(",")
    for channel in channelist:
        ApkTool.modify(source[0:len(source) - 4], channel)
        ApkTool.compile(source[0:len(source) - 4], channel)
        ApkTool.clean(source[0:len(source) - 4])
    return


def ____recompile(opts):
    source = ""
    versionCode = ""
    versionName = ""
    for op, value in opts:
        if op == "-s":
            source = value
        elif op == "-c":
            versionCode = value
        elif op == "-n":
            versionName = value
    if len(source) == 0:
        ____help(helpRecomplie)
    ApkTool.installFrameworkRes()
    ApkTool.decompile(source)
    if len(versionCode) == 0 or len(versionName) == 0:
        ApkTool.modify(source[0:len(source) - 4])
    else:
        print versionCode + versionName
        ApkTool.modify(source[0:len(source) - 4], None, versionCode, versionName)
    ApkTool.compile(source[0:len(source) - 4], "recompile")
    ApkTool.clean(source[0:len(source) - 4])

    return


def ____help(content):
    print content
    exit(0)


def ____process(args):
    ____getOpt(args)
    return


____process(sys.argv[1:])
