from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

# > seating numbers MIX
seating_nos = [*range(870000,870201,1),865231,868686,868682,
                481548,893538,387692,173148,234727,546254]

desk_nums = []
# student_names = []       # PLZ Keep hidden for privacy!
school_names = []
governorates = []
citys = []
assessment = []
Arabic_scores = []
F_1_scores = []
F_2_scores = []
biology_scores = []
geology_scores = []
chemistry_scores = []
physics_scores = []
total_scores = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    # > the target website
    page.goto('https://g12.emis.gov.eg')

    for seating_num in seating_nos:

        page.is_visible('div.allcom')
        page.fill('input#SeatingNo',str(seating_num))
        page.click('button[type=submit]')

        Ideal = page.is_hidden('div.text-center')
        # print(Ideal)

        # > permit only valid seating numbers (no page error promot)
        if Ideal == False:
            continue
        
        page.is_visible('div.col-lg-12.justify-content-center.section-title')

        # > read full html page
        html = page.inner_html('html')

        # > BeautifulSoup process
        soup = BeautifulSoup(html,'html.parser')

        # > student status (passed/failed)
        status = soup.select('.animate__animated.animate__fadeInDown')
      
        student_status = status[0].text
        if student_status == 'ناجـح':
            translated_status = 'Pass'
        else:
            translated_status = 'Fail'
        assessment.append(translated_status)

        # > student data
        student_details = soup.select('.p-data > table > tbody > tr td')

        desk_no = student_details[0].text
        desk_nums.append(desk_no)

        # > hiding student name is better than showing
        # student_name = student_details[1].text
        # student_names.append(student_name)

        school_name = student_details[2].text
        school_names.append(school_name)

        governorate = student_details[3].text
        governorates.append(governorate)

        city = student_details[4].text
        citys.append(city)

        # > student scores
        scores = soup.select('.p-details > table > tbody > tr > th:nth-of-type(2)')

        Arabic = float(scores[0].text)
        Arabic_scores.append(Arabic)

        F_1 = float(scores[1].text)
        F_1_scores.append(F_1)

        F_2 = float(scores[2].text)
        F_2_scores.append(F_2)

        biology = float(scores[3].text)
        biology_scores.append(biology)

        geology = float(scores[4].text)
        geology_scores.append(geology)

        chemistry = float(scores[5].text)
        chemistry_scores.append(chemistry)

        physics = float(scores[6].text)
        physics_scores.append(physics)

        total = float(scores[7].text)
        total_scores.append(total)

        # > To retart query for new desk number
        page.go_back()

natega_df = pd.DataFrame({'desk_no': desk_nums,
                        # 'student_name':student_names,
                        'school_name': school_names,
                        'directorate': governorates,
                        'neighborhood': citys,
                        'arabic':Arabic_scores, 
                        'first_forign_lang':F_1_scores, 
                        'second_forign_lang':F_2_scores,
                        'biology':biology_scores,
                        'geology':geology_scores,
                        'chemistry':chemistry_scores,
                        'physics':physics_scores,
                        'total_scores':total_scores,
                        'status':assessment
                        })

print(natega_df)

natega_df.to_csv('natega.csv',index=False)