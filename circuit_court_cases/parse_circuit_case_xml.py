import xml.etree.ElementTree as ET
import json 
import os 
import shutil
import csv
import pandas as pd

# how to use this
# first, locate the goldenseal staging directory containing all the circuit court cases
# next, run get_xml_files and enter the directory in os.listdir("/Users/e.schwartz/Library/CloudStorage/Box-Box/dlps/dlps_digitalassets/Goldenseal-Staging/ccr") 
# this will copy and save trhe xml files to a subdirectory in the same location called freedom_suits_xml
# next, navigate to oxygen xml editor. Click file, import/convert, additional conversions, xml to json. In the pop up window select add folder, and select the freedom_suits_xml folder. 
# in output folder, create an empty folder in the same directory as the xml folder called freedom_suits_json. Click run.
# After running this, the freedom_suits_json folder should contain json files. Naviagte back to this python script. Enter the name of the json folder in dir variable in main.
# run main. 
        


#  path to all the circuit court cases /Users/e.schwartz/Library/CloudStorage/Box-Box/dlps/dlps_digitalassets/Goldenseal-Staging/ccr
# extracts metadata for all xml files in the directory (dir)
def main():
    dir = "/Users/e.schwartz/Documents/projects/freedom_suits/freedom_suits_json/"
    cases_metadata = []
    for this_file in os.listdir(dir):
        uuid=  str(this_file.split('.')[0])+ str(this_file.split('.')[1])
        json_file =(dir + str(this_file))
        print(json_file)
        metadata = json_metadata_getter( json_file, uuid)
        print(metadata)
        cases_metadata.append(metadata)
    
    
    # makes_results_csv(cases_metadata, "/Users/e.schwartz/Documents/projects/freedom_suits/freedom_suits_metadata.csv")
    df=pd.DataFrame.from_dict(cases_metadata, orient='columns')
    df.to_csv('/Users/e.schwartz/Documents/projects/freedom_suits/freedom_suits.csv')



# moves all the .xml files in the goldenseal staging directory to their own file for bulk conversion to json (which is easier for elizabeth to parse)
def get_xml_files():
    xml_files = []
    for this_dir in os.listdir("/Users/e.schwartz/Library/CloudStorage/Box-Box/dlps/dlps_digitalassets/Goldenseal-Staging/ccr"):
        if 'xml' in this_dir:
            xml_files.append("/Users/e.schwartz/Library/CloudStorage/Box-Box/dlps/dlps_digitalassets/Goldenseal-Staging/ccr/" + str(this_dir))
    print('this is xml files', xml_files)
    for this_file in xml_files:
        print('----------------------------')
        print(this_file)
        shutil.copy(this_file, "/Users/e.schwartz/Documents/projects/freedom_suits/freedom_suits_xml")



def json_metadata_getter(json_file, uuid):
    with open(json_file, 'r', encoding= 'utf-8-sig') as f:
        data = json.load(f)
    try:
        caseDesc = data['teiCorpus']['teiHeader']['profileDesc'][0]['caseDesc']
    except KeyError:
        caseDesc = data['teiCorpus']['teiHeader']['profileDesc']['caseDesc']
    filing_date = {'dc_filing': '', 'text_filing': ''}
    term_date = {'dc_term': '', 'text_term': ''}
    if str(type(caseDesc['date'])) == "<class 'dict'>":
        if caseDesc['date']['type'] == 'filing':
                filing_date = get_filing_date(caseDesc['date'])
        elif caseDesc['date']['type'] == 'term':
                term_date = get_term_date(caseDesc['date'])
    else:
        for item in caseDesc['date']:
            if item['type'] == 'filing':
                filing_date = get_filing_date(item)
            elif item['type'] == 'term':
                term_date = get_term_date(item)
    parties = get_parties(caseDesc)
    cause_action = get_cause_action(caseDesc)
    judge = get_judge(caseDesc)
    attorneys = get_attorneys(caseDesc)
    return {
    'case_id': uuid,
    'title': get_case_title(caseDesc),
    'date_filing_dc': filing_date['dc_filing'],
    'date_filing_text': filing_date['text_filing'],
    'date_term_dc': term_date['dc_term'],
    'date_term_text': term_date['text_term'],
    'plaintiffs': parties['plaintiffs'],
    'defendants': parties['defendants'],
    'case_type': cause_action['case_type'],
    'cause_actions': cause_action['cause_actions'],
    'case_no': get_case_no(caseDesc),
    'court_type': get_court_type(caseDesc),
    'court_name': get_court_name(caseDesc),
    'judge_type': judge['judge_type'],
    'judge': judge['judge'],
    'justice_of_peace': get_justiceOfPeace(caseDesc)['justiceOfPeace'],
    'clerk': get_clerk(caseDesc),
    'sheriff': get_sheriff(caseDesc),
    'attorney_plaintiff': attorneys['plaintiff_attorneys'],
    'attorney_defendant': attorneys['defendant_attorneys'],
    'disposition': get_disposition(caseDesc),
    'related_case': get_relatedCase(caseDesc),
    'witnesses': get_witnesses(caseDesc)}


def get_witnesses(caseDesc): 
    try:
        return caseDesc['witness']
    except KeyError:
        return ''
    

def get_clerk(caseDesc):
    try:
        return caseDesc['clerk']
    except KeyError:
        return ''

