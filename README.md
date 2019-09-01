# Moog Analog Synthesizer Component Characterization and Implementation of their Digital Model in Pure Data.

SMC Master Thesis Nerea T. Ruiz. 2019

This repository is part of the work done for the Master Thesis of Sound and Music Computing Master program in Universitat Pompeu Fabra (UPF). It includes the project files related to the implementation of a simplyfied digital version of the analog synthesizer Moog Slim Phatty.

Files included are related to: 

1) the Pure Data model implementation.
2) the files corresponding to the listening experiments conducted with the participants. 
3) the python scripts to perform the dataset recordings created for the thesis.

The Pure Data model includes 3 patches each implementing a different ladder filter object. The objects are Muug~, Bob~, and Moog~. 

All the patches implement characterized controls with the data extracted from the original synthesizer, thus imitating the non linear behaviour of its parameters. 

The files Moog_PD_muug_object.pd, Moog_PD_bob_object.pd, and Moog_PD_moog_object.pd correspond to each of the patches developed for the project, each implementing a different ladder filter object, as indicated above. 

Open the patches in Pure Data to run them. Each includes a GUI with the controls of the synthesizer, noting that the GUI is identical in every model. 

For more information about the patch, click the Pd Moog object on the left side of the GUI in any of the patches. Three main parts are included:

1) Pd midi-file allows you to play and record midi files to conduct the experiment.
2) Pd curves includes the data extracted from the analysis performed with the analog synthesizer. These curves are implemented in the Pure Data knobs to imitate the non linear behaviour of the Moog Slim Phatty parameters.
3) Pd audio signal flow recreates the Moog Slim Phatty audio signal flow. It contains the sampled waveforms from the original synthesizer, VCF and VCA envelopes and the filter including cutoff frequency, resonance an envelope amount knobs modeled. 

To run the patch install the dependencies listed below: 

  ggee
  ceammc
  cyclone
  moonlib

All patches were developed with Pure Data version 0.49.1

The python scripts for dataset creation are included in this repository:

1) Script to create the parameter characterization dataset
2) Script to sample the Moog waveforms
3) Scriot to create an extended dataset to build a sampler.


The files related to the listening experiments are included in the repository. 

1) Google forms sheets
2) Likert_scale_test_results
3) Listening experiment Item Pair ID random configurations.

 
