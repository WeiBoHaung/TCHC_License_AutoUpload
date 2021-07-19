import os,sys
import time
from datetime import date, datetime
from pytesseract.pytesseract import Output

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import cv2 
import pytesseract
from PIL import Image
import numpy as np

wd = os.getcwd()
tchcWebPage='https://phcs.taichung.gov.tw/tchcPublic/front/login_mm'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
class TCHC:
    def __init__(self,id,pw):
        self.chromePath=wd+"\chromedriver"
        self.licenseFileName='通過認證時數證書'
        self.id=id
        self.pw=pw
        self.LicenseData=[]
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': wd+'\License'}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(self.chromePath,chrome_options=options)
        self.driver.minimize_window()

    def loginTCHC(self):
        print('登入台中市月嫂平台')
        self.driver.get(tchcWebPage) 
        time.sleep(1)
        tryTimes=0
        while self._check_logined()==0 and tryTimes<10:
            time.sleep(1)
            try:
                tryTimes=tryTimes+1
                idTextBox=self.driver.find_element_by_name('username')
                time.sleep(0.1)
                pwTextBox =self.driver.find_element_by_name('password')
                time.sleep(0.1)
                idTextBox.send_keys(self.id)
                pwTextBox.send_keys(self.pw)
                time.sleep(0.1)
                captchaBox=self.driver.find_element_by_id('captcha')
                time.sleep(0.1)
                captchaImage=self.driver.find_element_by_id('simpleCaptcha_image')
                time.sleep(0.1)
                captchaCode=self._get_captcha(captchaImage,'temp.jpg')
                captchaBox.send_keys(captchaCode)
                time.sleep(0.1)
                pwTextBox.send_keys(Keys.ENTER)
                time.sleep(0.1)

            except :
                print('登入發生TCHC問題')

        
    def _check_logined(self):
        try:
            idTextBox=self.driver.find_element_by_name('username')
            idTextBox.send_keys(Keys.ENTER)
            print('驗證碼辨認錯誤')
            return 0
        except:
            print('登入成功')
            return 1

    def _get_captcha(self,element,name):
        element.screenshot(name)  
        path = wd+'\\'+name
        src = cv2.imread(path) 
        # cv2.imshow('input',src)
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
        lower_black=np.array([0,0,0])
        upper_black=np.array([125,125,125])
        mask=cv2.inRange(hsv,lower_black,upper_black)
        open_out=mask
        cv2.bitwise_not(open_out, open_out)
        # cv2.imshow("open_out", open_out)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        textImage = Image.fromarray(open_out)
        # textImage.save(wd+'\\'+'test.png')
        text = pytesseract.image_to_string(textImage,lang='eng')
        print("驗證碼辨識结果： %s" % text[0:4])       
        return text[0:4]


    def checkLicense(self,licenseData):
        print('確認研習資料...')
        self.driver.get('https://phcs.taichung.gov.tw/tchcPublic/mmUser/study_list')
        time.sleep(0.1)
        self._getTableData()
        for newLicense in licenseData:
            for oldLicense in self.LicenseData:
                if newLicense['subject']==oldLicense['subject'] and newLicense['date']==oldLicense['date'] and newLicense['subject']==oldLicense['subject']:
                    if oldLicense['status']== '審核通過':
                        newLicense['status']= '審核通過'
                    elif oldLicense['status'] == '待審核':
                        newLicense['status']='待審核'

        self.LicenseData=licenseData
        print('確認完成')

    def addLicence(self,licenseFileName):
        print('新增資料中.....')
        for licenseList in self.LicenseData:
            if licenseList['status']=='':
                print('新增 %s' % licenseList['subject'])
                self._addLicensePage()
                try:
                    dateBox=self.driver.find_element_by_name('hc310.classDt')
                    sourceBox=self.driver.find_element_by_name('hc310.unit')
                    subjectBox=self.driver.find_element_by_name('hc310.name')
                    hourBox=self.driver.find_element_by_name('hc310.time')
                    idBox=self.driver.find_element_by_name('hc310.dNum')
                    inputFile=self.driver.find_element_by_name('HC310_1')
                    for btn in self.driver.find_elements_by_tag_name('button'):
                        if btn.text=='儲存':
                            submitBtn=btn
                    dateBox.send_keys(licenseList['date'])
                    sourceBox.send_keys(licenseList['source'])
                    subjectBox.send_keys(licenseList['subject'])
                    hourBox.send_keys(Keys.DELETE)
                    hourBox.send_keys(licenseList['hour'])
                    idBox.send_keys(licenseList['id'])
                    inputFile.send_keys(wd+'/License/'+licenseFileName)
                    time.sleep(0.1)
                    submitBtn.click()
                    print('成功')
                except:
                    print('新增時發生錯誤')
            elif licenseList['status']== '審核通過':
                print('[%s] 已審核通過' % licenseList['subject'])
            elif licenseList['status']== '待審核':
                print('[%s]   ，待審核' % licenseList['subject'])

        print('新增完成')

    def _getTableData(self):
        print('取得目前已登記資料')
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        table=soup.find('table', attrs={'id':'resultList'})
        tbody=table.find('tbody')  
        for tr in tbody.findAll('tr'):
            td_index=0
            for td in tr.findAll('td'):
                if td_index == 0:
                    qualifiedDate=td.get_text()
                elif td_index ==1:
                    source=td.get_text()
                elif td_index == 2:
                    subject=td.get_text()
                elif td_index == 3:
                    hour=td.get_text()
                elif td_index == 4:
                    status=td.get_text()

                td_index=td_index+1

            course={
                'subject':subject,
                'source':source,
                'date':qualifiedDate,
                'hour':hour,
                'status':status
            }
            self.LicenseData.append(course)

    def deleteLicense():
        print('未完工')

    def _addLicensePage(self):
        self.driver.get('https://phcs.taichung.gov.tw/tchcPublic/mmUser/study_create')
        time.sleep(0.1)
    
    def close(self):
        self.driver.close()
        



if __name__ == '__main__': 

    brower=TCHC(tchcID,tchcPW)
    brower.loginTCHC()
    time.sleep(10)
    brower.close()