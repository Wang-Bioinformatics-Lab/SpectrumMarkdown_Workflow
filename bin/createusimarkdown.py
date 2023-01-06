import sys
import argparse
import pandas as pd
import markdown

parser = argparse.ArgumentParser(description='Doing some conversions')
parser.add_argument('input_filename')
parser.add_argument('output_markdown')
parser.add_argument('output_html')
parser.add_argument('output_images_folder')

args = parser.parse_args()

df = pd.read_csv(args.input_filename, sep="\t")
df["image"] = df["usi"].apply(lambda x: '![](https://metabolomics-usi.gnps2.org/svg/?usi1={})'.format(x))

open(args.output_markdown, 'w').write(df.to_markdown(index=False))
open(args.output_html, "w").write(markdown.markdown(df.to_markdown(index=False), extensions=['tables']))

# TODO: Download all the images directly so we don't rely on server