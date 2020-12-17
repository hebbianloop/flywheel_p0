# Flywheel Challenge :: A Structural Preprocessing Gear Demo

This repository contains all of the requirements for building a Flywheel Gear to perform Non-Local Means Denoising on a single T1-weighted Magnetic Resonance Image.

## Non-Local Denoising
The acquisition of Magnetic Resonance Images often includes thermal noise that degrades image contrast and disrupts performance of tissue segmentation algorithms. Standard structural image processing pipelines address the issue of noise in the high frequency spatial domain with a simple low-pass smoothing filter. However this disrupts the ability to distinguish tissue boundaries in the brain.

Non-local Means Denoising with a Rician Distribution is an alternative method that preserves edges in images by "assuming that the real part and imaginary part of the MRI image is an uncorrelated Gaussian distribution with a zero mean and equal variance." The Advanced Normalization Tools structural image processing software package contains an implementation that vastly improves image segmentation results. 


## Upgrading Structural Analysis Pipelines
A key challenge to upgrading existing pipelines with this methodological advancement is successfully building the ANTs binaries across various operating systems that may possess different library requirements.

This repository contains a Flywheel Gear that implements NLM denoising with a Rician noise distribution using a pre-specified Dockerfile to achieve reproducibility across software environments.

The user just needs to build and deploy the attached dockerfile using their own data and does not have to worry about results being effected by software differences.

This implementation allows the user to specify the `noise_model` as `Gaussian` or `Rician` and provides an option for downsampling high-resolution images to ease computational burden using the `shrink_factor` parameter.

### Recommendations
Users are encouraged to perform Intensity Spatial Bias correction prior to NLM denoising. 
NLM denoising is a great preprocessing step prior to FreeSurfer reconstruction or cortical thickness estimation with ANTs.

## What is a Gear?
A [Flywheel Gear](https://github.com/flywheel-io/gears/tree/master/spec) is an open-source specification for a computational module that takes a configuration object as input to run a specified analysis, pipeline, or workflow. 

The specification includes all of the necessary requirements to ensure reproducibility including:
  * input file metadata
  * runtime environment
  * authorship, licenses, citations, and contribution information

Additional metadata empowering large-scale automation for analyzing data with reproducible workflows are also specified. See the [step-by-step Flywheel tutorial](https://docs.flywheel.io/hc/en-us/articles/360041766774-Gear-Building-Tutorial) for more information.

## How can I use this?
To use this gear, you must have access to a [Flywheel API key](https://docs.flywheel.io/hc/en-us/articles/360007660533). 

You must also have [Docker](https://docs.docker.com/get-docker/) installed and create an account on Docker Hub.

### What is Docker?
Docker is a virtual runtime environment that allows users to replicate the exact environment required to execute some set of software on any machine that can run the Docker client. 

Docker solves the challenges of software reproducibility by making sure researchers are all using the same binary packages to run their analyses. 

This is especially important in modern neuroimaging, a practice that relies on many libraries and software packages that are in active development and can interfere with each other or even cause [diverging results across different environments!](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0038234) 

A user seeking to replicate the exact analysis reported in a publication can use docker with their own data and rest assured that any variations in results are due to the data and not the software environment.

## Installing this gear
To install this gear, you must clone this repository to your local computer. You can do this by opening a terminal window and using the following command
```
git clone https://github.com/seldamat/flywheel_p0
```

### Building the docker file
This repository contains a recipe for building a docker file that will execute the NLM T1w Denoising Gear using the standard nipype runtime environment.

To build this docker file, open a terminal window and enter the following command 
```
cd flywheel_p0
docker build --tag dockerhubun/flywheel_p0:0.0 .
```

where `dockerhubun` is your Docker Hub username.

The tag command is an identifier to help you distinguish between different container builds. You can set this to your own custom preference.

Once submitted, Docker will pull all the required segments and code-chunks,
```
Sending build context to Docker daemon  46.15MB
Step 1/12 : FROM nipype/nipype:latest
latest: Pulling from nipype/nipype
...
```
and will execute the `RUN` commands specified in Dockerfile. A successful build will result in the following output
```
Step 1/13 : FROM nipype/nipype:latest
 ---> a39f55e223de
Step 2/13 : USER root
 ---> Using cache
 ---> d874bcfb44c9
Step 3/13 : LABEL MAINTAINER="Shady El Damaty <se394@georgetown.edu>"
 ---> Using cache
 ---> 74eab7dc83d7
Step 4/13 : RUN apt-get update     && apt-get install -y     bsdtar     zip     unzip     gzip
 ---> Using cache
 ---> 9ebad570f191
Step 5/13 : RUN pip install --upgrade pip &&     pip install flywheel-sdk
 ---> Using cache
 ---> 0f4d47963bb2
Step 6/13 : ENV FLYWHEEL /flywheel/v0
 ---> Using cache
 ---> e5b9b6c8f29e
Step 7/13 : WORKDIR ${FLYWHEEL}
 ---> Using cache
 ---> 439e4a1ed55d
Step 8/13 : RUN mkdir ${FLYWHEEL}/input
 ---> Running in 25b1c6e144d8
Removing intermediate container 25b1c6e144d8
 ---> bd78d2271648
Step 9/13 : RUN python -c 'import os, json; f = open("/tmp/gear_environ.json", "w"); json.dump(dict(os.environ), f)'
 ---> Running in 9bfe29d9208e
Removing intermediate container 9bfe29d9208e
 ---> cf76c075fce0
Step 10/13 : COPY manifest.json ${FLYWHEEL}/
 ---> d1ed0d647832
Step 11/13 : COPY run.py ${FLYWHEEL}/
 ---> fd7cab80f06b
Step 12/13 : RUN chmod a+x ${FLYWHEEL}/run.py
 ---> Running in 5bc0cc6f7611
Removing intermediate container 5bc0cc6f7611
 ---> 7da576ee8881
Step 13/13 : ENTRYPOINT ["${FLYWHEEL}/run.py"]
 ---> Running in f99eafc8333f
Removing intermediate container f99eafc8333f
 ---> fd33f8741bc8
Successfully built fd33f8741bc8
Successfully tagged flywheel_p0:0.0
```

To run this file on Flywheel you will need to publish it to Docker Hub.
```
docker push dockerhubun/flywheel_p0:0.0 
```

Once pushed you can execute on Flywheel.

The gear can be run locally if you have Flywheel installed on your machine. The gear is called along with all the required configuration inputs
```
fw gear local --t1w=anat_t1w_file --noise_model='Rician' --shrink_factor=1
```
where `anat_t1w_file` is the full path (e.g. '/home/user1/data/anat_t1w.nii.gz' to the anatomical image you'd like to denoise. The user can specify `Rician` or `Gaussian` for denoising and downsample an image up to 1000x. The image must be a nifti file.

The docker image will be pulled and the run.py file executed within the container to generate the noise corrected file `sub-hebbianloop_ses-2019a_acq-mprage_t1w_noise_corrected.nii.gz`

That's it! You've successfully deployed a Flywheel gear to perform Rician Denoising on a T1w structural image!

### References
https://stnava.github.io/ANTs/

J. V. Manjon, P. Coupe, Luis Marti-Bonmati, D. L. Collins, and M. Robles. Adaptive Non-Local Means Denoising of MR Images With Spatially Varying Noise Levels, Journal of Magnetic Resonance Imaging, 31:192-203, June 2010.

Yang, J., Fan, J., Ai, D. et al. Brain MR image denoising for Rician noise using pre-smooth non-local means filter. BioMed Eng OnLine 14, 2 (2015). https://doi.org/10.1186/1475-925X-14-2
