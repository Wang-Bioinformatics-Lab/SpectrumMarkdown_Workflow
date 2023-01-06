import sys
import argparse
import pandas as pd
import markdown 
import uuid
import requests

parser = argparse.ArgumentParser(description='Doing some conversions')
parser.add_argument('input_filename')
parser.add_argument('output_markdown')
parser.add_argument('output_html')
parser.add_argument('output_images_folder')

args = parser.parse_args()

df = pd.read_csv(args.input_filename, sep="\t")
df["image_path"] = df["usi"].apply(lambda x: '{}/{}.svg'.format(args.output_images_folder, uuid.uuid4()))
#df["image"] = df["usi"].apply(lambda x: '![](https://metabolomics-usi.gnps2.org/svg/?usi1={})'.format(x))
df["image"] = df["image_path"].apply(lambda x: '![]({})'.format(x))

open(args.output_markdown, 'w').write(df.to_markdown(index=False))
open(args.output_html, "w").write(markdown.markdown(df.to_markdown(index=False), extensions=['tables']))

# TODO: Download all the images directly so we don't rely on server
for results_obj in df.to_dict(orient="records"):
    usi = results_obj["usi"]
    image_path = results_obj["image_path"]

    url = "https://metabolomics-usi.gnps2.org/svg/?usi1={}".format(usi)
    
    try:
        r = requests.get(url)
        open(image_path, "wb").write(r.content)
    except:
        pass


