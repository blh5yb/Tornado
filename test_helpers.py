import pytest
from app import reverse_complement, parse_genome_data

@pytest.mark.parametrize(
    "sequence, exp_revcomped",
    [
        ("aaccttgca", "tgcaaggtt"),
        ("AAccttgca", "tgcaaggTT"),
        ("AAccNtgca", "tgcaNggTT"),
    ],
)
def test_reverse_complement(sequence, exp_revcomped):
    obs_revcomped = reverse_complement(sequence)
    assert obs_revcomped == exp_revcomped


def test_parse_genome_data():
    contigs_and_seqs = {
        "seq_1": "ATGAAAGCGAACCTGCTGGTTCTGCTGTGCGCGCTGGCGGCGGCGGACGCGGACACCATCTGCATCGGTTACCACGCGAACAACTCTACCGACACCGTTGACACCGTTCTGGAAAAAAACGTTACCGTTACCCACTCTGTTAACCTGCTGGAAGACTCTCACAACGGTAAACTGTGCCGT",
        "seq_2": "CTGAAAGGTATCGCGCCGCTGCAGCTGGGTAAATGCAACATCGCGGGTTGGCTGCTGGGT",
        "seq_3": "AACCCGGAATGCGACCCGCTGCTGCCGGTTCGTTCTTGGTCTTACATCGTTGAAACCCCGAACTCTGAAAACGGTATCTGCTACCCGGGTGACTTCATCGACTACGAAGAACTGCGTGAA"
    }
    def create_genome_data(contigs_and_seqs, length_seq_line=80):
        genome_data = ""
        for contig, seq in contigs_and_seqs.items():
            genome_data += f"> {contig}\n"
            genome_data += "\n".join([seq[idx:idx+length_seq_line] for idx in range(0, len(seq), length_seq_line)]) + "\n"
        return genome_data

    genome_data = create_genome_data(contigs_and_seqs)
    obs_contigs_and_seqs = parse_genome_data(genome_data)
    assert contigs_and_seqs == obs_contigs_and_seqs

