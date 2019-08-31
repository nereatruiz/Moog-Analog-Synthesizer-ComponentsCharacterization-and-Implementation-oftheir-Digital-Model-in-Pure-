# Moog Analog Synthesizer Component Characterization and Implementation of their Digital Model in Pure Data

This repository is part of the work done for the Master Thesis of the Sound and Music Computing program in Universitat Pompeu Fabra (UPF). It includes the project files related to the implementation of a simple digital version of the analog synthesizer Moog Slim Phatty. 

Files included are related to: 
1) the pure data model implementation, 
2) the files corresponding to the listening experiments conducted with the participants, and 
3) the dataset created for the thesis, and the python script files.

The Pure Data model includes 3 patches each implementing a different ladder filter object (making the total 3 different ladder filter objects). The objects are Muug, Bob, and Moog. All the patches implement characterized controls with the data extracted from the original synthesizer, thus imitating the non linear behaviour of its parameters. 

The files 15072019_Moog_raw_PD_muug_object.pd, 15072019_Moog_raw_PD_bob_object.pd, and 15072019_Moog_raw_PD_moog_object.pd correspond to each of the patches developed for the project, each with its own ladder filter object as indicated above. 

Open the patches in Pure Data to run them. Each includes a GUI with the controls of the synthesizer, noting that the GUI is identical. For more information about the patch, click the pd moog object on the left side of the GUI in any of the patches. Three main parts will be visible:

1) pd midi-file allows you to play and record midi files to conduct the experiment.
2) pd curves includes the data extracted from the analog synthesizer parameters. These curves are implemented in the pure data knobs to imitate the non linear behaviour of the Moog Slim Phatty.
3) pd audio signal flow allows you to recreate the Moog Slim Phatty audio signal flow. It contains the sampled waveforms from the original synthesizer VCF and VCA envelopes and the filter. It is necessary to install some dependencies: 

  ggee
  ceammc
  cyclone
  moonlib

All patches were developed with Pure Data version 0.49.1

The datasets of the projects are included in the repository as well. The files contain the initial dataset designed for the characterization of the parameters in the original synthesizer and the dataset designed to conduct the experiment with the experts. 

Python scripts for data sampling are included in the corresponding folders. 


SMC Master Thesis 2019. Nerea T. Ruiz
 
