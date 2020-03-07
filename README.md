# A Comparison of Probablistic Programming Languages

This repository will convert the desired datasets from probablistic soft logic (PSL) into the other probablistic programming languages (PPL), run the desired datasets for each PPL, and provide results for analysis. Current PPLs supported:

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

Running is broken into three phases: initialization, running, and evaluation.

#### Initialization

First begin by creating a postgreSQL database and user for tuffy.

```
createuser -s tuffy
createdb tuffy --password
```

Use **tuffy** as the password.

The data is gathered from psl-examples (which is already in a PSL formatting) and converted into the other PPL's formatting. Since this repository converts psl examples into other frameworks, use the psl-example directory names to specify which examples you want to run:

```
./init <example name> ...
```

For example if you want to run **cora** from the psl-examples, use the following command:

```
./init cora
```

Now that the psl data has been gathered, it is now time to convert it to the other PPLs. For this a few data files are needed:

##### Tuffy

Three files are required for tuffy to run:

1) predicates.txt - A helper file for converting PSL data.
2) prog.mln - A file containing the model in Tuffy syntax.
3) query.db - A file specifying what are the target predicates.

These are required and should be put into their respective directories: **./tuffy-examples/[EXPERIMENT]/**.

An example of the formatting for these files can be seen in **./scripts/tuffy-cora/**. To run the cora example use the following command:

```
cp scripts/cora-tuffy/* tuffy-examples/cora/
```

##### Data Conversion

As the final step in the initialization phase, data is convered from the PSL formatting to the other PPL's formatting:

```
./convert <example name> ...
```

For example if you want to run **cora**, use the following command:

```
./convert cora
```

#### Running

During the running phase, the desired examples are run for the PPLs:

```
./run <example name> ...
```

For example if you want to run **cora** from the psl-examples, use the following command:

```
./run cora
```
