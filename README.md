# A Comparison of Probablistic Programming Languages

Comparison between different probablistic programming languages. This repository will convert probablistic soft logic (PSL) examples into other probablistic programming languages (PPL).

1) Probablistic Soft Logic

   - Website: https://psl.linqs.org
   - Code: https://github.com/linqs

2) Tuffy

   - Website and Code: http://i.stanford.edu/hazy/tuffy

## Getting Started

### Prerequisites

1) PSL (https://psl.linqs.org)

2) Java virtual machine (https://www.java.com/en/download/manual.jsp)

3) PostgreSQL (https://www.postgresql.org/download/)

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
