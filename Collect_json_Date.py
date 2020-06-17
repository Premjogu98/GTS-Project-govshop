from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import re
import json
import pymysql.cursors
import sys, os
import time
import wx
import random


def Local_connection_links():
    a = 0
    while a == 0:
        try:
            connection = pymysql.connect(host='192.168.0.202',
                                         user='ams',
                                         password='amsbind',
                                         db='CompanyInfoDB',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            return connection
        except pymysql.connect  as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                  "\n", exc_tb.tb_lineno)
            a = 0
            time.sleep(10)


def ChromeDriver():
    app = wx.App()
    browser = webdriver.Chrome(executable_path=str('D:\\PycharmProjects\\Comapany_WEBSITE&MAIL\\chromedriver.exe'))
    browser.maximize_window()
    browser.get('https://govshop.publicspendforum.net/user/log-in/?next=/')
    for User_ID in browser.find_elements_by_xpath('/html/body/div[1]/div/div[1]/form/div[1]/input'):
        User_ID.send_keys('abfsz123@gmail.com')
        break
    for password in browser.find_elements_by_xpath('/html/body/div[1]/div/div[1]/form/div[2]/input'):
        password.send_keys('Gts@1234')
        break
    for LOGIN_BTN in browser.find_elements_by_xpath('/html/body/div[1]/div/div[1]/form/button'):
        LOGIN_BTN.click()
        break
    wx.MessageBox('Jaldi Web Site Pe OTP Dalde Bhi Tabhi Kaam Chalu Hoga', 'OTP', wx.OK | wx.ICON_WARNING)
    time.sleep(120)
    try:
        alert = browser.switch_to_alert()  # Close Alert Popup
        alert.dismiss()
    except:
        pass
    global a
    a = 0
    while a == 0:
        try:

            File_Location = open("D:\\PycharmProjects\\govshop\\For a object value (PAGE NO).txt", "r")  # read TXT File
            Loop_Number = File_Location.read()
            Loop_Number1 = int(Loop_Number)
            # print(Loop_Number)

            Duplicate = 0
            Inserted = 0
            while int(Loop_Number1) != 0:
                browser.get(
                    'https://govshop.publicspendforum.net/suppliers/search/?q=&filters=%7B%22offerings%22%3A%7B%22checked%22%3A%5B%5D%7D%'
                    '2C%22contractcodes%22%3A%7B%22checked%22%3A%5B%5D%7D%2C%22data_sources%22%3A%7B%22ch'
                    'ecked%22%3A%5B%5D%7D%2C%22sbir_awards%22%3A%7B%22checked%22%3A%5B%5D%7D%2C%22enhanced_type%22%3'
                    'A%7B%22checked%22%3A%5B%5D%7D%2C%22business_size%22%3A%7B%22checked%22%3A%5B%5D%7D%2C%22special_program'
                    's%22%3A%7B%22checked%22%3A%5B%5D%7D%2C%22ownership%22%3A%7B%22checked%22%3A%5B%5D%7D%2C%22locations_serv'
                    'ed%22%3A%7B%22checked%22%3A%5B%5D%7D%2C%22business_type%22%3A%7B%22checked%22%3A%5B%5D%7D%2C%22employees%'
                    '22%3A%7B%22checked%22%3A%5B%5D%7D%2C%22annual_revenue%22%3A%7B%22checked%22%3A%5B%5D%7D%2C%22country%22%3A%7B'
                    '%22checked%22%3A%5B%5D%7D%2C%22sam_exclusion%22%3A%7B%22checked%22%3A%5B%5D%7D%7D&shortlist=false&page=' + str(
                        Loop_Number1) + '')
                time.sleep(2)
                Json_Data = ''
                for Json_Data in browser.find_elements_by_xpath("/html/body/pre"):
                    Json_Data = Json_Data.get_attribute('outerHTML')
                    # print(Json_Data)
                    break
                Json_Data = Json_Data.partition("[")[2].partition("]")[0]
                Json_Data1 = [int(e) if e.isdigit() else e for e in Json_Data.split('},')]
                # print(Json_Data1)
                for Json_Data1 in Json_Data1:
                    Json_Data1 = Json_Data1.replace('\\r', '').replace('\\n', '').replace('&amp;', '&')

                    ID = Json_Data1.partition('id\":')[2].partition(",")[0].strip()
                    # print(ID)
                    NAME = Json_Data1.partition('name\":')[2].partition("\",")[0].strip().lstrip(' \"').replace("'", "''")
                    # print(NAME)
                    website_link = Json_Data1.partition('website_link\":')[2].partition("\",")[0].strip().lstrip('"')
                    # print(website_link)
                    description = Json_Data1.partition('description\":')[2].partition("\",")[0].strip().lstrip('"').replace("'", "''")
                    # print(description)
                    slug = Json_Data1.partition('slug\":')[2].partition("\",")[0].strip().lstrip('"').replace("'", "''")
                    # print(slug)
                    doc_link_slug = "https://govshop.publicspendforum.net/supplier-profile/" + str(slug) + ""
                    # print(doc_link_slug)
                    doc_link_json = 'https://govshop.publicspendforum.net/api/suppliers/' + str(ID).strip() + ''
                    # print(doc_link_json)
                    mydb_Local = Local_connection_links()
                    mycursorLocal = mydb_Local.cursor()
                    global b
                    b = 0
                    while b == 0:
                        try:
                            mydb_Local = Local_connection_links()
                            mycursorLocal = mydb_Local.cursor()
                            Duplicate_Email = "Select govshop_ID from govshop_linksdata where govshop_ID = '" + str(ID) + "'"
                            mycursorLocal.execute(Duplicate_Email)
                            results = mycursorLocal.fetchall()
                            # CompanyInfoDB_Local.close()
                            # CompanyInfoDB_cursorLocal.close()
                            if len(results) > 0:
                                print('Duplicate Email')
                                b = 1
                                Duplicate += 1
                            else:
                                Update_Website_Status = "INSERT INTO govshop_linksdata (govshop_ID,orgname,website,description,slug,doc_link_slug,doc_link_json) VALUES ('"+str(ID)+"','"+str(NAME)+"','"+str(website_link)+"','"+str(description)+"','"+str(slug)+"','"+str(doc_link_slug)+"','"+str(doc_link_json)+"')"
                                mycursorLocal.execute(Update_Website_Status)
                                mydb_Local.commit()
                                Inserted += 1
                            b = 1
                            print("Bhai Data Insert Ho gaya Hai: "+str(Inserted)+" , Bhai Ye Tho Duplicate Nikla:"+str(Duplicate)+"")
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n",
                                  fname, "\n",
                                  exc_tb.tb_lineno)
                            mydb_Local.close()
                            mycursorLocal.close()
                            time.sleep(5)
                            b = 0
                Loop_Number1 += 1
                File_Location = open("D:\\PycharmProjects\\govshop\\For a object value (PAGE NO).txt", "w")  # re-Write File
                File_Location.write(str(Loop_Number1))
                File_Location.close()
            a = 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            time.sleep(5)
            a = 0



ChromeDriver()