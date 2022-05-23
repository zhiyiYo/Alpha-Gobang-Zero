# coding:utf-8
import sys
from platform import platform

from win32con import DESKTOPHORZRES, HORZRES
from win32gui import GetDC, ReleaseDC
from win32print import GetDeviceCaps


def getWindowsVersion():
    if "Windows-7" in platform():
        return 7

    build = sys.getwindowsversion().build
    version = 10 if build < 22000 else 11
    return version


def getDevicePixelRatio():
    """ get dpi scale ratio """
    hdc = GetDC(None)
    t = GetDeviceCaps(hdc, DESKTOPHORZRES)
    d = GetDeviceCaps(hdc, HORZRES)
    ReleaseDC(None, hdc)
    return t / d
