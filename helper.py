import scrape
from bs4 import BeautifulSoup
import json
import re
import pandas as pd

# Fill 0 for first 10 ids
def convertToTarget(num):
    if(num <10):
        res = str(num).zfill(2)
    else:
        res = str(num)
    return(res)

def getCourseInfo():
    raw = scrape.getCourses()
    full = BeautifulSoup(raw,'lxml')
    courses = full.find('tr').find_all('tr')
    resList = []
    targetNumber= 2
    labels = ["rgno","season","ay","course_no","old_cno","lang","section","title_e","title_j","schedule","room","comment","maxnum","instructor","unit"]

    for i in range(len(courses)):
        if i == 0 :
            continue
        # Set Course number
        targetString = convertToTarget(targetNumber)
        id = "ctl00_ContentPlaceHolder1_grv_course_ctl" + targetString + "_lbl_"
        resDict = {}
        for j in range(len(labels)):
            # Generate label
            tarID = id + labels[j]
            # Find element
            res = courses[i].find('span',{'id': tarID}).getText()
            #print(labels[j],": ",res)
            resDict[labels[j]] = res
        # resDict["ids"]=int(resDict["rgno"])
        #resList.append(json.dumps(resDict,ensure_ascii=False))
        resList.append(resDict)
        #print("\n")
        targetNumber = targetNumber + 1
    return resList

def getCourseList():
    x = getCourseInfo()
    resgs=[]
    for x in regs:
        resgs.append(x['rgno'])
    return resgs

def getElaClassrooms():
    day_map = {
        1:'M',
        2:'Tu',
        3:'W',
        4:'Th',
        5:'F',
        6:'Sa'
    }
    room_map = {}
    raw = scrape.getELA()
    for section in raw:
        tables = pd.read_html(section)[0]
        title = tables.loc[0][0]
        if title == ('(Regular)'):
            date_range = range(1,6)
            time_range = range(1,8)
            for i in date_range:
                for j in time_range:
                    pp = tables.loc[j][i]
                    if str(pp) != 'nan' and pp[-5] == ('H' or 'I' or 'T'):
                        # print("{}/{} : {}".format(j,day_map[i],pp[-5:]))
                        period = "{}{}".format(day_map[i].lower(),j)
                        room_map.setdefault(str(pp[-5:]),[]).append(period)

        elif title == ('Component'):
            try:
                col_range = range(3,4)
                row_range = range(1,25)
                for i in col_range:
                    for j in row_range:
                        pp = tables.loc[j][i]
                        # print("{}/{} : {}".format(tables.loc[j][i][:1],tables.loc[j][i][-1],tables.loc[j][i+1]))
                        room_map.setdefault(tables.loc[j][i+1],[]).append("{}{}".format(tables.loc[j][i][:1].lower(),tables.loc[j][i][-1]))
            except:
                continue
        elif title == ('Instructor'):
            col_range = range(1,5)
            row_range = range(2,10)
            for col in col_range:
                period = (tables.loc[1][col])
                for row in row_range:
                    pp = tables.loc[row][col]
                    date = "tu" if period[0] == "T" else period[0]
                    # print("{}/{} : {}".format(date,period[-1],pp))
                    room_map.setdefault(pp,[]).append("{}{}".format(date.lower(),period[-1]))
        else:
            print('Error')
    return room_map

def getOpenClassrooms(term_value = "all"):
    raw = scrape.getCourses(term_value)
    full = BeautifulSoup(raw,'lxml')
    courses = full.find('tr').find_all('tr')
    resList = []
    targetNumber= 2
    courses.pop(0)
    classrooms = {}
    labels = ["rgno","season","ay","course_no","old_cno","lang","section","title_e","title_j","schedule","room","comment","maxnum","instructor","unit"]
    for i in range(len(courses)):
        # Set Course number
        targetString = convertToTarget(targetNumber)
        id = "ctl00_ContentPlaceHolder1_grv_course_ctl" + targetString + "_lbl_"
        resDict = {}
        for j in range(len(labels)):
            # Generate label
            tarID = id + labels[j]
            # Find element
            res = courses[i].find('span',{'id': tarID}).getText()
            resDict[labels[j]] = res
        resDict["id"]=int(resDict["rgno"])
        cno = resDict['course_no']
        schedule = resDict['schedule']
        room = resDict['room']
        shelist = []
        schedule = schedule.lower()
        schedule = schedule.replace("(","")
        schedule = schedule.replace(")","")
        schedule = schedule.replace("*","l")
        shelist = schedule.split(',')
        tag = []
        dictobj = {}
        if room != '':
            rooms = room.split(',')
            for r in rooms:    
                for period in shelist:
                    if period != '':
                        period = period.split('/')
                        text = period[1] + period[0]
                        if text[-2] == "l":
                            classrooms.setdefault(r,[]).append(period[1]+"4")
                        classrooms.setdefault(r,[]).append(text)
                # print(f'room {r} is used by {cno} for {shelist}') 
        #print("\n")
        targetNumber = targetNumber + 1
    ela = getElaClassrooms()
    for k in ela.keys():
        period_list = ela[k]
        for p in period_list:
            classrooms.setdefault(k,[]).append(p)

    list_keys = list(classrooms.keys())
    sorted_list = sortList(list_keys)
    for t in sorted_list:
        filter_list = ""
        for time in classrooms[t]:
            filter_list = filter_list + time + " "
        
        print(f'<div class="classroom {filter_list}">\n\t{t}\n</div>')
    return resList

def sortList(l):
    l.sort()
    return l