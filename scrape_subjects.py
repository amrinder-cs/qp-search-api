import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

options = [ # got this from academics.gndec.ac.in/datesheet
    {"value": "1,14", "branch": "B.Tech.(Civil Engineering)"},
    {"value": "1,15", "branch": "B.Tech.(Computer Science and Engineering)"},
    {"value": "1,17", "branch": "B.Tech.(Electronics and Communication Engineering)"},
    {"value": "1,16", "branch": "B.Tech.(Electrical Engineering)"},
    {"value": "1,21", "branch": "B.Tech.(Information Technology)"},
    {"value": "1,30", "branch": "B.Tech.(Mechanical Engineering)"},
    {"value": "1,31", "branch": "B.Tech.(Production Engineering)"},
    {"value": "3,28", "branch": "MBA(Masters in Business Administration)"},
    {"value": "4,29", "branch": "MCA(Masters in Computer Application)"},
    {"value": "2,50", "branch": "M.Tech.(Computer Science and Engineering)"},
    {"value": "2,35", "branch": "M.Tech.(Electronics and Communication Engineering)"},
    {"value": "2,34", "branch": "M.Tech.(Electrical Engineering)"},
    {"value": "2,36", "branch": "M.Tech.(Environmental Science and Engineering)"},
    {"value": "2,37", "branch": "M.Tech.(Industrial Engineering)"},
    {"value": "2,43", "branch": "M.Tech.(Power Engineering)"},
    {"value": "2,44", "branch": "M.Tech.(Production Engineering)"},
    {"value": "2,45", "branch": "M.Tech.(Structural Engineering)"},
    {"value": "2,47", "branch": "M.Tech.(VLSI Design)"},
    {"value": "2,38", "branch": "M.Tech.(Information Technology)"},
    {"value": "2,76", "branch": "M.Tech.(Soil Mechanics and Foundation Engineering)"},
    {"value": "2,65", "branch": "M.Tech.(Geo Technical Engineering )"},
    {"value": "2,63", "branch": "M.Tech.(Energy Engineering)"},
    {"value": "2,41", "branch": "M.Tech.(Mechanical Engineering)"},
    {"value": "1,32", "branch": "B.Tech.(Mechanical (Production Engineering))"},
    {"value": "7,91", "branch": "BCA(Bachelor of Computer Applications)"},
    {"value": "1,151", "branch": "B.Tech.(Minor in Computer Science and Engineering)"},
    {"value": "2,39", "branch": "M.Tech.(Computer Science and Information Technology)"},
    {"value": "1,211", "branch": "B.Tech.(Minor in Information Technology)"},
    {"value": "1,171", "branch": "B.Tech.(Minor in Electronics and Communication Engineering)"},
    {"value": "1,161", "branch": "B.Tech.(Minor in Electrical Engineering)"},
    {"value": "10,96", "branch": "BBA(Bachelor of Business Administration)"},
    {"value": "9,97", "branch": "(Interior Design)"}
]

url = 'https://academics.gndec.ac.in/datesheet/'

for option in options:
    data = { # Inspect element'ed the request in chrome, in network tab. This was the payload
        'course_branch': option['value'],
        'full_part_time': 'Full Time',
        'datesheet_view_show': 'datesheet_view_show',
        'submit': ''
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tables = soup.find_all('table')
        
        for i, table in enumerate(tables):
            rows = []
            max_cols = 0
            for tr in table.find_all('tr'):
                row = [td.text.strip() for td in tr.find_all('td')]
                max_cols = max(max_cols, len(row))
                if row:
                    rows.append(row)
            
            rows = [row + [''] * (max_cols - len(row)) for row in rows]
            
            df = pd.DataFrame(rows)
            
            branch_name = re.sub(r'[^\w\s]', '', option['branch'])
            # Saving the CSV
            csv_filename = f"{branch_name}_table_{i+1}.csv"
            df.to_csv(csv_filename, index=False, header=False)  # Avoid writing headers, they caused errors
            print(f"Saved CSV file: {csv_filename}")
    else:
        print(f"Failed to fetch data for {option['branch']}. Status code:", response.status_code)
