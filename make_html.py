#!python/bin/python

from jinja2 import Template
from make_popularity_graph import draw_graph, rank_by_year
from name_variance import get_names

def get_rank(name, gender):
    import sqlite3
    conn = sqlite3.connect('./data/names.db')
    db = conn.cursor()
    r2013 =db.execute("select rank from names where name = '%s' and gender='%s' and year=2013" % (name, gender)).fetchall() 
    if len(r2013) > 0:
        rank = r2013[0][0]
    else:
        rank = None
    qry = "select max(rank), min(rank) from names where name = '%s' and gender='%s'" % (name, gender)
    #print qry
    min, max = db.execute(qry).fetchall()[0]
    qry = "select year from names where name = '%s' and gender='%s' and rank='%s'" % (name, gender, min)
    #print qry
    min_year = db.execute(qry).fetchall()[0][0]
    qry = "select year from names where name = '%s' and gender='%s' and rank='%s'" % (name, gender, max)
    #print qry
    max_year = db.execute(qry).fetchall()[0][0]
    conn.commit()
    conn.close()
    return '2013 Rank (highest rank, lowest rank)', "%s (%s in %s, %s in %s)" % (rank, max, max_year, min, min_year)

def get_counts(name, gender):
    import sqlite3
    conn = sqlite3.connect('./data/names.db')
    db = conn.cursor()
    r2013 =db.execute("select n.count from names n where name ='%s' and gender='%s' and year=2013" % (name, gender)).fetchall() 
    if len(r2013) > 0:
        count = r2013[0][0]
    else:
        count = None
    max, min = db.execute("select max(count), min(count) from names where name = '%s' and gender='%s'" % (name, gender)).fetchall()[0]
    min_year = db.execute("select year from names where name = '%s' and gender='%s' and count='%s'" % (name, gender, min)).fetchall()[0][0]
    max_year = db.execute("select year from names where name = '%s' and gender='%s' and count='%s'" % (name, gender, max)).fetchall()[0][0]
    conn.commit()
    conn.close()
    return '2013 Count (highest count, lowest count)', "%s (%s in %s, %s in %s)" % (count, max, max_year, min, min_year)

def make_html(names, data_func):
    outnames = []
    for name, gender in names:
        print name
        header, data = data_func(name, gender)
        graph = draw_graph(rank_by_year(name, gender), name, gender)
        #graph = './images/%s-%s.png' % (name, gender)
        outnames += [(name, gender, data, graph)]
    print names
    with open('names.html') as f:
        template = Template(f.read())
    with open('names-output.html', 'w') as f:
        f.write(template.render(names=outnames, data_header=header))

if __name__ == '__main__':
    names = get_names('M')
    #names = [('Blaise', 'M')]
    #names = [
            #('Larkin', 'F'),
            #('Estelle', 'F'),
            #('Seraphina', 'F'),
            #('Ophelia', 'F'),
            #('Finley', 'F'),
            #('Clementine', 'F'),
            #('Aurelia', 'F'),
            #('Neva', 'F'),
            #('Annika', 'F'),
            #]
    #names = [
            #('tobin', 'M'),
            #('maddox', 'M'),
            #('charley', 'M'),
            #('oliver', 'M'),
            #('stanley', 'M'),
            #('wesley', 'M'),
            #('russell', 'M'),
            #('lamar', 'M'),
            #('leora', 'F'),
            #('aiyana', 'F'),
            #('cadence', 'F'),
            #('brooke', 'F'),
            #('brielle', 'F'),
            #('annika', 'F'),
            #('claire', 'F'),
            #('finley', 'F'),
            #('ruth', 'F'),
            #]
    make_html(names, get_rank)
    #make_html(names, get_counts)
