import os
import pandas as pd
import pypdf
from PIL import Image, ImageSequence

def main():
    file_locations = pd.read_csv('/Users/e.schwartz/Library/CloudStorage/Box-Box/scdps/scdps_services_projects/freedom_suits/ccr_flat_files/ccr_file_locations.csv')

    box_dir = '/Users/e.schwartz/Library/CloudStorage/Box-Box/'

    images = file_locations.loc[file_locations['case_id']=='ccr185006891']['image_paths'].tolist()[0].split('||')
    i = 0
    for this_image in images:
        tiff_to_pdf(tiff_path=box_dir+this_image, case_id='ccr185006891', file_number=i)
        i += 1






# from stackoverflow user Nori 7/11/2021
def tiff_to_pdf(tiff_path: str, case_id, file_number) -> str:

 
    pdf_path = '/Users/e.schwartz/Documents/projects/freedom_suits/freedom_suits_experiments/'+ str(case_id) + str(file_number) + '.pdf'
    if not os.path.exists(tiff_path): raise Exception(f'{tiff_path} does not find.')
    image = Image.open(tiff_path)

    images = []
    for i, page in enumerate(ImageSequence.Iterator(image)):
        page = page.convert("RGB")
        images.append(page)
    if len(images) == 1:
        images[0].save(pdf_path)
    else:
        images[0].save(pdf_path, save_all=True,append_images=images[1:])
    return pdf_path

main()