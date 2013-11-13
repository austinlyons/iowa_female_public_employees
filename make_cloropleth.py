## Making an Iowa cloropleth map using Python
## Namely, plotting percentage of public employees that are female in each county
# imports
import pandas as pd
import numpy as np
from BeautifulSoup import BeautifulSoup

# implement county->fips lookup table with a dataframe with the county as the index
fips = pd.read_csv('iowa_county_fips.csv', index_col=0)

# Iowa public employees dataframe: % female, % male, total # employees. County is set as the index
iowa_by_sex = pd.read_csv('iowa_public_employees_female_male_ratio.csv', index_col=0)

# add code column to our iowa dataframe
iowa_by_sex['code'] = fips['code'].astype(int)

# load the blank Iowa SVG
svg = open('iowa_counties.svg', 'r').read()

# parse SVG, defining selfClosingTags as shown here: https://josephhall.org/nqb2/index.php/flwdchrplth
soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])

# find counties using findAll
paths = soup.findAll('path')

# The map colors in order from lightest to darkest
colors = ['#F1EEF6', '#D0D1E6', '#A6BDDB', '#74A9CF', '#2B8CBE', '#045A8D']

# county base style. We'll add the fill color (at the end of this string) for each county path
path_style="font-size:12px;fill-rule:nonzero;stroke:#000000;stroke-width:0.1;stroke-linecap:butt;stroke-linejoin:bevel;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;marker-start:none;fill:"

# Color the counties based on percent of public employees that are female
for p in paths:
 
    if p['id'] not in ["State_Lines", "separator"]: # only color the counties
        try:
            rate = iowa_by_sex[iowa_by_sex['code'] == int(p['id'])]['F']
        except:
            continue
 
        if rate > 0.833:
            color_class = 5
        elif rate > 0.666:
            color_class = 4
        elif rate > 0.5:
            color_class = 3
        elif rate > 0.333:
            color_class = 2
        elif rate > 0.166:
            color_class = 1
        else:
            color_class = 0
 
        color = colors[color_class]
        p['style'] = path_style + color

# Save result
fo = open("iowa_counties_colored.svg", "wb")
fo.write(soup.prettify());
fo.close()
