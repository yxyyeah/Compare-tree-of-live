'''open tree of life
OpenTree API'''
import re
from opentree import ot_object as ot

m = ot.OpenTree()
#search for unambiguous name
a_name = input('a: ')
b_name = input('b: ')
result = m.tnrs_autocomplete(a_name)
a_choice = {i['unique_name'] for i in result.response_dict}
result = m.tnrs_autocomplete(b_name)
b_choice = {i['unique_name'] for i in result.response_dict}
if len(a_choice) != 1 and a_name.title() not in a_choice:
    print('a_name has mutiple search results')
    for i in a_choice:
        print(i)
    a_name = input('Enter full name to match: ')
if len(b_choice) != 1 and b_name.title() not in b_choice:
    print('b_name has mutiple search results')
    for i in b_choice:
        print(i)
    b_name = input('Enter full name to match: ')
#match name with ottid
a = m.get_ottid_from_name(a_name.strip().title())
a_lineage = []
b = m.get_ottid_from_name(b_name.strip().title())
b_lineage = []
#search for lineage
info = m.taxon_info(ott_id=a,include_lineage=True)
for i in info.response_dict['lineage']:
    name = i['unique_name']
    name = re.sub(r' \([\w ]*\)','',name)
    a_lineage.insert(0,name+' ('+i['rank']+')'if i['rank']!='no rank' else name)
name = info.response_dict['unique_name']
rank = info.response_dict['rank']
a_lineage.append(re.sub(r' \([\w ]*\)','',name)+' ('+rank+')' if rank!='no rank' else name)
info = m.taxon_info(ott_id=b,include_lineage=True)
for i in info.response_dict['lineage']:
    name = i['unique_name']
    name = re.sub(r' \([\w ]*\)','',name)
    b_lineage.insert(0,name+' ('+i['rank']+')'if i['rank']!='no rank' else name)
name = info.response_dict['unique_name']
rank = info.response_dict['rank']
b_lineage.append(re.sub(r' \([\w ]*\)','',name)+' ('+rank+')' if rank!='no rank' else name)
#search for mrca
mrca = m.taxon_mrca(ott_ids=[a,b])
mrca = mrca.response_dict['mrca']
name = mrca['unique_name']
rank = mrca['rank']
mrca = re.sub(r' \([\w ]*\)','',name)
mrca = mrca+' ('+rank+')' if rank!='no rank' else mrca
mrca_index = a_lineage.index(mrca)

#print tree
a_len = len(a_lineage)
b_len = len(b_lineage)
if a_len >= b_len:
    for i in range(a_len):
        if i <= mrca_index:
            print('{:^80}'.format(a_lineage[i]))
        elif i < b_len:
            print('{:^40}{:^40}'.format(a_lineage[i],b_lineage[i]))
        else:
            print('{:^40}'.format(a_lineage[i]))
else:
    for i in range(b_len):
        if i <= mrca_index:
            print('{:^80}'.format(a_lineage[i]))
        elif i < a_len:
            print('{:^40}{:^40}'.format(a_lineage[i],b_lineage[i]))
        else:
            print('{:^40}{:^40}'.format('',b_lineage[i]))

input()