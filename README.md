# freedom_suits
A repository containing scripts for remediating and migrating XML from the freedom suits to sustain its future use

## Background:
These python  scripts create flat files for the circuit court records project. The original project consisted of
scanned page images for each court record and custom-encoded XML files. The generated flat
files consist of the metadata for each case and the locations of the page-images and
xml files.

## Metadata Fields
Each case has a unique case_id that starts with the string ‘ccr’ followed by the 4 digit
year in which the case was file, followed by 5 unique digits, I.e., ccrYYYY00000. For
example, ccr185006891.

These case_ids should be used to identify a record across the csv files.
The flat files were generated using the python scripts in:
https://github.com/WUDigitalGateway/freedom_suits/tree/main
ccr_metadata.csv details the metadata encoded into the xml files for each case_id.

The fields include:
- case_id: the unique identifier for the record
- title: the title of the case as encoded by the Legal Encoded team
- date_filing_dc: the date the case was filed in Dublin core format (YYYY-MM-DD)
- date_filing_text: the filing date as a text field (i.e., April 15, 1825)
- date_term_dc: the term of the court in Dublin core format (YYYY-MM)
- date_term_text: the term of the court as a text field (i.e., April Term, 1851)
- plaintiffs: a list of the people named as plaintiffs in the case
- defendants: a list of the people named as defendants in the case
- case_type: the type of case (i.e., civil vs. criminal vs. appellate)
- cause_actions: a list of the legal claims that allow a party to seek judicial relief (i.e.,
Trespass)
- case_no: the case number
- court_type: the type of court the case was held in i.e., state vs. territorial
- court_name: the name of the court the case took place in
- judge_type: the type of judge (i.e., presiding, trial)
- judge: the judge of the trial
- justice_of_peace: the justice of the peace for the case or a list of justices of peace
- clerk: the clerk or list of clerks for the case
- sheriff: the sheriff or a list of sheriffs for the case
- attorney_plaintiff: the attorney or a list of attorneys for the plaintiff
- attorney_defendant: the attorney or a list of attorneys for the defendant
- disposition: summary of what happened at the trial
- related_case: a case or list of cases related to the record
- witnesses: a witness or list of witnesses for the case

## Python Scripts:

### parses_circuit_case_xml.py*: 
generates 1 csv file wherein each row maps to one circuit court case and the columns represent metadata fields extracted from the xml file.
https://github.com/WUDigitalGateway/freedom_suits/blob/c952e5758e52cf08c51b9a3c6
0e0924c0c77edbb/circuit_court_cases/parse_circuit_case_xml.py



### make_file_index.py:
Generates 2 csv files. **ccr_file_locations.csv** details the xml file location and the image files locations for
each case. These can be located in WashU’s box at the pathways provided. The image file paths are separated by ‘||’ such that there may be multiple image files in one image_paths cell separated by ‘||’ :
https://github.com/WUDigitalGateway/freedom_suits/blob/c952e5758e52cf08c51b9a3c6
0e0924c0c77edbb/circuit_court_cases/makes_file_index.py

Additionally, make_file_index creates **file_error_report.csv**: A csv file of all files where the number of files that match the
case ID differs from the number specified in the xml title. Includes explanations of the
discrepancy. Most of these files produce errors because the file naming convention for
the images in the Dred Scott cases differs from the ccr cases. Others have
discrepancies because there are duplicate pages scans or because page scan files
corrupted

### tifs-to-pdf.py
Ingests the file location csv file, ccr_file_locations.csv, converts the tifs to pdfs, merges the pdf files, and saves them to a location in box. Use these file paths and metadata to bulk upload items to IA. 

### makes_plain_text.py
Parses an xml file of a circuit court case and returns it as a plain text string. Creates a csv file containing the transcript for each case.

### merge_ccr_files.py
Merges the metadata csv file, the file locations csv file, and the plain text csv file by merging them on the case_id field. 

