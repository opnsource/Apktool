#!/usr/bin/env python
# coding:UTF-8

import os
import subprocess
import zipfile
import shutil


# -
# 解压APK文件
# -
def _____unzipApkFile(apkFilePath, unzipPath):
    if not os.path.exists(unzipPath):
        os.makedirs(unzipPath, 0777)
    zf = zipfile.ZipFile(apkFilePath)

    for name in zf.namelist():
        # print name
        if name.endswith(os.sep):
            os.makedirs(os.path.join(unzipPath, name), 0777)
        else:
            ext_filename = os.path.join(unzipPath, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir):
                os.makedirs(ext_dir, 0777)
            outfile = open(ext_filename, 'wb')
            outfile.write(zf.read(name))
            outfile.close()
    zf.close()

    print "--unzipApkFile %s to %s finish." % (apkFilePath, unzipPath)


# -
# 重新压缩成APK文件
# -
def _____zipApkFile(unzipPath, apkFilePath):
    filelist = []
    if os.path.isfile(unzipPath):
        filelist.append(unzipPath)
    else:
        for root, dirs, files in os.walk(unzipPath):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(apkFilePath, "w", zipfile.zlib.DEFLATED)
    for name in filelist:
        arcname = name[len(unzipPath):]
        # print arcname
        zf.write(name, arcname)
    zf.close()

    print "--zipApkFile %s to %s finish." % (unzipPath, apkFilePath)


# -
# 格式对齐APK文件
# -
def _____zipalignApkFile(signedApkPath, alignedApkPath):
    alignCmd = "zipalign -f 4 %s %s" % (signedApkPath, alignedApkPath)
    # print alignCmd
    print "--zipalignApkFile %s..." % signedApkPath
    subprocess.check_call(alignCmd, shell=True)
    print "--zipalignApkFile %s finish." % signedApkPath


def rezip(sourceApk, rezipApk):
    # 临时解压APK目录
    unzipTempDir = "unzip_temp"

    # 解压APK文件
    _____unzipApkFile(sourceApk, unzipTempDir)

    # 重新压缩成APK文件
    rezipTempApk = "rezip_temp.apk"
    _____zipApkFile(unzipTempDir, rezipTempApk)

    # 对重压缩的文件进行4字节对齐
    _____zipalignApkFile(rezipTempApk, rezipApk)

    # 删除临时文件和目录
    if os.path.exists(unzipTempDir):
        shutil.rmtree(unzipTempDir)
    if os.path.exists(rezipTempApk):
        os.remove(rezipTempApk)
    print "Finish reziping [%s] to [%s]." % (sourceApk, rezipApk)
    print "\nreziping package successfully!"
