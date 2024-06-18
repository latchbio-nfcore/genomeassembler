from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], busco_lineage_path: typing.Optional[LatchDir], reference: typing.Optional[LatchFile], mash_screen_db: typing.Optional[LatchFile], enable_ont_kmer_analyses: typing.Optional[bool], email: typing.Optional[str], multiqc_title: typing.Optional[str], genome: typing.Optional[str], fasta: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], step: typing.Optional[str], kmer_size: typing.Optional[int], ploidy: typing.Optional[int], busco_lineages: typing.Optional[str], kmer_counter: typing.Optional[str]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('step', step),
                *get_flag('kmer_size', kmer_size),
                *get_flag('ploidy', ploidy),
                *get_flag('busco_lineages', busco_lineages),
                *get_flag('busco_lineage_path', busco_lineage_path),
                *get_flag('reference', reference),
                *get_flag('mash_screen_db', mash_screen_db),
                *get_flag('kmer_counter', kmer_counter),
                *get_flag('enable_ont_kmer_analyses', enable_ont_kmer_analyses),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('genome', genome),
                *get_flag('fasta', fasta),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_genomeassembler", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_genomeassembler(input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], busco_lineage_path: typing.Optional[LatchDir], reference: typing.Optional[LatchFile], mash_screen_db: typing.Optional[LatchFile], enable_ont_kmer_analyses: typing.Optional[bool], email: typing.Optional[str], multiqc_title: typing.Optional[str], genome: typing.Optional[str], fasta: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], step: typing.Optional[str] = 'data_qc,preprocess,assemble,validate,curate', kmer_size: typing.Optional[int] = 31, ploidy: typing.Optional[int] = 2, busco_lineages: typing.Optional[str] = 'auto', kmer_counter: typing.Optional[str] = 'fastk') -> None:
    """
    nf-core/genomeassembler

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, step=step, kmer_size=kmer_size, ploidy=ploidy, busco_lineages=busco_lineages, busco_lineage_path=busco_lineage_path, reference=reference, mash_screen_db=mash_screen_db, kmer_counter=kmer_counter, enable_ont_kmer_analyses=enable_ont_kmer_analyses, email=email, multiqc_title=multiqc_title, genome=genome, fasta=fasta, multiqc_methods_description=multiqc_methods_description)

