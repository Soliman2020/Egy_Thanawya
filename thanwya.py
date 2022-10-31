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

            # > To retart query for new desk number
            page.go_back(timeout=0)

    natega_df = pd.DataFrame({'desk_no': desk_nums,
                            'school_name': school_names,
                            'directorate': directorates,
                            # 'neighborhood': citys,
                            # 'arabic':Arabic_scores, 
                            # 'first_forign_lang':F_1_scores, 
                            # 'second_forign_lang':F_2_scores,
                            # 'biology':biology_scores,
                            # 'geology':geology_scores,
                            # 'chemistry':chemistry_scores,
                            # 'physics':physics_scores,
                            # 'history':history_scores,
                            # 'geography':geography_scores,
                            # 'philosophy':philosophy_scores,
                            # 'psychology':psychology_scores,
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