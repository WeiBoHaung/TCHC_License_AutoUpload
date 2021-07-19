import sys,os
import time



from Elearn import Elearn
from TCHC import TCHC


if __name__ == '__main__':

    elearnID=str(input('輸入E政府帳號 : '))

    elearnPW=str(input('輸入E政府密碼 : '))
    elearn=Elearn(elearnID,elearnPW)
    elearn.loginElear()
    year=str(input('輸入要登記年份輸入西元 : '))
    elearn.downloadLicense(2021)
    tchcID=str(input('輸入台中市月嫂平台帳號 : '))
    tchcPW=str(input('輸入台中市月嫂平台密碼 : ') )

    tchc=TCHC(tchcID,tchcPW)
    tchc.loginTCHC()
    tchc.checkLicense(elearn.LicenseData)
    tchc.addLicence(elearn.licenseFileName)
    time.sleep(10)
    tchc.close()
    