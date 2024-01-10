import re
import xml.etree.ElementTree as etree
import os
import pandas as pd

def troubleshoot():
    text = xml_to_text("/Users/e.schwartz/Documents/projects/freedom_suits/freedom_suits_xml/ccr1805.26134.004.xml")
    print(text)


def main():
    dir = '/Users/e.schwartz/Documents/projects/freedom_suits/freedom_suits_xml/'
    results = []
    errors = []
    for this_file in os.listdir(dir):
        uuid=  str(this_file.split('.')[0])+ str(this_file.split('.')[1])
        print(uuid)
        try:
            text = xml_to_text(dir + this_file)
            results.append({'case_id': uuid,
                            'transcript': text})
        except IndexError:
            errors.append(uuid)
        except etree.ParseError: 
            pass
    df = pd.DataFrame(data=results)
    print(errors)

    df.to_csv('/Users/e.schwartz/Library/CloudStorage/Box-Box/scdps/scdps_services_projects/freedom_suits/ccr_flat_files/ccr_transcriptions.csv')
    

def xml_to_text(xml_path):
    # so this is fine but it brings in the metadata with it- we only want the stuff in TEI text
    text = xml_reader(xml_path)
    text = re.sub("<.*?>", "", text)
    text = re.sub('\n', '', text)
    text = re.sub(' +', ' ', text)
    text = re.sub('&amp;', '&', text)
    text = re.sub( "%NEW_DOC%", '\n', text)
    return text
    # with open('/Users/e.schwartz/Documents/projects/freedom_suits/testing_text.txt', 'w') as outfile:
    #     print(text, file=outfile)

def xml_reader(file_path):
    tree = etree.parse(file_path)
    root = tree.getroot()
    items = len(root)
    i = 1
    
    as_str = ""
    print(items)
    for thing in range(len(root) -1):
        print(i)
        this_str = etree.tostring(root[i][1][0]).decode('utf-8') + "%NEW_DOC%"
        # as_str += etree.tostring(root[i][1][0], encoding='utf-8').decode('utf-8')
        as_str += this_str
        i +=1
    return as_str
    

main()
# troubleshoot()