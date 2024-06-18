
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'step': NextflowParameter(
        type=typing.Optional[str],
        default='data_qc,preprocess,assemble,validate,curate',
        section_title=None,
        description='The stage of genome assembly to run',
    ),
    'kmer_size': NextflowParameter(
        type=typing.Optional[int],
        default=31,
        section_title=None,
        description='The k-mer size to use in k-mer analyses when not supplied in yaml metadata',
    ),
    'ploidy': NextflowParameter(
        type=typing.Optional[int],
        default=2,
        section_title=None,
        description='The estimated ploidy to use when not supplied in yaml metadata',
    ),
    'busco_lineages': NextflowParameter(
        type=typing.Optional[str],
        default='auto',
        section_title=None,
        description='The busco lineages to examine, when not supplied in the yaml metadata',
    ),
    'busco_lineage_path': NextflowParameter(
        type=typing.Optional[LatchDir],
        default=None,
        section_title=None,
        description='The local path to the downloaded busco lineages',
    ),
    'reference': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='An optional reference genome for comparison to',
    ),
    'mash_screen_db': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='A mash screen database to search for contamination',
    ),
    'kmer_counter': NextflowParameter(
        type=typing.Optional[str],
        default='fastk',
        section_title=None,
        description='The default k-mer counter to use for k-mer analyses',
    ),
    'enable_ont_kmer_analyses': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Flag to enable k-mer analyses on ONT data',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to FASTA genome file.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

