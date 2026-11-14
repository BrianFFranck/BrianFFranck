<div align="center">

<picture><source media="(prefers-color-scheme: light)" srcset="assets/light/hero.svg" /><img src="assets/hero.svg" width="100%" alt="BRIAN.LAB: Brian Franck, also known as Atlas, with a neural network passing signals from BIO to AI. BSc student in Computational Biomedicine &amp; AI at Universidade Lusófona. Now building Iris, a Gleason grading AI." /></picture>

</div>

<p align="center">
  <b>Hi, I'm Brian</b>, aka <b>Atlas</b>. I'm a <b>Computational Biomedicine &amp; AI</b> student at <b>Universidade Lusófona</b> in Lisbon.<br/>
  I'm interested in the place where medicine and machine learning meet: models that learn from slides, signals and sensors.
</p>

<p align="center">
  <sub>NOW BUILDING&nbsp;&nbsp;→&nbsp;&nbsp;<b><a href="https://github.com/BrianFFranck/IRIS">IRIS</a></b>, an AI that grades prostate biopsies and shows where it looked: a second reader for every prostate biopsy.</sub>
</p>

<br/>

<div align="center">

<a href="https://github.com/BrianFFranck/IRIS"><picture><source media="(prefers-color-scheme: light)" srcset="assets/light/iris.svg" /><img src="assets/iris.svg" width="100%" alt="Project 01, Iris: Gleason grading of prostate biopsies with attention multiple instance learning on the PANDA dataset, targeting the ISUP Grade Group 1 vs 2 boundary. Stage: early R&amp;D. Click to open the repository." /></picture></a>

<br/>

<a href="https://github.com/BrianFFranck/IRIS/blob/main/experiments.md"><picture><source media="(prefers-color-scheme: light)" srcset="assets/light/lab.svg" /><img src="assets/lab.svg" width="100%" alt="Iris lab notebook: the best real run so far from the experiment log, with validation QWK per fold, how many ISUP 2 slides were recognised, how much cancer the tiling keeps, the main finding, what comes next and which stages are done. Updated automatically. Click to open the experiment log." /></picture></a>

</div>

<div align="center">

<a href="https://github.com/BrianFFranck/IRIS"><picture><source media="(prefers-color-scheme: light)" srcset="assets/light/slide.svg" /><img src="assets/slide.svg" width="100%" alt="A real prostate biopsy from the PANDA dataset, ISUP grade 2, with the 48 tiles Iris keeps drawn on it. Tiles that contain cancer according to the PANDA label mask are outlined in amber. Three of the tiles are shown at the resolution the model reads. Tiling keeps 89% of the tissue and 95% of the cancer on this slide. Slide imagery: Radboud UMC and Karolinska Institutet, CC BY-SA-NC 4.0." /></picture></a>

</div>

<p align="center">
  <sub>Slide from the PANDA challenge dataset, used for non-commercial research under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-SA-NC 4.0</a>; the overlay is my own work and is shared under the same licence.<br/>
  Bulten, W., Kartasalo, K., Chen, P.-H. C. et al. <a href="https://doi.org/10.1038/s41591-021-01620-2">Artificial intelligence for diagnosis and Gleason grading of prostate cancer: the PANDA challenge</a>. Nat Med 28, 154–163 (2022).</sub>
</p>

<p align="center">
<!-- lab:start -->
<b>Where Iris is today (2026-11-13).</b> Best run so far: <code>abmil (gated attention MIL)</code> on 998 PANDA slides, validation QWK <b>0.69 ± 0.03</b>, with 17 of 125 ISUP 2 slides called ISUP 2. Tiling keeps a median 0.94 to 0.95 of the cancer tissue. Next: boundary-weighted loss (GG1 ↔ GG2 errors cost more)
<!-- lab:end -->
<br/>
<sub>These are validation numbers from early R&amp;D, not test results. The card and this line show the best run so far and update themselves from the <a href="https://github.com/BrianFFranck/IRIS/blob/main/experiments.md">experiment log</a>; every run, including the ones that don't work, is in the log.</sub>
</p>

