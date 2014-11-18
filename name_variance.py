#!python/bin/python
import sqlite3
import pickle
import numpy as np
import csv
from scipy import stats

conn = sqlite3.connect('./data/names.db')
db = conn.cursor()
#MIN_YEAR=1880
MIN_YEAR=1960
MAX_YEAR=2014
def get_names(gender):
    #if True:
    if False:
        all_names = set()
        name_years = {}
        name_counts = {}
        final_names = {}
        rank_2010 = {}
        indices_data_present = {}
        STEP = 4
        for i, min_year in enumerate(range(MIN_YEAR, MAX_YEAR+1, STEP)):
            max_year = min_year + STEP
            if max_year > MAX_YEAR: max_year = MAX_YEAR
            #query = '''
                    #select distinct name, avg(rank) as a from names where length(name)<7 and year>=%s and year<%s and gender='F' group by name having a > 500;
                    #''' % (min_year, max_year)
            query = '''
                    select distinct name, avg(rank), avg(count) as a from names where year>=%s and year<%s and gender='%s' group by name;
                    ''' % (min_year, max_year, gender)
            print query
            for name, rank, count in db.execute(query):
                if min_year == 2010:
                    rank_2010[name] = rank
                if name in all_names:
                    name_years[name] += [min_year]
                    final_names[name] += [rank]
                    indices_data_present[name] += [i]
                    name_counts[name] += [count]
                    #if name in final_names:
                        #running_avg = final_names[name]
                        #if abs(rank - running_avg) > (running_avg * 0.25):
                            #del(final_names[name])
                        #else:
                            #final_names[name] = ((running_avg * i) + rank) / (i+1)
                else:
                    all_names.add(name)
                    indices_data_present[name] = [i]
                    name_years[name] = [min_year]
                    name_counts[name] = [count]
                    final_names[name] = [rank]
        with open('./pickle/final_names-%s' % gender, 'w') as f:
            pickle.dump(final_names, f)
        with open('./pickle/name_years-%s' % gender, 'w') as f:
            pickle.dump(name_years, f)
        with open('./pickle/rank_2010-%s' % gender, 'w') as f:
            pickle.dump(rank_2010, f)
        with open('./pickle/indices_data_present-%s' % gender, 'w') as f:
            pickle.dump(indices_data_present, f)
        with open('./pickle/name_counts-%s' % gender, 'w') as f:
            pickle.dump(name_counts, f)
    with open('./pickle/final_names-%s' % gender) as f:
        final_names = pickle.load(f)
    with open('./pickle/name_years-%s' % gender) as f:
        name_years = pickle.load(f)
    with open('./pickle/rank_2010-%s' % gender) as f:
        rank_2010 = pickle.load(f)
    with open('./pickle/indices_data_present-%s' % gender) as f:
        indices_data_present = pickle.load(f)
    with open('./pickle/name_counts-%s' % gender) as f:
        name_counts = pickle.load(f)

    # for correlation
    comp_name = 'Russell'
    comp_set = set(name_years[comp_name])
    comp_ranks = final_names[comp_name]

    for name, years in name_years.iteritems():
        if name in final_names:
            if len(years) < 9:
                del(final_names[name])
                continue
            #min_rank = min(final_names[name])
            #max_rank = max(final_names[name])

            # stdev
            #stdev = np.std(name_counts[name])
            #print stdev
            #if stdev > 100 or min(name_counts[name]) < 100:
                #del(final_names[name])

            # correlation
            name_set = set(name_years[name])
            inter = comp_set.intersection(name_set)
            compdata = [comp_ranks[(name_years[comp_name].index(i))] for i in inter]
            namedata = [final_names[name][name_years[name].index(i)] for i in inter]
            corrcoef = np.corrcoef(compdata, namedata)[0][1]
            if corrcoef < 0.993 or np.isnan(corrcoef) or len(inter) < 5:
                del(final_names[name])

            # linear reg
            #slope, icpt, rval, pval, err = stats.linregress(indices_data_present[name], final_names[name])
            #print slope
            #if slope < -1000 or slope > -100 or name[0].lower() != 'd':
            #if slope > 100 or slope < 90:
                #del(final_names[name])
            #if max_rank - min_rank < 
            #else:
                #print name
    try:
        names = []
        for name, rank in final_names.iteritems():
            names.append((int(np.mean(rank)), name))
        with open('variance_names.csv', 'w') as f:
            w = csv.writer(f)
            w.writerow(['Name', 'Avg rank', '2010s rank', 'Decades', 'Counts'])
            for rank, name in sorted(names):
                r2010 = rank_2010[name] if rank_2010.has_key(name) else "N/A"
                w.writerow([name, rank, r2010, name_years[name], name_counts[name]])
                #f.write('%s - %s (%s)\n' % (rank, name, name_years[name]))
        return [(name[1], gender) for name in names]
    except Exception, e:
        import traceback
        traceback.print_exc()
        import pdb; pdb.set_trace()
if __name__ == '__main__':
    get_names('M')
    #conn.commit()
    conn.close()
