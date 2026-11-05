<div align="center">

<img src="https://capsule-render.vercel.app/api?type=venom&color=0:0a192f,50:0e7490,100:22d3ee&height=260&section=header&text=BRIAN&fontSize=90&fontColor=ffffff&fontAlignY=42&desc=where%20medicine%20meets%20machine%20learning&descAlignY=66&descSize=20&animation=twinkling" width="100%" alt="header"/>

<img src="assets/ecg.svg" width="100%" alt="ECG line"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=20&duration=3200&pause=1000&color=22D3EE&center=true&vCenter=true&width=780&lines=%24+python+brian.py;Loading+medicine...+done.;Loading+machine+learning...+done.;Teaching+models+to+read+what+doctors+see." alt="Typing SVG" />
</a>

</div>

<br/>

```text
$ python brian.py

  ┌──────────────────────────────────────────────┐
  │  BSc Computational Biomedicine & AI          │
  │  Universidade Lusófona                       │
  │  + day job: writing code, remotely           │
  └──────────────────────────────────────────────┘

  > Goal: use AI to help medicine see more in its own data.
```

<br/>

## 🧠 `model.summary()`

If I were a neural network, this is roughly what I'd look like:

```text
Model: "Brian_v1.0"
_____________________________________________________________________
 Layer (type)                What it learns                  Status
=====================================================================
 medicine_input   (Input)    Biomedicine, biology, clinical   ✔ loaded
 python_core      (Dense)    Python · SQL · R · C             ✔ trained
 data_layer       (Dense)    Pandas · NumPy · stats           ✔ trained
 deep_learning    (Conv2D)   PyTorch · TensorFlow             ◐ training
 med_imaging      (Attn)     Pathology · MIL · CLAM           ◐ training
 biosignals       (LSTM)     ECG auditing & preparation       ◐ training
 biosensors       (Dense)    Optical & acoustic sensing       ◐ exploring
=====================================================================
 output           (Softmax)  AI researcher in medicine        ➜ loading...
_____________________________________________________________________
```

<br/>

## 🔬 What I'm building: a slide-to-diagnosis pipeline

My main project teaches a model to grade prostate cancer biopsies, aiming at the tricky **Gleason Grade 2 vs 3** boundary, using the PANDA dataset.

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#0a192f','primaryTextColor':'#e5e7eb','primaryBorderColor':'#22d3ee','lineColor':'#22d3ee','fontFamily':'monospace'}}}%%
flowchart LR
    A["🧫 Biopsy slide<br/>gigapixel image"] --> B["🔲 Patches<br/>thousands of tiles"]
    B --> C["🧠 ResNet-50<br/>feature extraction"]
    C --> D["🎯 CLAM attention<br/>which tiles matter?"]
    D --> E["🩺 Gleason grade<br/>ISUP 2 vs 3"]
```

The idea behind Multiple Instance Learning: a slide has only one label, but thousands of patches. The model learns **where to look**, the way a pathologist does.

<br/>

## 📡 Live log

```text
[done]  Medical AI project    ->  CLAM-style MIL for Gleason grading
[run ]  Clinical ECG data     ->  auditing & preparing signals for analysis
[run ]  Fiber-optic sensing   ->  label-free biosensors & compact ultrasound probes
[run ]  Medical imaging       ->  digging deeper every week
[todo]  More projects         ->  Python · C++ · C · Linux
[todo]  Career                ->  AI/ML research & engineering
```

<br/>

<div align="center">

<img src="https://skillicons.dev/icons?i=py,pytorch,tensorflow,r,c,linux,git,github,vscode&theme=dark" alt="stack"/>

<br/><br/>

<img height="165" src="https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME&show_icons=true&theme=dark&bg_color=0a192f&title_color=22d3ee&icon_color=22d3ee&text_color=e5e7eb&border_color=0e7490" alt="stats"/>
<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=YOUR_USERNAME&layout=compact&theme=dark&bg_color=0a192f&title_color=22d3ee&text_color=e5e7eb&border_color=0e7490" alt="top languages"/>

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0a192f?style=for-the-badge&logo=linkedin&logoColor=22d3ee)](https://linkedin.com/in/YOUR_HANDLE)
[![Email](https://img.shields.io/badge/Email-0a192f?style=for-the-badge&logo=gmail&logoColor=22d3ee)](mailto:YOUR_EMAIL)

<img src="assets/ecg.svg" width="100%" alt="ECG line"/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:22d3ee,50:0e7490,100:0a192f&height=110&section=footer" width="100%" alt="footer"/>

</div>
