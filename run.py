#!/usr/bin/env python3
#
#
# A simple demo gear that takes a structural image as input
# and runs Nonlocal Means Denoising to generate a denoised output.
#
# The gear uses the nipype ANTs interface and reads user defined options
# from the Flywheel-UI generated config.json for noise_model and shrink_factor
#
# Code for building a workflow with nodes are included as comments
# --> this can be scaled up to build a complete custom preproc pipeline

import flywheel
from nipype.interfaces.ants import DenoiseImage
# import workflow and node wrappers
#import nipype.pipeline.engine as pe 
# testing with simple os run
import os

context = flywheel.GearContext()  # Get the gear context.
config = context.config           # from the gear context, get the config settings.

## Load in values from the gear configuration.
noise_model = config['noise_model']
shrink_factor = config['shrink_factor']

## Load in paths to input files for the gear.
anat_t1w = context.get_input_path('t1w')

## configure nipype node for denoise image
# denoise = pe.Node(interface=DenoiseImage,name='nlm_denoise')

## configure nipype denoise image
denoise = DenoiseImage()
denoise.inputs.dimension = 3
denoise.inputs.noise_model=noise_model
denoise.inputs.shrink_factor = shrink_factor
denoise.inputs.input_image = anat_t1w
# print command 
print(denoise.cmdline)

# simple run
os.system(denoise.cmdline)

## set up workflow
# workflow = pe.Workflow(name="anat_t1w_denoise")
# workflow.base_dir = '.'
## add nodes
# workflow.add_nodes([denoise])
## write graph
# workflow.write_graph()
## run workflow
# workflow.run()
