## Bioinformatic API Server

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


## Quickstart

Create a virtual environment and install prerequisites:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

To start the service in debug mode (which enables automatic reloading when code
changes are detected):

```
python3 app.py --debug
```

