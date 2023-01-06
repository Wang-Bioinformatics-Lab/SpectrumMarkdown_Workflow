#!/usr/bin/env nextflow

params.input_usi_file = "./data/testusi.txt"

// Workflow Boiler Plate
params.OMETALINKING_YAML = "flow_filelinking.yaml"
params.OMETAPARAM_YAML = "job_parameters.yaml"

TOOL_FOLDER = "$baseDir/bin"

process processData {
    publishDir "./nf_output", mode: 'copy'

    conda "$TOOL_FOLDER/conda_env.yml"

    input:
    file input from Channel.fromPath(params.input_usi_file)

    output:
    file 'usiview.md'
    file 'usiview.html'
    file "images"

    """
    mkdir images
    python $TOOL_FOLDER/createusimarkdown.py $input usiview.md usiview.html images
    """
}