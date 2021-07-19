import os,sys
import time
from datetime import date, datetime

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests


wd = os.getcwd()
elearnWebPage='https://elearn.hrd.gov.tw/mooc/index.php'
eGOV='https://www.cp.gov.tw/portal/Clogin.aspx?ReturnUrl=https%3A%2F%2Felearn.hrd.gov.tw%2Fegov_login.php'

class Elearn:
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


    def loginElear(self):
        print('登入E政府')
        self.driver.get(eGOV) 
        time.sleep(1)
        tryTimes=0
        while self._check_logined()==0:
            time.sleep(1)
            if tryTimes !=0 and tryTimes<=3:
                print('帳號或是密碼錯誤')
                self.id=str(input('輸入E政府帳號 : '))
                self.pw=str(input('輸入E政府密碼 : '))
            elif tryTimes > 3:
                print('嘗試過多次數')
                os.system("pause")
                exit()

            tryTimes=tryTimes+1
            try:
                idTextBox=self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$AccountPassword1$txt_account')
                time.sleep(0.1)
                pwTextBox =self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$AccountPassword1$txt_password')
                time.sleep(0.1)
                loginButton =self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$AccountPassword1$btn_LoginHandler')
                time.sleep(0.1)
                idTextBox.send_keys(self.id)
                pwTextBox.send_keys(self.pw)
                time.sleep(0.1)
                loginButton.click();      
                time.sleep(0.1)
                self.driver.switch_to_alert().accept()
                time.sleep(0.1)
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(0.1)
            except:
                print('登入失敗')
            

    def _check_logined(self):
        try:
            idTextBox=self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$AccountPassword1$txt_account')
            return 0
        except:
            return 1


    def downloadLicense(self,year):
        tryTimes=0
        while self._gotoLicensePage()==0 and tryTimes<10:
            self.loginElear();
            tryTimes=tryTimes+1

        try:
            print('下載證書...')
            downloadButton=self.driver.find_element_by_link_text('列印證書')
            time.sleep(0.1)
            downloadButton.click()
            time.sleep(0.1)
            select = Select(self.driver.find_element_by_name('pass_year'))
            time.sleep(0.1)
            select.select_by_value(str(year))
            time.sleep(0.1)
            check_allButton=self.driver.find_element_by_id('check_all')
            time.sleep(0.1)
            check_allButton.click()
            create_pdfButton=self.driver.find_element_by_id('create_pdf')
            time.sleep(0.1)
            create_pdfButton.click()
            ROC_year=str(int(datetime.now().strftime('%Y'))-1911)
            self.licenseFileName = self.licenseFileName + ROC_year+str(datetime.now().strftime('%m%d%H%M'))+'.pdf'
            time.sleep(0.1)
        except:
            print('下載時發生錯誤')

        time.sleep(0.1)
        print('取得證書資料...')
        self._getTableData()
        self._addLicenseSource(year)
        print('完成取得')
        self.driver.close()


    def _getTableData(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        table=soup.find('table', attrs={'id':'table_print'})
        tbody=table.find('tbody')  
        for tr in tbody.findAll('tr'):
            td_index=0
            for td in tr.findAll('td'):
                if td_index ==1:
                    id=td.find('div').get_text()
                elif td_index == 2:
                    subject=td.find('div').get_text()
                elif td_index == 3:
                    qualifiedDate=td.find('div').get_text()

                td_index=td_index+1
            
            qualifiedDate=str(int(qualifiedDate[0:4])-1911)+qualifiedDate[4:len(qualifiedDate)]
            qualifiedDate=qualifiedDate.replace('-','/')
            course={
                'id':id,
                'subject':subject,
                'source':'',
                'date':qualifiedDate,
                'hour':'',
                'status':''
            }
            self.LicenseData.append(course)

    def deleteLicense():
        print('未完工')

    def _gotoLicensePage(self):
        self.driver.get('https://elearn.hrd.gov.tw/mooc/user/learn_stat.php')
        time.sleep(0.1)
        try:
            self.driver.find_element_by_link_text('登出')
        except:
            print('已登出 重新嘗試登入')
            return 0
        time.sleep(0.1)        
        print('已登入')
        return 1

    def _addLicenseSource(self,year):
        self._gotoLicensePage()
        try:
            select = Select(self.driver.find_element_by_name('curYear'))
            time.sleep(0.1)
            select.select_by_value(str(year))
            time.sleep(0.1)
            self.driver.execute_script('doSearch()')
            time.sleep(1)
        except:
            print('查詢失敗')

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        table=soup.find('table', attrs={'class':'table subject'})
        tbody=table.find('tbody')  
        time.sleep(1)
        for tr in tbody.findAll('tr'):
            sorce=self._getSource(tr.get('onclick'))
            td_index=0
            for td in tr.findAll('td'):
                if td_index==2:
                    tempSubJect=td.find('div').get_text()
                    SubJectID=self._segSTR(tempSubJect)
                elif td_index==9:
                    strHour=td.find('div').get_text()
                    intHour=strHour[0:strHour.index('.')]
                td_index=td_index+1

            for i in range(len(self.LicenseData)):
                if self.LicenseData[i]['id']== SubJectID['id'] and self.LicenseData[i]['subject'] == SubJectID['subject']:
                    self.LicenseData[i]['hour']=intHour
                    self.LicenseData[i]['source']=sorce


    def _getSource(self,FunctionName):
        leftIndex=FunctionName.index('(')
        rightIndex=FunctionName.index(')')
        id=FunctionName[leftIndex+1:rightIndex]   
        url ='https://elearn.hrd.gov.tw/info/'+id 
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}    
        resp = requests.get(url,headers=headers)
        resp.encoding = 'utf-8' 
        soup=BeautifulSoup(resp.text,'html.parser')
        titleDiv=soup.find_all('div', attrs={'class':'course-goal'})
        subDiv=titleDiv[1].find_all('div')
        source=subDiv[1].text
        time.sleep(0.1)
        return source

    def _segSTR(self,tempSTR):
        leftIndex=tempSTR.index('(')
        rightIndex=tempSTR.index(')')
        id=tempSTR[leftIndex+1:rightIndex]
        subject=tempSTR[0:leftIndex]
        temp={
            'id':id,
            'subject':subject
        }
        return temp 

    def close(self):
        self.driver.close()
        



if __name__ == '__main__': 
    brower=Elearn()
    brower.openWebPage()
    brower.loginElear()
    brower.downloadLicense(2021)

