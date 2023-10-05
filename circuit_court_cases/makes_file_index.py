import pandas as pd
import glob


def get_files(): 
    case_ids = pd.read_csv('/Users/e.schwartz/Documents/projects/freedom_suits/freedom_suits.csv')['case_id'].unique().tolist()
    df = pd.DataFrame(case_ids, index=range(len(case_ids)), columns=['case_ids'])
    df['xml_path'] = ''
    df['image_paths'] = ''
    print(df)

    for this_file in glob.glob("/Users/e.schwartz/Library/CloudStorage/Box-Box/dlps/dlps_digitalassets/Goldenseal-Staging/ccr/*[0-9]*.tif"):
        filename = this_file.split('/')[10].split('_')[0]
        this_id = find_case_id_img(filename, case_ids)

        try:
            i = df.index[df['case_ids'] == this_id.strip()].to_list()[0]
            df.at[i, 'image_paths'] += "dlps/dlps_digitalassets/Goldenseal-Staging/ccr/" + this_file.split('/')[10] + "||"

        except: AttributeError
    
    for this_file in glob.glob("/Users/e.schwartz/Library/CloudStorage/Box-Box/dlps/dlps_digitalassets/Goldenseal-Staging/ccr/*[0-9]*.xml"):
        filename = this_file.split('/')[10]
        this_id = find_case_id_xml(filename, case_ids)
        
        try:
            i = df.index[df['case_ids'] == this_id.strip()].to_list()[0]
            df.at[i, 'xml_path'] += "dlps/dlps_digitalassets/Goldenseal-Staging/ccr/" + this_file.split('/')[10]

        except: AttributeError
    df.to_csv("/Users/e.schwartz/Library/CloudStorage/Box-Box/scdps/scdps_services_projects/freedom_suits/ccr_file_locations.csv")


def find_case_id_xml(filename, case_ids):
    filename = filename.split('.')
    return str(filename[0]) + str(filename[1])



def find_case_id_img(filename, caseids): 
    for this_id in caseids:
        if filename in this_id:
            return this_id
        else: pass 


get_files()