# A Comparison of Probablistic Programming Languages

Comparison between different probablistic programming languages. This repository will convert PSL examples into other probablistic programming languages (PPL).

1) Probablistic Soft Logic (PSL)

   - Website: https://psl.linqs.org
   - Code: https://github.com/linqs

2) Tuffy

   - Website and Code: http://i.stanford.edu/hazy/tuffy

## Getting Started

### Prerequisites

PSL must be installed on your machine. Check out the main website (https://psl.linqs.org) for an installation guide.

### Running

This is broken into two phases: initialization and running.

#### Initialization

During the initialization phase, data is gathered for PSL and converts to the other PPLs. Since this repository converts psl examples into other frameworks, use the psl-example directory names to specify which examples you want to run:

```
./init <example name ...>
```

For example if you want to run the psl-examples simple-acquaintances and jester, use the following command:

```
./init simple-acquaintances jester
```

#### Running

During the running phase, the desired examples are run for all of the PPLs.
