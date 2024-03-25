## KEGG_sketching_annotation_reproducibles

Reproducible scripts for the manuscript `Fast, lightweight, and accurate metagenomic functional profiling
using FracMinHash sketches`. The associated preprint will be added soon.

<!-- TOC start -->

### Contents:

- [Environment setup](#environment-setup)
- [Part 1: comparison with other tools](#part-1-comparison-with-other-tools)
- [Part 2: analyze HMP functional profiles](#part-2-analyze-hmp-functional-profiles)
- [Part 3: functional UniFrac](#part-3-functional-unifrac)

<!-- TOC end -->



<!-- TOC --><a name="environment-setup"></a>

### Environment setup

```
git clone https://github.com/KoslickiLab/KEGG_sketching_annotation_reproducibles.git
cd KEGG_sketching_annotation_reproducibles
conda create -y --name annotate_ko
conda activate annotate_ko
conda install -y -c conda-forge -c bioconda --file ./src/requirements.txt
```



The manuscript comprises three distinct experimental sections, with each section encompassing multiple subtasks. It's not necessary to do one after the other. Under the same conda environment, please refer to each specific section below to reproduce the corresponding results. 

</br>

<!-- TOC --><a name="part-1-comparison-with-other-tools"></a>

### Part 1: comparison with other tools

---

This segment replicates the findings presented in **Section 3.1**, where benchmarking analyses of `sourmash` were conducted in comparison to other tools. 

Please follow [this guideline](https://github.com/KoslickiLab/KEGG_sketching_annotation_reproducibles/blob/main/part1_comparison_with_other_tools/README.md) to reproduce all results (link below):

```
https://github.com/KoslickiLab/KEGG_sketching_annotation_reproducibles/blob/main/part1_comparison_with_other_tools/README.md
```

</br>

<!-- TOC --><a name="part-2-analyze-hmp-functional-profiles"></a>

### Part 2: analyze HMP functional profiles

---

This segment replicates the findings presented in **Section 3.2**, where we utilized `sourmash` to get functional profiles of all [HMP](https://portal.hmpdacc.org/) gut microbiome data and further analyzed the outputs. 

Please follow [this guideline](https://github.com/KoslickiLab/KEGG_sketching_annotation_reproducibles/blob/main/part2_analyze_HMP_data/README.md) to reproduce all results (link below):

```
https://github.com/KoslickiLab/KEGG_sketching_annotation_reproducibles/blob/main/part2_analyze_HMP_data/README.md
```

</br>

<!-- TOC --><a name="part-3-functional-unifrac"></a>

### Part 3: functional UniFrac

---

This segment replicates the findings presented in **Section 3.3**, where we demonstrate the usage of [Functional UniFrac](https://github.com/KoslickiLab/FunUniFrac) as a downstream analysis based on the FracMinHash-generated KO profiles. 

Please follow [this guideline](https://github.com/KoslickiLab/KEGG_sketching_annotation_reproducibles/blob/main/part3_FunUniFrac/README.md) to reproduce all results (link below):

```
https://github.com/KoslickiLab/KEGG_sketching_annotation_reproducibles/blob/main/part3_FunUniFrac/README.md
```
