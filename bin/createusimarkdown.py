import sys
import argparse
import pandas as pd
import markdown 
import uuid
import requests

def main():

    parser = argparse.ArgumentParser(description='Doing some conversions')
    parser.add_argument('input_filename')
    parser.add_argument('output_markdown')
    parser.add_argument('output_html')
    parser.add_argument('output_images_folder')

    args = parser.parse_args()

    df = pd.read_csv(args.input_filename, sep="\t")
    df["image_path"] = df["usi"].apply(lambda x: '{}/{}.svg'.format(args.output_images_folder, uuid.uuid4()))
    df["image"] = df["image_path"].apply(lambda x: '![]({})'.format(x))

    for results_obj in df.to_dict(orient="records"):
        usi = results_obj["usi"]
        if "usi2" in results_obj:
            usi2 = results_obj["usi2"]
        else:
            usi2 = None
        
        image_path = results_obj["image_path"]

        params = {}

        if usi2 is not None:
            url = "https://metabolomics-usi.gnps2.org/svg/mirror/".format(usi, usi2)
            params["usi1"] = usi
            params["usi2"] = usi2
        else:
            url = "https://metabolomics-usi.gnps2.org/svg/".format(usi)
            params["usi1"] = usi

        if "mz_max" in results_obj:
            params["mz_max"] = results_obj["mz_max"]

        if "mz_min" in results_obj:
            params["mz_min"] = results_obj["mz_min"]

        if "max_intensity" in results_obj:
            params["max_intensity"] = results_obj["max_intensity"]
        
        try:
            r = requests.get(url, params=params)
            open(image_path, "wb").write(r.content)
        except:
            pass

    # drop image_path
    df = df.drop(columns=["image_path"])

    if "mz_max" in df.columns:
        df = df.drop(columns=["mz_max"])

    if "mz_min" in df.columns:
        df = df.drop(columns=["mz_min"])

    if "max_intensity" in df.columns:
        df = df.drop(columns=["max_intensity"])


    open(args.output_markdown, 'w').write(df.to_markdown(index=False))
    open(args.output_html, "w").write(markdown.markdown(df.to_markdown(index=False), extensions=['tables']))


if __name__ == '__main__':
    main()