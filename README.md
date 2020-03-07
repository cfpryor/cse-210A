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

This is broken into three phases: initialization, running, and evaluation.

#### Initialization

First begin by creating a postgreSQL database and user for tuffy.

```
createuser -s tuffy
createdb tuffy --password
```

Use **tuffy** as the password.

Data is gathered from psl-examples (which is already in a PSL formatting) and converted to the other PPL's formatting. Since this repository converts psl examples into other frameworks, use the psl-example directory names to specify which examples you want to run:

```
./init <example name> ...
```

For example if you want to run the psl-examples cora, use the following command:

```
./init cora
```

Now that the psl data has been gathered, it is now time to convert it to the other PPLs. For this a few datafiles are needed to aid in the process:

##### Tuffy

Three files are required for tuffy to run

1) predicates.txt - A helper file for converting PSL data.
2) prog.mln - A file containing the model in Tuffy syntax.
3) query.db - A file specifying what are the target predicates.

and are required to be put into there respective experiment directory **./tuffy-examples/[EXPERIMENT]/**.

An example of these files can be seen in **./scripts/tuffy-cora/**. To run the cora example use the following command:

```
cp scripts/cora-tuffy/* tuffy-examples/cora/
```

##### Data Conversion

As the final step in the initialization phase, data is convered from the PSL formatting to the other PPL's formatting with the following command:

```
./convert <example name> ...
```
For example if you want to run the psl-examples cora, use the following command:

```
./convert cora
```

#### Running

During the running phase, the desired examples are run for all of the PPLs.
