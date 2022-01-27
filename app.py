from argparse import ArgumentParser
from io import StringIO
import logging
from typing import Dict
import os
import json
import re

from Bio import SeqIO
from Bio.Seq import Seq

from db import ConnectingSQL

import tornado
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging
from tornado.web import Application, RequestHandler, StaticFileHandler, MissingArgumentError

__version__ = "1.0.0"

logger = logging.getLogger(__name__)


def upload_genome(file_body, file_name):
    """
    Upload a genome to 'genomes' table of 'coding_challenge' database

    Parameters
    ----------
    file_body
        genome file contents
    file_name
        name of the genome file

    Returns
    -------
    id of the genome database record
    """
    sql_query = f"insert into genomes (file_name, file_body) " \
                f"VALUES ('{file_name}', '{file_body}')"
    db = ConnectingSQL()
    db.execute(sql_query, 'coding_challenge')
    db.commit()

    get_id_query = f"select id from genomes where file_name= '{file_name}'"
    db.execute(get_id_query, 'coding_challenge')
    file_id = list(db.fetch()[0])[0]
    db.close()

    return file_id


def fetch_genome(id):
    """
    Fetch genome for db by id
    Parameters
    ----------
    id
        genome id

    Returns
    -------
    Dictionary of genome locations and sequences
    """
    db = ConnectingSQL()
    db.execute(f"Select file_body from genomes where id = {id}",
               "coding_challenge")
    un_parsed_genome = list(db.fetch()[0])[0]
    my_genome = parse_genome_data(un_parsed_genome)
    return my_genome


def fetch_all_genomes():
    """
    Fetch all genomes in db
    Returns
    -------
    Dictionary of genome dictionaries
    """
    db = ConnectingSQL()
    db.execute(f"Select id, file_body from genomes", "coding_challenge")
    unparsed_genomes = db.fetch()

    parsed_genomes = {}
    for g in list(unparsed_genomes):
        parsed_genomes[str(g[0])] = parse_genome_data(g[1])

    return parsed_genomes


def get_matches(sub_seq, region):
    """
    Get locations of matches in a genomic region

    Parameters
    ----------
    sub_seq
        sequence substring being queried for
    region
        genomic region to query

    Returns
    -------
    Dictionary of forward and reverse complement matches
    """
    try:
        forward_start_sites = [s.start() for s in re.finditer(sub_seq.upper(), region.upper())]
        reverse_seq = Seq(sub_seq).reverse_complement()
        reverse_start_sites = [s.start() for s in re.finditer(str(reverse_seq).upper(), region.upper())]
    except TypeError:
        logger.error(TypeError)

    forward_matches = [{"start": i + 1, "end": (i + len(sub_seq))} for i in forward_start_sites]
    reverse_matches = [{"start": i + 1, "end": (i + len(sub_seq))} for i in reverse_start_sites]

    return {"forward_matches": forward_matches, "reverse_matches": reverse_matches}


def parse_genome_data(contents: str) -> Dict[str, str]:
    """
    Parse genome data.

    Parameters
    ----------
    contents
        Contents of the genome file data.

    Returns
    -------
    Dictionary mapping names to sequences.

    """
    try:
        buffer = StringIO(contents)
        return {
            record.name: str(record.seq) for record in SeqIO.parse(buffer, "fasta")
        }
    except Exception as e:
        logger.error(f"{e}")


class VersionHandler(RequestHandler):
    """Handle version requests."""

    def get(self) -> None:
        """Write version info."""
        self.write({"api": __version__, "tornado": tornado.version})

    def post(self) -> None:
        """Why would you POST to a version endpoint?"""
        self.set_status(405, reason="you can't change the version via POST")


class GenomeSeqHandler(RequestHandler):
    def get(self, id) -> None:
        try:
            sub_seq = self.get_argument("seq")
            genome = fetch_genome(id)
            response = {}
            for region in genome:
                response[region] = get_matches(sub_seq, genome[region])

            self.set_status(200)
            self.write(response)
        except Exception as e:
            logger.error(f"{e}")
            self.set_status(400, reason=f"{e}")


