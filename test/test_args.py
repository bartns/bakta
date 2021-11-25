import os
import pytest

from pathlib import Path
from subprocess import run

from .conftest import FILES, SKIP_PARAMETERS


@pytest.mark.parametrize(
    'parameters',
    [
        ([]),  # not provided
        (['']),  # empty
        (['foo.fasta']),  # not existing
        (['fo o.fasta']),  # not existing (whitespace)
        (['test/data/invalid.fasta']),  # invalid fasta DNA alphabet
        (['test/data/NC_002127.1.fna', 'foo']),  # additional argument
    ]
)
def test_genome_failing(parameters, tmpdir):
    # test genome arguments
    cmd_line = ['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS
    proc = run(cmd_line)
    assert proc.returncode != 0


@pytest.mark.parametrize(
    'parameters',
    [
        ([]),  # not provided
        (['--db']),  # missing path
        (['--db', '', ]),  # empty
        (['--db', 'test/foo']),  # not existing
    ]
)
def test_database_failing_parameter(parameters, tmpdir):
    # test database arguments

    cmd_line = ['bin/bakta', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna']
    proc = run(cmd_line)
    assert proc.returncode != 0


@pytest.mark.parametrize(
    'env_key,env_value',
    [
        ('foo', ''),  # not provided
        ('BAKTA_DB', ''),  # missing path
        ('BAKTA_DB', 'test/foo')  # not existing path
    ]
)
def test_database_failing_environment(env_key, env_value, tmpdir):
    # test database arguments

    env = os.environ
    env[env_key] = env_value
    cmd_line = ['bin/bakta', '--output', tmpdir, 'test/data/NC_002127.1.fna']
    proc = run(cmd_line, env=env)
    assert proc.returncode != 0


def test_database_ok(tmpdir):
    # test database arguments

    # parameter OK
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir] + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode == 0

    # environment OK
    env = os.environ
    env['BAKTA_DB'] = 'test/db'
    proc = run(['bin/bakta', '--output', tmpdir] + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'], env=env)
    assert proc.returncode == 0


def test_output_failing():
    # test database arguments
    cmd_line = ['bin/bakta', '--output', '/', 'test/data/draft-w-plasmids.fna']
    proc = run(cmd_line)
    assert proc.returncode != 0


@pytest.mark.parametrize(
    'parameters',
    [
        (['--tmp-dir'])  # not provided
    ]
)
def test_tmp_dir_failiing(parameters, tmpdir):
    # test tmp dir arguments
    cmd_line = ['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna']
    proc = run(cmd_line)
    assert proc.returncode != 0


def test_tmp_dir_ok(tmpdir):
    # test tmp dir arguments

    # parameter OK
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir, '--tmp-dir', ''] + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode == 0


@pytest.mark.parametrize(
    'parameters',
    [
        (['--prodigal-tf']),  # not provided
        (['--prodigal-tf', '']),  # empty
        (['--prodigal-tf', 'foo'])  # not existing
    ]
)
def test_prodigal_tf_failiing(parameters, tmpdir):
    # test prodigal training file arguments
    cmd_line = ['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna']
    proc = run(cmd_line)
    assert proc.returncode != 0


@pytest.mark.slow
def test_prodigal_tf_ok(tmpdir):
    # test prodigal training file arguments

    # OK
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir, '--prefix', 'test', '--prodigal-tf', 'test/data/prodigal.tf'] + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode == 0

    tmpdir_path = Path(tmpdir)
    for file in FILES:
        assert Path.exists(tmpdir_path.joinpath(file))


@pytest.mark.parametrize(
    'parameters',
    [
        (['--replicons']),  # not provided
        (['--replicons', '']),  # empty
        (['--replicons', 'foo'])  # not existing
    ]
)
def test_replicons_failiing(parameters, tmpdir):
    # test replicons file arguments
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode != 0


@pytest.mark.slow
def test_replicons_ok(tmpdir):
    # test replicons file arguments

    # OK: replicons as CSV
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir, '--prefix', 'test', '--replicons', 'test/data/replicons.csv'] + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode == 0

    tmpdir_path = Path(tmpdir)
    for file in FILES:
        assert Path.exists(tmpdir_path.joinpath(file))

    # OK: replicons as TSV
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir, '--prefix', 'test', '--replicons', 'test/data/replicons.tsv'] + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode == 0

    tmpdir_path = Path(tmpdir)
    for file in FILES:
        assert Path.exists(tmpdir_path.joinpath(file))


@pytest.mark.parametrize(
    'parameters',
    [
        (['--proteins']),  # not provided
        (['--proteins', '']),  # empty
        (['--proteins', 'foo'])  # not existing
    ]
)
def test_proteins_failiing(parameters, tmpdir):
    # test proteins file arguments
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode != 0


@pytest.mark.slow
def test_proteins_ok(tmpdir):
    # test proteins file arguments

    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir, '--prefix', 'test', '--proteins', 'test/data/user-proteins.faa'] + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode == 0

    tmpdir_path = Path(tmpdir)
    for file in FILES:
        assert Path.exists(tmpdir_path.joinpath(file))


@pytest.mark.parametrize(
    'parameters',
    [
        (['--locus']),  # not provided
        (['--locus', '']),  # empty
        (['--locus', ' ']),  # whitespace only
        (['--locus', '  ']),  # whitespaces only
        (['--locus', 'fo o']),  # containing whitespace
        (['--locus', 'ABCDEFGHIJKLMNOPQRSTU'])  # more than 20 characters
    ]
)
def test_locus_failiing(parameters, tmpdir):
    # test locus prefix arguments
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode != 0