# there are types of sheriffs- do we want to preserve that metadata or just extract names?
def get_sheriff(caseDesc):
    try:
        return caseDesc['sheriff']
    except KeyError:
        return ''

def get_court_name(caseDesc):
    try:
        return caseDesc['court']['#text']
    except TypeError:
        return caseDesc['court']

def get_court_type(caseDesc):
    try:
        return caseDesc['court']['type']
    except TypeError:
        return ''


def get_case_title(caseDesc):
    try:
        return caseDesc['caseTitle']
    except KeyError:
        return ''
      

def get_cause_action(caseDesc):
    cause_actions = []
    case_type = ''
    try: 
        if str(type(caseDesc['causeAction'])) == "<class 'dict'>":
            try:
                cause_actions.append(caseDesc['causeAction']['#text'])
            except KeyError: 
                cause_actions.append(caseDesc['causeAction'])
            try:
                case_type = caseDesc['causeAction']['type']
            except KeyError: pass
        elif str(type(caseDesc['causeAction'])) == "<class 'list'>":
            for action in caseDesc['causeAction']:
                try:
                    cause_actions.append(action['#text'])
                except KeyError: 
                    cause_actions.append(action)
                except TypeError:
                    cause_actions.append(action)
            try:
                case_type = caseDesc['causeAction'][0]['type']
            except KeyError: pass
            except TypeError: pass
        else:
            cause_actions.append(caseDesc['causeAction'])
    except KeyError: pass
    return {'cause_actions': cause_actions, 'case_type': case_type}



def get_case_no(caseDesc):
    try:
        return caseDesc['caseNo']
    except KeyError:
        return ''



def get_plaintiff(this_party):
    return this_party['#text']


def get_defendant(this_party):
    return this_party['#text']

def get_term_date(this_date):
    try:
        return {'dc_term': this_date['when'],
            'text_term': this_date['#text']}
    except KeyError:
        return {'dc_term': '',
            'text_term': ''}
# this doesn't make sense- there can be more than one judge dependent on type- presiding, appeal, etc. could make sense to add types like we do for attorneys
def get_judge(caseDesc):
    try:
        if str(type(caseDesc['judge'])) == "<class 'dict'>":
            return {'judge_type': caseDesc['judge']['type'],
               'judge': caseDesc['judge']['#text']}
        else:
            return {'judge_type': '', 'judge': caseDesc['judge']}
    except KeyError:
        return{'judge_type': '', 'judge': ''}

def get_justiceOfPeace(caseDesc):
    justice_of_peace = {'justiceOfPeace': ''}
    try:
        justice_of_peace['justiceOfPeace'] =  caseDesc['justiceOfPeace']
    except KeyError:
        pass
    return justice_of_peace
    
def get_filing_date(this_date):
    try:
        return {'dc_filing': this_date['when'],
                'text_filing': this_date['#text']}
    except KeyError: 
         return {'dc_filing': '',
                'text_filing': ''}
        
        
def get_attorneys(caseDesc):
    attorney_plaintiff = []
    attorney_defendant = []
    try:
        if str(type(caseDesc['attorney'])) == "<class 'dict'>":
            if caseDesc['attorney']['for'] == 'plaintiff':
                            try:
                                attorney_plaintiff.append(caseDesc['attorney']['#text'])
                            except KeyError:
                                attorney_plaintiff.append('')
            elif caseDesc['attorney']['for'] == 'defendant':
                            try:
                                attorney_defendant.append(caseDesc['attorney']['#text'])
                            except KeyError:
                                attorney_defendant.append('')
        else:
            for attorney in caseDesc['attorney']: 
                    if attorney['for'] == 'plaintiff':
                            try:
                                attorney_plaintiff.append(attorney['#text'])
                            except KeyError:
                                attorney_plaintiff.append('')
                    elif attorney['for'] == 'defendant':
                            try:
                                attorney_defendant.append(attorney['#text'])
                            except KeyError:
                                attorney_defendant.append('')
    except: KeyError
    return {'plaintiff_attorneys': attorney_plaintiff, 'defendant_attorneys': attorney_defendant}


def get_parties(caseDesc): 
    plaintiffs = []
    defendants = []
    others = []
    print(type(caseDesc['party']))
    try:
        if str(type(caseDesc['party'])) == "<class 'dict'>":
            print(caseDesc['party'].keys())
            if caseDesc['party']['role'] == 'plaintiff':
                try:
                    plaintiffs.append(caseDesc['party']['#text'])
                except KeyError: 
                    plaintiffs.append('')
                except TypeError:
                    print(caseDesc['party'])
                    plaintiffs.append('')
            elif caseDesc['party']['role'] == 'defendant':
                try:
                    defendants.append(caseDesc['party']['#text'])
                except KeyError:
                    defendants.append('')
        else:
            for party in caseDesc['party']:
                if party['role'] == 'plaintiff':
                    try:
                        plaintiffs.append(party['#text'])
                    except KeyError: 
                        plaintiffs.append('')
                elif party['role'] == 'defendant':
                    try:
                        defendants.append(party['#text'])
                    except KeyError:
                        defendants.append('')
                else:
                    print(party)
    except KeyError: 
        pass
    return {'plaintiffs': plaintiffs,
           'defendants': defendants}

def get_disposition(caseDesc):
    try:
        return caseDesc['disposition']
    except KeyError:
        return ''
    
def get_relatedCase(caseDesc):
    try:
        return caseDesc['relatedCase']
    except KeyError:
        return ''



 
main()
