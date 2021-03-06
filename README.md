# Socru
[![Build Status](https://travis-ci.org/quadram-institute-bioscience/socru.svg?branch=master)](https://travis-ci.org/quadram-institute-bioscience/socru)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-brightgreen.svg)](https://github.com/quadram-institute-bioscience/socru/blob/master/LICENSE)
[![Docker Build Status](https://img.shields.io/docker/build/quadram-institute-bioscience/socru.svg)](https://hub.docker.com/r/quadram-institute-bioscience/socru)
[![Docker Pulls](https://img.shields.io/docker/pulls/quadram-institute-bioscience/socru.svg)](https://hub.docker.com/r/quadram-institute-bioscience/socru)  

## Contents
  * [Introduction](#introduction)
  * [Installation](#installation)
    * [Ubuntu/Debian](#ubuntudebian)
    * [Docker](#docker)
  * [Usage](#usage)
  * [License](#license)
  * [Feedback/Issues](#feedbackissues)
  * [Citation](#citation)

## Introduction
Socru allows you to easily identify and communicate the order and orientation of complete genomes. These large scale structural variants have real impacts on the phenotype of the organism, and with the advent of long read sequencing, we can now start to delve into the mechanisms at work.

# Installation
If you just want to quickly try out the software please try a Docker continer. This software is designed to run on Linux and OSX. It will not run on Windows.

## Conda
To install Socru, first install conda with Python3 then run:
```
conda install barrnap blast git
pip3 install git+git://github.com/quadram-institute-bioscience/socru.git
```

## Docker
Install [Docker](https://www.docker.com/).  There is a docker container which gets automatically built from the latest version of Socru. To install it:

```
docker pull andrewjpage/socru
```

To use it you would use a command such as this (substituting in your filename/directories), using the example file in this respository:
```
docker run --rm -it -v /path/to/example_data:/example_data andrewjpage/socru socru xxxxx
```

# Usage

## Quick start
Given you have an Escherichia coli complete genome (K12.fasta), see what datbases are available:

```
socru_species
```
Next use one of the database names:
```
socru Escherichia_coli K12.fasta
```
which will give you output like:
```
K12.fasta	GS1.0	1	2	3	4	5	6	7
```



## socru
This is the main script for the application. If you provide a complete assembly, it will give you back the orientation and order of the fragments.

```
usage: socru [options] species assembly.fasta

calculate the order and orientation of complete bacterial genomes

positional arguments:
  species               Species name, use socru_species to see all available
  input_files           Input FASTA files (optionally gzipped)

optional arguments:
  -h, --help            show this help message and exit
  --db_dir DB_DIR, -d DB_DIR
                        Base directory for specices databases, defaults to
                        bundled (default: None)
  --threads THREADS, -t THREADS
                        No. of threads to use (default: 1)
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Output filename, defaults to STDOUT (default: None)
  --novel_profiles NOVEL_PROFILES, -n NOVEL_PROFILES
                        Filename for novel profiles (default:
                        profile.txt.novel)
  --not_circular, -c    Assume chromosome is not circularised (default: False)
  --min_bit_score MIN_BIT_SCORE
                        Minimum bit score (default: 1000)
  --min_alignment_length MIN_ALIGNMENT_LENGTH
                        Minimum alignment length (default: 1000)
  --verbose, -v         Turn on debugging (default: False)
  --version             show program's version number and exit
```

__species__: This mandatory argument is the name of the species database you wish to use. You can either create your own species database using socru_create or look up one of the bundled databases with socru_species. It normally takes the form of Genus_species, for example: "Salmonella_enterica".

__input_files__: This mandatory argument takes in a list of 1 or more FASTA files. Each FASTA file should be a complete assembly (chromosome in 1 contig) and never short read draft assemblies. Short read assemblies cant resolve large repeats, such as the rrn region. The FASTA files can be optionally gzipped (compressed).

__help__: This will print out the extended help information, including default values, then exit.

__db_dir__: By default the software will look for the bundled databases. You can use this option to change the base directory for the databases and point it somewhere else, perhaps if you have a custom database you wish to use or if you wish to separate data from software on your computing system.  You can use a relative or absolute path. The full database pathname is derived from joining this directory to the species argument.

__threads__: An integer with the number of threads to use. It defaults to 1 and you get diminishing returns with higher numbers. Theres not much benefit to be had from using more than 4 threads.

__output_file__: By default the output is printed to STDOUT (to your terminal screen). You can specify a filename to print it to instead. The default behaviour is to create the file if it doesnt already exist, and to __append__ to the end of the file if it already exists.

__novel_profiles__: Sometimes you encounter novel arrangments and orders. These will get printed to a file to allow you to update the profile.txt file in the database. If there is a new order of fragments, the first number will be 0. You will need to assign a number manually before adding it to the profile.txt. This is because you need to check to see if there is an assembly error or if it is a legitimate new pattern.  If its just a novel reorientation, the first number will have an integer of 1 or more.   Please considered sending your changes back to the GitHub repository, so that the whole community will benefit from your science.

__not_circular__: Not all bacteria have circular chromosomes, or you may have an incomplete assembly. This flag tells the software not to try joining up the start and end of the largest contig.  If you are using this flag, you may be attempting to use this software for a purpose for which it was never designed. 

__min_bit_score__: Internally blastn is used and this allows you to specify the minimum bit score for a hit to be considered, since blast will throw up a lot of small hits. 

__min_alignment_length__: Only consider blast alignment lengths above this value. Remember that there can be some very short fragments between rrns, so you'll need to know the approximate minimum fragment size (in bases) before increasing this value too high.

__verbose__: Print out enhanced information while the program is running.

__version__: Print the version of the software and exit. If the version is 'x.y.z' it probably means you havent installed the software in a standard manner (conda/pip).

### Output
The output is printed to STDOUT or to an output file. It is tab delimited and provides the filename, the GS number and the order and orientation of the individual fragments. If a fragment is reversed compared to the database reference, it is denoted prime (').
```
Staphylococcus/aureus/USA300.fna.gz	GS1.0	1	2	3	4	5
Staphylococcus/aureus/MOZ66.fna.gz	GS1.8	1	2	3	4'	5
```

### Not all complete genomes are equal
You should be aware that not all complete assemblies are equal. In the early days, each complete reference genome was lovingly hand finished by teams of scientists at huge expense. With the advent of long read sequencing and better bioinformatics methods, it allowed a huge number of complete assemblies to be produced at a fraction of the cost. Many of these assemblies have not rigourouse quality checks, so may contain large structural errors. These errors may manifest as novel patterns in the output of this software. So its useful for quality control if your input is your own assemblies.

## socru_species
This will list all the species databases bundled with the software. You can then copy and paste one of the names for use with the main socru script. It doesnt take any input, instead it just prints out a sorted list of available species.

```
usage: socru_species [options]

List all available species

optional arguments:
  -h, --help     show this help message and exit
  --verbose, -v  Turn on debugging (default: False)
  --version      show program's version number and exit
```

__help__: This will print out the extended help information, including default values, then exit.

__verbose__: Print out enhanced information while the program is running.

__version__: Print the version of the software and exit. If the version is 'x.y.z' it probably means you havent installed the software in a standard manner (conda/pip).

### Output
```
Acinetobacter_baumannii
Enterobacter_cloacae
Enterococcus_faecium
Klebsiella_pneumoniae
Salmonella_enterica
Staphylococcus_aureus
```

## socru_create
You can create your own database. All you need is a single complete genome in FASTA format as input.  Please consider pushing your new database back to the GitHub repository so that the whole community can benefit from your hard work.

```
usage: socru_create [options] output_directory assembly.fasta

create genome arrangement type scheme

positional arguments:
  output_directory      Output directory
  input_file            Input FASTA file (optionally gzipped)

optional arguments:
  -h, --help            show this help message and exit
  --threads THREADS, -t THREADS
                        No. of threads to use (default: 1)
  --fragment_order FRAGMENT_ORDER, -f FRAGMENT_ORDER
                        Order of fragments, you may need to change this,
                        example 1-2-3-4-5-6-7 (default: None)
  --dnaa_fasta DNAA_FASTA, -d DNAA_FASTA
                        Location of dnaA FASTA file, defaults to bundled
                        (default: None)
  --verbose, -v         Turn on debugging [False]
  --version             show program's version number and exit
```

__output_directory__: This is the directory where your new database will live. The directory must not already exist.  

__input_file__: This is a complete assembly file in FASTA format. You only need the chromosome, and if you provide it with more, only the largest sequence in the file will be used. This means that bacteria with more than 1 chromosome will only have their largest chromosome used by this software, sorry Vibrio.

__help__: This will print out the extended help information, including default values, then exit.

__threads__: An integer with the number of threads to use. It defaults to 1 and you get diminishing returns with higher numbers. Theres not much benefit to be had from using more than 4 threads.

__fragment_order__: By default the software will take the largest fragment and go around in a clockwise fashion, labeling the fragments incrementally (1,2,3,4,5...). You can choose to force different numbers on the fragments, perhaps if someone has already published a particular scheme. In practice this option shouldnt be used, and if you are using it, dont ask for any support when things go wrong.

__dnaa_fasta__: This is the location of the FASTA file containing the dnaA sequences which are used to anchor the fragment orientations. It defaults to a bundled version, so you should never need to change it. The FASTA file containing the dnaA genes was generated by [Circlator](https://github.com/sanger-pathogens/circlator). The [original file](https://raw.githubusercontent.com/sanger-pathogens/circlator/master/circlator/data/dnaA.fasta) is run through [cd-hit-est](http://weizhongli-lab.org/cd-hit/) with default parameters to cluster similar sequences and reduce the size of the overall file.

__verbose__: Print out enhanced information while the program is running.

__version__: Print the version of the software and exit. If the version is 'x.y.z' it probably means you havent installed the software in a standard manner (conda/pip).


## socru_lookup
This is a utility script which will take in a fragment pattern and give you back the GS number. Its probably of limited use, but if you do find it useful and need it extended/made better, please submit an Issue on GitHub to let us know.

```
usage: socru_lookup[options] /path/to/database 1-2-3-4-5-6-7

Given a set of fragments, output the type

positional arguments:
  db_dir         Database directory
  fragments      Fragments such as 1-2-3-4-5-6-7 or 1'-3-4'-5'-6'-7-2

optional arguments:
  -h, --help     show this help message and exit
  --verbose, -v  Turn on debugging [False]
  --version      show program's version number and exit
```

__db_dir__: The full path to the database.

__fragments__: The pattern to lookup. Each number is separated by a dash (-), and reverse orientations are denoted with prime ('). The first number should be 1.

__help__: This will print out the extended help information, including default values, then exit.

__verbose__: Print out enhanced information while the program is running.

__version__: Print the version of the software and exit. If the version is 'x.y.z' it probably means you havent installed the software in a standard manner (conda/pip).

# License
Socru is free software, licensed under [GPLv3](https://raw.githubusercontent.com/quadram-institute-bioscience/socru/master/VERSION/LICENSE).

# Feedback/Issues
Please report any issues or to provide feedback please go to the [issues page](https://github.com/quadram-institute-bioscience/socru/issues). If you make improvements to the software, add databases or extend profiles, please send us the changes though a [pull request](https://github.com/quadram-institute-bioscience/socru/pulls) so that the whole community may benefit from your work.

# Citation
Coming soon

# Resources required
To give you an indication of the resources required, a single 5Mbase assembly takes about 20 seconds using a single thread on an average laptop and uses no more than 250MB RAM. So overall the resource requirements are very light.

# Etymology
[socrú](https://www.focloir.ie/en/dictionary/ei/arrangement) (sock-roo) is the word for arrangment in Irish (Gaeilge). 