@pytest.mark.slow
@pytest.mark.parametrize(
    'parameters',
    [
        (['--locus', 'ABC']),
        (['--locus', 'ABCDEFGHIJKLMNOPQRST']),
        (['--locus', 'A123_.:*#-'])
    ]
)
def test_locus_ok(parameters, tmpdir):
    # test locus prefix arguments
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode == 0


@pytest.mark.parametrize(
    'parameters',
    [
        (['--locus-tag']),  # not provided
        (['--locus-tag', '']),  # empty
        (['--locus-tag', ' ']),  # whitespace only
        (['--locus-tag', '  ']),  # whitespaces only
        (['--locus-tag', 'fo o']),  # containing whitespace
        (['--locus-tag', '123ABC']),  # first character is not a letter
        (['--locus-tag', 'abc']),  # lower case letters
        (['--locus-tag', 'AB']),  # less than 3 characters
        (['--locus-tag', 'ABCDEFGHIJKLM']),  # more than 12 characters
        (['--locus-tag', 'ABC_']),  # wrong characters
        (['--locus-tag', 'ABC-']),  # wrong characters
        (['--locus-tag', 'ABC!']),  # wrong characters
        (['--locus-tag', 'ABC?']),  # wrong characters
        (['--locus-tag', 'ABC*']),  # wrong characters
        (['--locus-tag', 'ABC.']),  # wrong characters
        (['--locus-tag', 'ABC,']),  # wrong characters
        (['--locus-tag', 'ABC;'])  # wrong characters
    ]
)
def test_locustag_failiing(parameters, tmpdir):
    # test locus-tag prefix arguments
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode != 0


@pytest.mark.slow
@pytest.mark.parametrize(
    'parameters',
    [
        (['--locus-tag', 'ABC']),
        (['--locus-tag', 'ABCDEFGHIJKL']),
        (['--locus-tag', 'A12']),
        (['--locus-tag', 'A23456789012'])
    ]
)
def test_locustag_ok(parameters, tmpdir):
    # test locus-tag prefix arguments
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode == 0


@pytest.mark.parametrize(
    'parameters',
    [
        (['--genus']),  # not provided
        (['--genus', '']),  # empty
        (['--genus', ' ']),  # whitespace only
        (['--genus', '  '])  # whitespaces only
    ]
)
def test_genus_failiing(parameters, tmpdir):
    # test genus prefix arguments
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode != 0


@pytest.mark.parametrize(
    'parameters',
    [
        (['--species']),  # not provided
        (['--species', '']),  # empty
        (['--species', ' ']),  # whitespace only
        (['--species', '  '])  # whitespaces only
    ]
)
def test_species_failiing(parameters, tmpdir):
    # test species prefix arguments
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode != 0


@pytest.mark.parametrize(
    'parameters',
    [
        (['--strain']),  # not provided
        (['--strain', '']),  # empty
        (['--strain', ' ']),  # whitespace only
        (['--strain', '  '])  # whitespaces only
    ]
)
def test_strain_failiing(parameters, tmpdir):
    # test strain prefix arguments
    proc = run(['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna'])
    assert proc.returncode != 0


@pytest.mark.parametrize(
    'parameters',
    [
        (['--gram']),  # not provided
        (['--gram', '']),  # empty
        (['--gram', 'foo']),  # wrong string
        (['--gram', '-1']),  # number
        (['--gram', '0']),  # number
        (['--gram', '1.1']),  # number
    ]
)
def test_threads_failing(parameters, tmpdir):
    # test gram arguments
    cmd_line = ['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna']
    proc = run(cmd_line)
    assert proc.returncode != 0


@pytest.mark.parametrize(
    'parameters',
    [
        (['--threads']),  # not provided
        (['--threads', '']),  # empty
        (['--threads', 'foo']),  # string
        (['--threads', '-1']),  # smaller than zero
        (['--threads', '0']),  # zero
        (['--threads', '1.1']),  # float
        (['--threads', '1000'])  # larger than available threads
    ]
)
def test_threads_failing(parameters, tmpdir):
    # test threads arguments
    cmd_line = ['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna']
    proc = run(cmd_line)
    assert proc.returncode != 0


@pytest.mark.parametrize(
    'parameters',
    [
        (['--min-contig-length']),  # not provided
        (['--min-contig-length', '']),  # empty
        (['--min-contig-length', 'foo']),  # string
        (['--min-contig-length', '-1']),  # smaller than zero
        (['--min-contig-length', '0']),  # zero
        (['--min-contig-length', '1.1']),  # float
    ]
)
def test_min_contig_length_failing(parameters, tmpdir):
    # test min-contig-length arguments
    cmd_line = ['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna']
    proc = run(cmd_line)
    assert proc.returncode != 0


@pytest.mark.parametrize(
    'parameters',
    [
        (['--translation-table']),  # not provided
        (['--translation-table', '']),  # empty
        (['--translation-table', 'foo']),  # string
        (['--translation-table', '-1']),  # smaller than zero
        (['--translation-table', '0']),  # zero
        (['--translation-table', '1.1']),  # float
    ]
)
def test_min_contig_length_failing(parameters, tmpdir):
    # test min-contig-length arguments
    cmd_line = ['bin/bakta', '--db', 'test/db', '--output', tmpdir] + parameters + SKIP_PARAMETERS + ['test/data/NC_002127.1.fna']
    proc = run(cmd_line)
    assert proc.returncode != 0
