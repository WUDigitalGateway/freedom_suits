# Circuit Court Cases
## what are these? 
As part of the Freedom Suits Project, WashU, the Missouri History Museum, the St. Louis Circuit Court, and the Missouri State Archivist worked together to digitize circuit court case records from approximately the Louisana Purchase to 1860. These cases are encoded in a custom TEI schema developed in collaboration with the WashU Law Library. Encoded in the TEI are a number of legal-related metadata fields that hold the potential to make these cases searchable for legal historians. 

## why make this github repo?
The scripts contained within this github repository aim to extract the TEI encoded metadata fields from the XML to make the documents searchable even in the absence of a database. While the future of the project (that's currently hosted on DLSX) remains unknown, the hope is that these metadata csv files can enable use of the records beyond the existence of the live website and ultimately facilitate the creation of a new web home for the project. 

## what's in this repository?
Currently, the repository contains 2 files
- parse_circuit_court_cases.py : a python script to convert xml to json, extract metadata from the json document, and write those fields to a csv file for easier viewing/searching
- circuit_court_cases.csv : the csv file that parse_circuit_court_cases.py produces

## what other files/software do I need to run this: 
- you will need a directory (folder) containing the circuit court case json files available at: https://wustl.box.com/s/2adu9hi66etmwhta1nmstj6r4mgxe317 note that these were created using the get_xml() function in parse_circuit_court_xml.py. That function copies all the xml files from the ccr directory in box to their own folder. Next, that folder was run through Oxygen XML's XML to JSON converter. The produced json files are those in the supplied box folder.
- You also need a Python environment with the libraries json, os, shutil, and pandas
  

## how can I run this? 
- After downloading the circuit court json records, installing Python and the dependent libraries, and this github repo, navigate to parse_circuit_court_xml.py and run it.
- When prompted, enter the path to the json records you just downloaded in the prompt. It will look something like "/Users/[your username]/Desktop/circuit_court_json/
- Next, you will be asked to enter the path to where you'd like to save the csv file. This should look something like: "/Users/[your username]/Desktop/circuit_court_metadata.csv"
- Now the python script will extract all the metadata fields from each json file and write them to the csv file. Once the program finishes, you can access the csv file. 

## what are the next steps?
- Right now, we are ignoring the complexity of different sherrif and judge types- we may want to extract that information. To do so, we'd need to introduce many new metadata fields
- 
