#!python/bin/python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('./data/names.db')
db = conn.cursor()

START_YEAR=1900
END_YEAR=2014

US_POP = [76.09, 77.58, 79.16, 80.63, 82.17, 83.82, 85.45, 87.01, 88.71, 90.49, 92.41, 93.86, 95.34, 97.23, 99.11, 100.55, 101.96, 103.27, 103.21, 104.51, 106.46, 108.54, 110.05, 111.95, 114.11, 115.83, 117.40, 119.04, 120.51, 121.77, 123.08, 124.04, 124.84, 125.58, 126.37, 127.25, 128.05, 128.82, 129.82, 130.88, 132.12, 133.40, 134.86, 136.74, 138.40, 139.93, 141.39, 144.13, 146.63, 149.19, 152.27, 154.88, 157.55, 160.18, 163.03, 165.93, 168.90, 171.98, 174.88, 177.83, 180.67, 183.69, 186.54, 189.24, 191.89, 194.30, 196.56, 198.71, 200.71, 202.68, 205.05, 207.66, 209.90, 211.91, 213.85, 215.97, 218.04, 220.24, 222.58, 225.06, 227.22, 229.47, 231.66, 233.79, 235.82, 237.92, 240.13, 242.29, 244.50, 246.82, 249.62, 252.98, 256.51, 259.92, 263.13, 266.28, 269.39, 272.65, 275.85, 279.04, 282.16, 284.97, 287.63, 290.11, 292.81, 295.52, 298.38, 301.23, 304.09, 306.77, 309.33, 311.59, 313.91, 316.16]

def normalized_count(name, gender):
    query = '''
    SELECT year, count FROM names WHERE year>=1900 AND name like '%s' AND gender='%s' ORDER BY year;
    ''' % (name, gender)
    data = []
    for i, (year, count) in enumerate(db.execute(query)):
        data.append(count / US_POP[i])
    return data

def rank_by_year(name, gender):
    query = '''
    SELECT year, rank FROM names WHERE name like '%s' AND gender='%s' ORDER BY year;
    ''' % (name, gender)
    data = []
    for i, (year, rank) in enumerate(db.execute(query)):
        data.append(-rank)
        #print year, rank
    return data

def draw_graph(data, name, gender):
    fig = plt.figure(figsize=(1,0.5), dpi=72, frameon=False)
    #fig, ax = plt.subplots()
    plt.plot(data)
    fig.patch.set_visible(False)
    plt.axes().get_xaxis().set_visible(False)
    plt.axes().get_yaxis().set_visible(False)
    fname = "./images/%s-%s.png" % (name, gender)
    plt.savefig(fname, format='png')
    plt.cla()
    return fname

if __name__ == '__main__':
    name = 'Finley'
    gender = 'F'
    #count = normalized_count(name, gender)
    rank = rank_by_year(name, gender)
    draw_graph(rank, name, gender)