class QueryGenomeHandler(RequestHandler):
    """
    query for the names and lengths of chromosomes for a given registered genome
    or
    retrieve the sequence of a genomic region of the registered genome
    using the unique identifier (both queries require id)
    """
    def get(self, id) -> None:
        try:
            seq_name = self.get_argument('region')
            start = int(self.get_argument('start'))
            end = int(self.get_argument('end')) + 1

            genome = fetch_genome(id)
            response = {
                'sequence': genome[seq_name][start:end]
            }
            self.set_status(200)
            self.write(response)

        # if no query params, return genome chromosomes and lengths
        except Exception as e:
            logger.info(f"{e}")
            self.set_status(400, reason=f"{e}")


class QueryRegionHandler(RequestHandler):
    """
    return matches for given query sequence and genomic region for all genomes
    """
    def get(self) -> None:
        try:
            sub_seq = self.get_argument("seq")
            region = self.get_argument("region")
            genomes = fetch_all_genomes()
            print(genomes)
            response = {}
            for id in genomes:
                full_seq = genomes[str(id)][region]
                response[f"genome_id_{id}"] = get_matches(sub_seq, full_seq)
            self.set_status(200)
            self.write(response)

        except Exception as e:
            logger.error(f"{e}")
            self.set_status(400, reason=f"{e}")


class GenomeHandler(RequestHandler):
    """Register genome (POST)
    or
    return any substring matches of a query sequence and genome
    """
    def get(self) -> None:
        """Query Genome given an id param"""
        try:
            id = self.get_argument("id")
            print(id)
            genome = fetch_genome(id)
            for seq in genome:
                genome[seq] = f'{len(seq)} bp'
            self.set_status(200)
            self.write(genome)

        except Exception as e:
            logger.error(e)
            self.set_status(400, reason=f"{e}")
            # ################## just for testing ######################
            #self.write("Upload a genome or add genome id query param")
            #self.render("index.html")

    def post(self) -> None:
        """Upload genome file and save to 'coding_challenge' database table"""
        try:
            genome_file = self.request.files["genomeFile"][0]
            genome_id = upload_genome(genome_file.body.decode(), genome_file.filename)
            response = {'id': genome_id}
            self.set_status(200)
            self.write(response)

        except Exception as e:
            logger.error(f"Error writing genome file, {genome_file.filename}: {e}")
            self.set_status(500, reason=f"Server Error: {e}")
            self.write("Server Error")


def make_app(debug: bool = False) -> Application:
    """Create the Tornado web application.

    Please see https://www.tornadoweb.org/en/stable/guide.html for a crash
    course in how to build web applications with Tornado. Routes are defined
    with regular expressions (the guide contains some simple examples such as
    found at https://tornado-doc-chs.readthedocs.io/en/latest/guide/structure.html#the-application-object).

    """
    return Application(
        # TODO: define the rest of your routes here
        [
            ("/version", VersionHandler),
            ("/genomes", GenomeHandler),
            ("/retrieve_seq/([0-9]+)", QueryGenomeHandler),
            ("/genome_search/([0-9]+)", GenomeSeqHandler),
            ("/genome_regions", QueryRegionHandler),
        ],
        debug=debug,
    )


def main() -> None:
    """Run the API service."""
    parser = ArgumentParser()
    parser.add_argument("--debug", "-d", action="store_true", help="enable debug mode")
    parser.add_argument(
        "--port", "-p", type=int, default=8080, help="port to listen on"
    )
    args = parser.parse_args()
    enable_pretty_logging()
    app = make_app(args.debug)
    app.listen(args.port)
    logger.info("Listening on port %d", args.port)
    IOLoop.current().start()


if __name__ == "__main__":
    main()
