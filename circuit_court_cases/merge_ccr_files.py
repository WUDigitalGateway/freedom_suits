import pandas as pd

def main():
    metadata = pd.read_csv("/Users/e.schwartz/Library/CloudStorage/Box-Box/scdps/scdps_services_projects/freedom_suits/ccr_flat_files/ccr_metadata_revised.csv")
    file_locs = pd.read_csv("/Users/e.schwartz/Library/CloudStorage/Box-Box/scdps/scdps_services_projects/freedom_suits/ccr_flat_files/ccr_file_locations.csv")[['case_id', 'xml_path', 'image_paths']]
    transcripts = pd.read_csv("/Users/e.schwartz/Library/CloudStorage/Box-Box/scdps/scdps_services_projects/freedom_suits/ccr_flat_files/ccr_transcriptions.csv")[['case_id', 'transcript']]
    files_and_metadata = pd.merge(metadata, file_locs, on='case_id', how='outer')
    ccrs = pd.merge(files_and_metadata, transcripts, on='case_id', how='outer')
    ccrs.to_csv("/Users/e.schwartz/Library/CloudStorage/Box-Box/scdps/scdps_services_projects/freedom_suits/ccr_flat_files/ccr_records.csv")

main()