<div align="center">

<a href="https://github.com/BrianFFranck/IRIS"><picture><source media="(prefers-color-scheme: light)" srcset="assets/light/iris-vision.svg" /><img src="assets/iris-vision.svg" width="100%" alt="Iris vision, a concept mock-up with illustrative values: biopsy cores where Iris marks the three regions it weighed most, zoomed crops showing pattern 3 glands and one small possible pattern 4 focus, a grade distribution leaning to ISUP 2 but borderline 1 / 2, and a send-to-pathologist button. Mission: a second reader for every prostate biopsy. The plan: research (now), prototype, validation, pilot, company." /></picture></a>

</div>

<details>
<summary><b>&nbsp;Iris: what it is, where it's going, and why the name</b></summary>

<br/>

**The problem.** Prostate biopsies are graded with the Gleason system and grouped into ISUP grade groups (1 to 5). The grade drives treatment, yet pathologists often disagree, especially on whether any Gleason pattern 4 is present: **ISUP 1 (Gleason 3+3)** versus **ISUP 2 (Gleason 3+4)**. That call often decides between active surveillance and treatment.

**The idea.** A whole-slide image is gigapixel-sized and comes with a single label. Iris treats each slide as a bag of thousands of tiles and uses **attention-based multiple instance learning** ([Ilse et al. 2018](https://arxiv.org/abs/1802.04712), the core of [CLAM](https://github.com/mahmoodlab/CLAM)) to learn which tiles drive the grade. Its attention map becomes a heatmap a pathologist can check, so the answer is never just a number. The code lives in [BrianFFranck/IRIS](https://github.com/BrianFFranck/IRIS).

**Where it's going.** A second reader that helps pathologists grade prostate biopsies faster and more consistently, and always shows its reasoning. If the model earns trust on public data first, the long-term goal is to build Iris into a company.

**Roadmap**

- [x] **Pipeline:** tissue masking, tiling, feature extraction, training loop and tests
- [x] **Data:** a 299-slide [PANDA](https://www.kaggle.com/c/prostate-cancer-grade-assessment) development subset, stratified by lab and grade; tiling checked against the label masks
- [x] **Baseline:** ResNet-50 tile features with mean/max pooling, the number to beat
- [ ] **Iris v1:** gated attention MIL on the same features
- [ ] **Boundary-weighted loss:** penalise ISUP 1 ↔ 2 mistakes more heavily than other errors
- [ ] **Full run:** all of PANDA at 20× on GPU
- [ ] **Evaluation:** quadratic weighted kappa on ISUP 0 (no cancer) to 5, per data centre, with a focused look at the ISUP 1 vs 2 boundary
- [ ] **Explainability:** attention heatmaps overlaid on the slide, checked against pixel-level Gleason masks
- [ ] **Write-up:** public code, results and what didn't work

**Beyond the model**

- [ ] **Validation:** external datasets and feedback from practising pathologists
- [ ] **Pilot:** a second-reader workflow tested with a pathology lab

**Something that didn't work.** Pen ink on a slide made the tissue mask throw away pale tissue: one ISUP 5 slide was left with 2 tiles. Ignoring ink and capping the threshold brought it to 18. Details like this go in the [experiment log](https://github.com/BrianFFranck/IRIS/blob/main/experiments.md).

**Why "Iris"?** The iris is the part of the eye that decides how much light gets in. Iris does the same for a biopsy: out of thousands of tiles, it decides which ones deserve attention, and it shows you where it looked.

<sub>Iris is in early research and development. It is not a medical device and is not cleared for clinical use.</sub>

</details>

<br/>

<div align="center">

<a href="https://github.com/BrianFFranck/ecg-data-audit"><picture><source media="(prefers-color-scheme: light)" srcset="assets/light/ecg-audit.svg" /><img src="assets/ecg-audit.svg" width="100%" alt="Project 02, ECG audit, a university group project: a reproducible audit of clinical ECG records that flags missing values, duplicate records, implausible values and quality notes without deleting anything. Click to open the repository." /></picture></a>

<br/>

<a href="https://github.com/BrianFFranck/myocardium-histology-network"><picture><source media="(prefers-color-scheme: light)" srcset="assets/light/histology.svg" /><img src="assets/histology.svg" width="100%" alt="Project 03, myocardium cell graph, a university group project: simulated H&amp;E heart biopsies turned into a spatial cell network with per-cell morphology, clusters and hubs, built with a grid neighbour search in linear time using only NumPy and Pillow. Click to open the repository." /></picture></a>

</div>

<p align="center">
  <sub>Projects 02 and 03 are group coursework at Universidade Lusófona, built with Rafael Pereira, Filipe Lopes and Bernardo Margarido:
  <a href="https://github.com/BrianFFranck/ecg-data-audit">ecg-data-audit</a> &nbsp;·&nbsp; <a href="https://github.com/BrianFFranck/myocardium-histology-network">myocardium-histology-network</a></sub>
</p>

<div align="center">

<picture><source media="(prefers-color-scheme: light)" srcset="assets/light/rppg.svg" /><img src="assets/rppg.svg" width="100%" alt="Project 04, rPPG vitals, a personal project: heart rate and breathing rate from an ordinary webcam. MediaPipe tracks the face, the forehead and cheeks give a mean skin colour per frame, POS turns it into a pulse signal and the spectrum peak gives beats per minute. Illustration with example values; not a medical device." /></picture>

</div>

<div align="center">

<picture><source media="(prefers-color-scheme: light)" srcset="assets/light/processes.svg" /><img src="assets/processes.svg" width="100%" alt="Process table of what I'm working on: BSc in biomedicine and AI (running), Iris Gleason grading (building), ECG data audit (shipped), myocardium cell graph (shipped), medical imaging (learning), Python (running)." /></picture>

<br/>

<picture><source media="(prefers-color-scheme: light)" srcset="assets/light/toolchain.svg" /><img src="assets/toolchain.svg" width="100%" alt="Toolchain as a constellation. Systems: Python (advanced), Linux, Git and GitHub, C. Data: pandas and NumPy, SQL, R, data visualization with Matplotlib and Seaborn. Machine learning: PyTorch, TensorFlow." /></picture>

</div>

<br/>

<p align="center">
  <b>Let's talk</b> about computational pathology, biosignals, Iris or anything where medicine meets machine learning.
</p>

<p align="center">
  <a href="mailto:brianferrarif@gmail.com?subject=Hi%20Brian"><picture><source media="(prefers-color-scheme: light)" srcset="assets/light/contact-email.svg" /><img src="assets/contact-email.svg" width="40%" alt="Email: brianferrarif@gmail.com" /></picture></a>
  <a href="https://www.linkedin.com/in/brian-franck-/"><picture><source media="(prefers-color-scheme: light)" srcset="assets/light/contact-linkedin.svg" /><img src="assets/contact-linkedin.svg" width="40%" alt="LinkedIn: in/brian-franck-" /></picture></a>
  <br/>
  <a href="https://www.instagram.com/_brian.franck_/"><picture><source media="(prefers-color-scheme: light)" srcset="assets/light/contact-instagram.svg" /><img src="assets/contact-instagram.svg" width="40%" alt="Instagram: @_brian.franck_" /></picture></a>
  <picture><source media="(prefers-color-scheme: light)" srcset="assets/light/contact-discord.svg" /><img src="assets/contact-discord.svg" width="40%" alt="Discord: username ._.atllas._. (display name Atlas)" /></picture>
</p>

<p align="center">
  <sub>Discord <code>._.atllas._.</code> (Atlas) &nbsp;·&nbsp; Lisbon, Portugal</sub>
</p>
