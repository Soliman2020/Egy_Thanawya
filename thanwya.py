from __future__ import division
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time


while True:
   try:
       start = int(input('Enter a start seating num in range 100000-999999 >>> '))
   except ValueError:
       print ("That's not a number!")
   else:
       if 100000 <= start < 999999:
           size = int(input('Please enter how many iterations you want to get >>> ')) 
           last = start + size + 1
           print('processing, please wait...')
           break
       else:
           print ('Out of range. Try again')


# > seating numbers MIX
seating_nos = [*range(start,last,1)]

# seating_nos = [*range(870000,870101,1)]
# seating_nos = [865231,868686,868682,481548,893538,387692,173148,234727,546254]

desk_nums = []
percentages = []
# student_names = []       # PLZ Keep hidden for privacy!
school_names = []
directorates = []
citys = []
assessment = []
divisions = []
Arabic_scores = []
F_1_scores = []
F_2_scores = []
pure_mathematics = []
history_scores = []
geography_scores = []
philosophy_scores = []
psychology_scores = []
chemistry_scores = []
biology_scores = []
geology_scores = []
applied_math = []
physics_scores = []
total_scores = []


def core():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # > the target website
        page.goto('https://natega.cairo24.com/', timeout = 0)

        for seating_num in seating_nos:
            page.is_visible('div.all')
            time.sleep(1)
            page.fill('input#seating_no',str(seating_num))
            page.click('input#submit')

            Ideal = page.is_hidden('center.field-validation-valid:nth-child(3)')
            print(Ideal)

            # > permit only valid seating numbers (no page error promot)
            if Ideal == False:
                continue
            
            # > read full html page
            html = page.inner_html('html')

            # > BeautifulSoup process
            soup = BeautifulSoup(html,'html.parser')

            # > student status
            desk_no = soup.select('li.col:nth-child(1)>h1')[0].text
            desk_nums.append(desk_no)

            total = soup.select('li.col:nth-child(2)>h1')[0].text
            total_scores.append(total)            

            percentage = soup.select('li.col:nth-child(3)>h1')[0].text
            # percentage_value = percentage_loc[0].text
            percentages.append(percentage)

            school_name = soup.select('.full-result > ul:nth-child(1) > li:nth-child(2) > span:nth-child(2)')[0].text
            school_names.append(school_name)

            directorate = soup.select('.full-result > ul:nth-child(1) > li:nth-child(3) > span:nth-child(2)')[0].text
            directorates.append(directorate)

            status = soup.select('.full-result > ul:nth-child(1) > li:nth-child(5) > span:nth-child(2)')[0].text.strip()
            assessment.append(status)

            division = soup.select('.full-result > ul:nth-child(1) > li:nth-child(7) > span:nth-child(2)')[0].text
            divisions.append(division)

            page.is_visible('.RightSide2')

            arabic = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > span:nth-child(2)')[0].text
            Arabic_scores.append(arabic)

            foreign_1 = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(2) > span:nth-child(2)')[0].text
            F_1_scores.append(foreign_1)

            foreign_2 = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(3) > span:nth-child(2)')[0].text
            F_2_scores.append(foreign_2)

            pm = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(4) > span:nth-child(2)')[0].text
            pure_mathematics.append(pm)

            history = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(5) > span:nth-child(2)')[0].text
            history_scores.append(history)

            geo = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(6) > span:nth-child(2)')[0].text
            geography_scores.append(geo)

            philo = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(7) > span:nth-child(2)')[0].text
            philosophy_scores.append(philo)

            psych = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(8) > span:nth-child(2)')[0].text
            psychology_scores.append(psych)

            chemistry = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(9) > span:nth-child(2)')[0].text
            chemistry_scores.append(chemistry)

            biology = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(10) > span:nth-child(2)')[0].text
            biology_scores.append(biology)

            geology = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(11) > span:nth-child(2)')[0].text
            geology_scores.append(geology)

            am = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(12) > span:nth-child(2)')[0].text
            applied_math.append(am)

            physics = soup.select('div.result-details:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(13) > span:nth-child(2)')[0].text
            physics_scores.append(physics)

            # > To retart query for new desk number
            page.go_back(timeout=0)

    natega_df = pd.DataFrame({'desk_no': desk_nums,
                            'school_name': school_names,
                            'directorate': directorates,
                            'arabic':Arabic_scores, 
                            'first_foreign_lang':F_1_scores, 
                            'second_foreign_lang':F_2_scores,
                            'pure_mathematics':pure_mathematics,
                            'history':history_scores,
                            'geology':geology_scores,
                            'philosophy':philosophy_scores,
                            'psychology':psychology_scores,
                            'chemistry':chemistry_scores,
                            'biology':biology_scores,
                            'geography':geography_scores,
                            'applied_math':applied_math,
                            'physics':physics_scores,
                            'division':divisions,
                            'total_scores':total_scores,
                            'percentage':percentages,
                            'status':assessment
                            })

    print(natega_df)

    natega_df.to_csv(f'natega_valid_range_{start}_to_{last-1}.csv',index=False)

    print('Results are ready, check the output CSV file.')

def main():
    core()

if __name__ == '__main__':
    main()