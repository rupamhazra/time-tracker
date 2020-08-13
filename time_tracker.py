#!/usr/bin/env python

import pyautogui
from time import sleep
from datetime import *
import time
from random import randint
import os
import threading
import socket
import pymysql
import requests


sleep(1)
connection = pymysql.connect(
    host="localhost",
    user="localhost",
    passwd="123456",
    database="tracker_management" 
    )
cursor = connection.cursor()

sys_name = socket.gethostname()

system_unique_code = sys_name +"_"+datetime.now().strftime("%d_%m_%Y")
#print("system name: ", sys_name)

class Tracker():
    def __init__(self):
        self.path = r"C:\Users\rupam\Tracker"
        self.upload_url = "http://localhost/add_image_tracker/"
        self.tt_id = 0
    """docstring for ClassName"""
    def timecalculator(self):
        value = []
        working_time = 0
        non_working_time = 0
        end_min = 0
        pc_str_time = datetime.now()
        sql = ""
        insert_flag = 0
        #print("pc_str_time: ",pc_str_time)
        system_start_date = pc_str_time.strftime("%d/%m/%Y")
        system_start_time = pc_str_time.strftime("%H:%M:%S")
        str_hour = int(pc_str_time.strftime("%H"))
        str_min = int(pc_str_time.strftime("%M"))
        end_hour = int(pc_str_time.strftime("%H"))

        while ((str_hour>=9)&(end_hour<=19)):
            value1 = []
            if insert_flag == 0:
                print('check')
                cursor.execute("SELECT id FROM time_tracking_timetracking WHERE system_name=%s AND system_start_date=%s", [sys_name,system_start_date])
                if cursor.rowcount == 0:
                    print('no data')
                    sql = "INSERT INTO time_tracking_timetracking (system_name, system_start_date, system_start_time, working_time, non_working_time, system_unique_code) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (sys_name,system_start_date, system_start_time, working_time, non_working_time,system_unique_code)
                    cursor.execute(sql, val)
                    connection.commit()
                    self.tt_id = cursor.lastrowid
                insert_flag = 1
            


            if((str_hour>=10)&(end_hour<19)):
                currentMouseX_1, currentMouseY_1 = pyautogui.position()
                tm1 = int(time.time())
                sleep(600)
                tm2 = int(time.time())

                tm_span = tm2 - tm1
                currentMouseX_2, currentMouseY_2 = pyautogui.position()

                if((currentMouseX_1==currentMouseX_2)&(currentMouseY_1==currentMouseY_2)):
                    non_working_time = non_working_time + tm_span
                    print(non_working_time)

                else:
                    working_time = working_time + tm_span
                    print(working_time)

                end_time = datetime.now()
                end_hour = int(end_time.strftime("%H"))
                end_min = int(end_time.strftime("%M"))
                try:
                    sql_update = "UPDATE time_tracking_timetracking SET working_time = %s, non_working_time = %s WHERE system_name = %s and system_start_date = %s"
                    val1 = (working_time, non_working_time, sys_name, system_start_date)
                    #value1.append(val1)
                    cursor.execute(sql_update, val1)
                    connection.commit()
                    sleep(1)
                except Exception as er:
                    # print("Oops! Something wrong")
                    print("error_up: ",er)
                

                print("your not working time",non_working_time)
                print("your working time",working_time)
            if str_hour <10:
                print("Wait a minute")
                sleep(60)


    def takescreenshot(self):
        hostname = socket.gethostname()
        now_date = datetime.now()
        file_name = now_date.strftime("%d_%m_%Y")
        print(file_name)
        path = '{}/{}'.format(self.path, file_name)

        if not os.path.isdir(path):
            os.makedirs(path)
            # print("Path created")

        x = [randint(1, 59) for q in range(0, 12)]
        new_list = [i * 60 for i in x]
        for i in range(len(new_list)):
            value_img = []
            noworking_time = datetime.now()
            cur_time = noworking_time.strftime("%H_%M_%S")
            shot_time_H = int(noworking_time.strftime("%H"))
            if i==0:
                sleep(new_list[0])
                cur_time = noworking_time.strftime("%H_%M_%S")
                image_name = "img_{}.png".format(cur_time)
                img_shot = pyautogui.screenshot('{}/{}/img_{}.png'.format(self.path, file_name,cur_time))
                image_path = '{}/{}/img_{}.png'.format(self.path, file_name,cur_time)
            else:
                s_time = 3600 - new_list[i-1] + new_list[i]
                sleep(s_time)
                cur_time = noworking_time.strftime("%H_%M_%S")
                image_name = "img_{}.png".format(cur_time)
                img_shot = pyautogui.screenshot('{}/{}/img_{}.png'.format(self.path, file_name,cur_time))
                image_path = '{}/{}/img_{}.png'.format(self.path, file_name,cur_time)

            try:               
                image_filename = os.path.basename(image_path)
                multipart_form_data = {
                "image_path": (image_filename, open(image_path, 'rb')),
                "system_unique_code": (None, system_unique_code),
                "image_name" : (None, image_filename)
                }
                response = requests.post(self.upload_url, files=multipart_form_data)
                print("response API: ",response.status_code)


            except Exception as e:
                print()
                # print("Oops! Something wrong(img)")
                # raise e


class ThreadTest1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run (self):
        tk = Tracker()
        tk.timecalculator()
        

class ThreadTest2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        tk = Tracker()
        tk.takescreenshot()


th1 = ThreadTest1()
th1.start()
th2 = ThreadTest2()
th2.start()

