from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from firebase import firebase
from multiprocessing.dummy import Pool as ThreadPool
import os

# HR_file_path = '/home/abheisenberg/PycharmProjects/CCCSchedule/stored_htmls/HRSource.txt'
# HE_file_path = '/home/abheisenberg/PycharmProjects/CCCSchedule/stored_htmls/HESource.txt'
# CC_file_path = '/home/abheisenberg/PycharmProjects/CCCSchedule/stored_htmls/CCSource.txt'

url = ['HR', 'CC', 'HE']


def crawl(url):

    if url is 'HR':
        crawl_hackerrank()
    elif url is 'HE':
        crawl_hackerearth()
    elif url is 'CC':
        crawl_codechef()


def crawl_hackerrank():

    driver_1 = webdriver.Firefox(executable_path='/app/geckodriver')

    # if not os.path.isfile(HR_file_path):
    # if os.stat(HR_file_path).st_size == 0:
    #     driver_1.get('https://www.hackerrank.com/contests')
    #
    #     print "Downloading page source of Hackerrank..."
    #
    #     page_source = driver_1.page_source
    #     with open(HR_file_path, 'w') as file_1:
    #         file_1.write(page_source.encode('utf8'))
    #     file_1.close()
    #
    # soup = BeautifulSoup(open(HR_file_path, 'r'), "lxml")

    driver_1.get('https://www.hackerrank.com/contests')
    page_source_1 = driver_1.page_source

    soup = BeautifulSoup(page_source_1, "lxml")

    active_contests = soup.find_all("div", class_="active_contests active-contest-container fnt-wt-600")

    hrfirebase = firebase.FirebaseApplication('https://competitivecontestsschedule.firebaseio.com/', None)
    hm = {}
    name_for_db = ""
    date_for_db = ""

    print "Crawling Hackerrank..."

    for each_active_contest in active_contests:
        li = each_active_contest.find_all("li", class_="contests-list-view mdB")

        for each_item in li:
            name = each_item.find("div", class_="contest-name head-col truncate txt-navy")
            if name is not None:
                print name.get_text(),
                name_for_db = name.get_text()
                print ': \t',
            else:
                continue

            date = each_item.find("time", class_="timeago")
            if date is not None:
                print date.get_text()
                date_for_db = date.get_text()
            else:
                print "Indefinite Timings"
                date_for_db = "Indefinite Timings"
            print date_for_db

            hm[name_for_db] = date_for_db

    result = hrfirebase.put('', 'hackerrank', hm)
    driver_1.close()
    # driver_1.quit()
    print "hackerrank result -> ",
    print result


def crawl_hackerearth():
    driver_2 = webdriver.Firefox(executable_path='/app/geckodriver')
    # if not os.path.isfile(HE_file_path):
    # if os.stat(HE_file_path).st_size == 0:
    #     print "Downloading page source of Hackerearth..."
    #
    #     driver_2.get('https://www.hackerearth.com/challenges/')
    #     page_source = driver_2.page_source
    #
    #     with open(HE_file_path, 'w') as file_2:
    #         file_2.write(page_source.encode('utf8'))
    #     file_2.close()
    #
    #     # driver_2.quit()
    #
    # soup = BeautifulSoup(open(HE_file_path), 'lxml')

    driver_2.get('https://www.hackerearth.com/challenges/')
    page_source_2 = driver_2.page_source

    soup = BeautifulSoup(page_source_2, "lxml")

    hefirebase = firebase.FirebaseApplication('https://competitivecontestsschedule.firebaseio.com/', None)
    name_for_db = ""
    date_for_db = ""
    type_for_db = ""

    print "Crawling Hackerearth..."

    all_upcoming_contests = soup.find_all("div", class_="challenge-card-modern")

    for each_contest in all_upcoming_contests:

        hm = {}
        challenge_name = each_contest.find("span", class_="challenge-list-title challenge-card-wrapper")
        challenge_time_left_if_active_now = each_contest.find("div", class_="date date-countdown")
        if challenge_time_left_if_active_now is not None:
            all_times = challenge_time_left_if_active_now.find_all("div", class_="inline-block large weight-600 dark")
            if len(all_times) is not 0:
                times = []
                for i in range(4):
                    line = all_times[i].get_text()
                    times.append(line)
                time_left = str(int(times[0]) * 10 + int(times[1])) + " days : " + str(
                    int(times[2]) * 10 + int(times[3])) + " hours "
                hm['time left'] = time_left

        challenge_date = each_contest.find("div", class_="date less-margin dark")
        challenge_type = each_contest.find("div", class_="challenge-type light smaller caps weight-600")

        if challenge_name is not None:
            name_for_db = challenge_name.get_text()
            hm['name'] = name_for_db
            print name_for_db,
        else:
            continue

        print " is on ",

        if challenge_date is not None:
            date_for_db = challenge_date.get_text()
            print date_for_db,
        else:
            date_for_db = "Active Now"
            print "right now",
            if hm.__contains__("time left"):
                print " time left -> " + hm['time left'],
        hm['date'] = date_for_db

        print ", Type: ",

        if challenge_type is not None:
            type_for_db = challenge_type.get_text().encode('utf').strip()
            print type_for_db
        else:
            type_for_db = "Unknown"
            print "~NA~"
        hm['type'] = type_for_db

        result = hefirebase.post('/hackerearth', hm)

        print "hackerearth result -> ",
        print result
    driver_2.close()


def crawl_codechef():
    driver_3 = webdriver.Firefox(executable_path='/app/geckodriver')
    # if not os.path.isfile(CC_file_path):
    # if os.stat(CC_file_path).st_size == 0:
    #     print "Downloading page source of Codechef"
    #
    #     driver_3.get('https://www.codechef.com/contests')
    #     page_source = driver_3.page_source
    #
    #     with open(CC_file_path, 'w') as file_3:
    #         file_3.write(page_source.encode('utf8'))
    #     file_3.close()
    #     driver_3.close()
    #     # driver_3.quit()
    #
    # soup = BeautifulSoup(open(CC_file_path), 'lxml')

    driver_3.get('https://www.codechef.com/contests')
    page_source_3 = driver_3.page_source

    soup = BeautifulSoup(page_source_3, "lxml")

    tables = soup.find_all("table", class_="dataTable")

    ccfirebase = firebase.FirebaseApplication('https://competitivecontestsschedule.firebaseio.com/', None)
    titles = ['contest_code', 'contest_name', 'start_time', 'end_time']
    hm = {}

    print "Crawling Codechef..."

    for i in range(2):
        table = tables.__getitem__(i)
        for rows in table.find_all("tr"):
            tds = rows.find_all("td")
            print '\n'
            print tds
            if len(tds) is not 0:
                for i in range(4):
                    td = tds[i]
                    hm[titles[i]] = td.get_text()
            result = ccfirebase.post('/codechef', hm)


# def delete_contents():
#     with open(HE_file_path, 'w') as file:
#         pass
#     file.close()
#     with open(HR_file_path, 'w') as file:
#         pass
#     file.close()
#     with open(CC_file_path, 'w') as file:
#         pass
#     file.close()

# delete_contents()

display = Display(visible=0, size=(800, 600))
display.start()

pool = ThreadPool(3)
results = pool.map(crawl, url)
pool.close()
pool.join()

# crawl_hackerrank()
