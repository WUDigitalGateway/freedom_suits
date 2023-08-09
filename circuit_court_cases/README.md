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
- you will need a directory (folder) containing the circuit court cases available at:
- you will also need to install Oxygen XML editor

## how can I run this? 
