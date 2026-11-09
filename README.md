<div align="center">

<img src="assets/hero.svg" width="100%" alt="BRIAN.LAB: Brian Franck, also known as Atlas, BSc student in Computational Biomedicine & AI at Universidade Lusófona. Now building Iris, a Gleason grading AI." />

</div>

<p align="center">
  <b>Hi, I'm Brian</b>, or <b>Atlas</b> online. I'm a <b>Computational Biomedicine &amp; AI</b> student at <b>Universidade Lusófona</b> in Lisbon.<br/>
  I'm interested in the place where medicine and machine learning meet: models that learn from slides, signals and sensors.
</p>

<p align="center">
  <sub>NOW BUILDING&nbsp;&nbsp;→&nbsp;&nbsp;<b>IRIS</b>, an AI that grades prostate biopsies and shows where it looked. The goal is to grow it into a company.</sub>
</p>

<br/>

<div align="center">

<img src="assets/iris.svg" width="100%" alt="Project 01, Iris: Gleason grading of prostate biopsies with CLAM attention multiple instance learning on the PANDA dataset, targeting the ISUP grade 2 vs 3 boundary. Stage: early R&D." />

<br/>

<img src="assets/iris-vision.svg" width="100%" alt="Iris vision, a concept mock-up with illustrative values: a biopsy with an attention heatmap, a grade distribution and a send-to-pathologist button. Mission: a second reader for every prostate biopsy. The plan: research (now), prototype, validation, pilot, and a company as the goal." />

</div>

<details>
<summary><b>&nbsp;Iris: what it is, where it's going, and why the name</b></summary>

<br/>

**The problem.** Prostate biopsies are graded with the Gleason system and grouped into ISUP grade groups (1 to 5). The grade drives treatment, yet pathologists often disagree, especially between **ISUP 2 (Gleason 3+4)** and **ISUP 3 (Gleason 4+3)**. That call can decide whether active surveillance is still on the table.

**The idea.** A whole-slide image is gigapixel-sized and comes with a single label. Iris treats each slide as a bag of thousands of tiles and uses **attention-based multiple instance learning ([CLAM](https://github.com/mahmoodlab/CLAM))** to learn which tiles drive the grade. Its attention map becomes a heatmap a pathologist can check, so the answer is never just a number.

**Where it's going.** I'm building Iris with the goal of turning it into a company: a second reader that helps pathologists grade prostate biopsies faster and more consistently, and always shows its reasoning. Today it's in early R&D, and the first step is a model that earns trust on public data.

**Roadmap**

- [ ] **Data:** [PANDA](https://www.kaggle.com/c/prostate-cancer-grade-assessment) slides and labels, tissue masking, tile extraction
- [ ] **Baseline:** ResNet-50 tile features with simple mean/max pooling
- [ ] **Iris v1:** CLAM attention MIL on the same features
- [ ] **Evaluation:** quadratic weighted kappa on ISUP 0 to 5, with a focused look at the 2 vs 3 split
- [ ] **Explainability:** attention heatmaps overlaid on the slide
- [ ] **Write-up:** open code, results and what didn't work

**Beyond the model**

- [ ] **Validation:** external datasets and feedback from practising pathologists
- [ ] **Pilot:** a second-reader workflow tested with a pathology lab
- [ ] **Company:** build Iris into a company

**Why "Iris"?** The iris is the part of the eye that decides how much light gets in. Iris does the same for a biopsy: out of thousands of tiles, it decides which ones deserve attention, and it shows you where it looked.

<sub>Iris is in early research and development. It is not a medical device and is not cleared for clinical use.</sub>

</details>

<br/>

<div align="center">

<img src="assets/ecg-audit.svg" width="100%" alt="Project 02, ECG audit: cleaning clinical ECG data by flagging missing values, lead-off segments, drift and noise before any model sees it." />

<br/>

<img src="assets/fiber-optic.svg" width="100%" alt="Project 03, fiber-optic sensing: label-free optical biosensing where sound shifts the phase of light in a fiber, enabling compact EMI-immune ultrasound probes." />

<br/>

<img src="assets/processes.svg" width="100%" alt="Process table of what I'm working on: BSc in biomedicine and AI (running), Iris Gleason grading (building), ECG audit (running), optoacoustic sensing (research), medical imaging (learning), Python (running)." />

<br/>

<img src="assets/toolchain.svg" width="100%" alt="Toolchain as a constellation. Systems: Python (advanced), Linux, Git and GitHub, C. Data: pandas and NumPy, SQL, R, data visualization with Matplotlib and Seaborn. Machine learning: PyTorch, TensorFlow." />

</div>

<br/>

<p align="center">
  <b>Let's talk</b> about computational pathology, biosignals, Iris or anything where medicine meets machine learning.<br/>
  <sub>Lisbon, Portugal</sub>
</p>

<p align="center">
  <a href="mailto:brianferrarif@gmail.com?subject=Hi%20Brian"><img src="assets/contact-email.svg" width="32%" alt="Email: brianferrarif@gmail.com" /></a>
  <a href="https://www.instagram.com/_brian.franck_/"><img src="assets/contact-instagram.svg" width="32%" alt="Instagram: @_brian.franck_" /></a>
  <img src="assets/contact-discord.svg" width="32%" alt="Discord: username ._.atllas._. (display name Atlas)" />
</p>

<p align="center">
  <sub>Email <a href="mailto:brianferrarif@gmail.com">brianferrarif@gmail.com</a> &nbsp;·&nbsp; Instagram <a href="https://www.instagram.com/_brian.franck_/">@_brian.franck_</a> &nbsp;·&nbsp; Discord <code>._.atllas._.</code> (Atlas)</sub>
</p>

<br/>

<div align="center">

<img src="assets/footer.svg" width="100%" alt="Built with Python, curiosity and a lot of data." />

</div>
