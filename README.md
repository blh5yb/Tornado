# Inscripta Code Interview

Thank you for your interest in Inscripta! As part of our candidate interview process, we'd like to get
a sense of your programming ability and style. To that end, we've developed the following programming
scenario that we'd like to invite you to complete.

## Bioinformatic API Server

You are a Bioinformatic software engineer developing a web service to handle genomic data. You have been
provided the following set of main features that need to be included in your initial server:

1. User can register a genome file (user can POST the file and will receive a unique identifier for the registered file):

Files will be of the form:
```
>chromosome1
ACGTACGTACGATCGACAGTCGATCGATCGATCGATCAGCTAGCTA
>chromosome2
GATCGATCGATCAGTCAGTGCTAGCATCGATCGATCGATCGATCGA
```

Files should be stored and can be later looked up by the unique identifier provided in the response.

2. User can query for the names and lengths of chromosomes for a given registered genome using the unique identifier.

3. User can retrieve the sequence of a genomic region of the registered genome, ex:
   chromosome1: 1-5 of the genome in #1 should return ACGTA

4. User can provide a query sequence and genome or genomic region, service will return any substring matches of the
   sequence in the forward direction as well as reverse complement direction on the genome. Service should return
   indices (start and end) of the match.

## Getting Started
A basic backend API application is provided for you in this zip file. Please enhance the code in the application such
that the server has the features enumerated above.

As you develop your server, please treat this exercise as production ready code and include docstrings, tests, etc.
We believe you should be able to complete your web server in a few hours - please don't spend more than four hours!
If you find there are enhancements that you would make to your code given more time, feel free to note them.

### Notes:
- The web service should be treated as a backend only service
- Update the provided README with any additional instructions required to run the server
- Feel free to use any additional libraries you want.
  If you do leverage additional libraries, they should be added to the `requirements.txt` file.
- Reverse complement direction refers to reversing the sequence and converting each nucleotide to its complement
  (A->T, C->G, G->C, T->A) e.g. ACTG becomes CAGT

## Quickstart

Create a virtual environment and install prerequisites:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

(You may also use a [conda](https://docs.conda.io/en/latest/miniconda.html)
environment if you prefer.)

To start the service in debug mode (which enables automatic reloading when code
changes are detected):

```
python3 app.py --debug
```


