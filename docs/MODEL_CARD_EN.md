---
language:
  - zh
  - en
pipeline_tag: text-generation
tags:
  - crossgen
  - taiwan
  - traditional-chinese
  - gguf
  - lora
  - qlora
  - computer-use
  - development-preview
library_name: gguf
---

# CrossGen-AGI-μ v0.1

**Developed in Taiwan by 跨世代媒體科技股份有限公司.**

CrossGen-AGI-μ is a product designed for interaction in Taiwanese Traditional Chinese, coding-oriented reasoning, and computer task execution. This repository archives the **v0.1 meeting demonstration build**: a Windows desktop executable, a GGUF base model, the v13 epoch3 LoRA adapter, and traceable build and training summaries.

**Status: development preview; full release acceptance criteria have not been met.** AGI is part of the product name, not a claim that artificial general intelligence has been achieved or that arbitrary on-screen tasks can be completed. This card distinguishes completed training, historical research, software checks, and unfinished work.

## Downloads and quick start

| File | Contents | Usage |
|---|---|---|
| [Windows executable archive](https://huggingface.co/yoxia/CrossGen-AGI-mu-v0.1/resolve/main/CrossGen-AGI-mu-v0.1-Windows.zip) | Desktop application, runtime dependencies, setup scripts, and instructions | Extract the entire archive; do not move the EXE by itself |
| [Base model GGUF](https://huggingface.co/yoxia/CrossGen-AGI-mu-v0.1/resolve/main/models/CrossGen-core-Q4_K_M.gguf) | 4,683,074,048 bytes; Q4_K_M inference base | Use with the LoRA adapter below |
| [v13 epoch3 LoRA GGUF](https://huggingface.co/yoxia/CrossGen-AGI-mu-v0.1/resolve/main/models/CrossGen-v13-e3-LoRA.gguf) | 322,988,800 bytes; fine-tuned adapter weights | Not a standalone model; requires the base model |
| [System prompt](https://huggingface.co/yoxia/CrossGen-AGI-mu-v0.1/resolve/main/system-prompt.txt) | Default product identity and response instructions | Optional for the llama.cpp chat interface |
| [Complete setup guide](https://huggingface.co/yoxia/CrossGen-AGI-mu-v0.1/blob/main/QUICKSTART.md) | Windows, Ollama, and llama.cpp instructions | Guide for the demonstration computer; written in Traditional Chinese |
| [Build manifest and checksums](https://huggingface.co/yoxia/CrossGen-AGI-mu-v0.1/blob/main/DELIVERY_MANIFEST.json) | EXE, ZIP, and GGUF SHA256 values | Verify downloaded files |
| [Training evidence summary](https://huggingface.co/yoxia/CrossGen-AGI-mu-v0.1/blob/main/TRAINING_EVIDENCE.json) | Recorded training results, configuration, and data distribution | Technical review |
| [Application source snapshot](https://huggingface.co/yoxia/CrossGen-AGI-mu-v0.1/resolve/main/CrossGen-source-snapshot.zip) | Product source and executable build entry point | Private backup; excludes credentials and personal browser data |

The repository is private. Downloads require an authorized Hugging Face account. The executable does not require a separate Python installation, but its inference engine uses Ollama. The GGUF files can also be used directly with a LoRA-capable llama.cpp build; these are independent deployment options.

```powershell
.\llama-server.exe -m "models/CrossGen-core-Q4_K_M.gguf" --lora "models/CrossGen-v13-e3-LoRA.gguf" -c 4096 -ngl 28 --host 127.0.0.1 --port 8080
```

This command is a starting configuration for 6GB VRAM, not a configuration validated on the RTX 4050. Reduce the number of offloaded layers if memory is insufficient. Once the server starts, open `http://127.0.0.1:8080`. This release does not include a newly merged and requantized single-file model. It preserves the two verified files so that a new conversion is not mistaken for the previously evaluated weights. [llama.cpp project](https://github.com/ggml-org/llama.cpp)

## 1. Product identity

| Field | Value |
|---|---|
| Product | CrossGen-AGI-μ |
| Developer, registered company name | 跨世代媒體科技股份有限公司 |
| Origin | Taiwan |
| Company type | Startup company |
| Incorporation approval date | 2026-08-10 |
| Employee count | Not publicly disclosed; the wording “not yet finalized” is also accepted, without inferring a number |
| Primary interaction language | Taiwanese Traditional Chinese, preserving user-specified code, paths, and quotations |

Product identity is represented in both training data and deployment defaults. These are evaluated separately: a neutral system prompt supplies no brand answers and tests behavior learned in the weights; the deployment system prompt supplies consistent product information. General tasks should not be overwritten by unsolicited self-introductions. This work adapts an existing approximately 7.6B-parameter coder base and integrates it into a product; it is not pretraining from scratch. Technical provenance and required licensing information are kept separately in `model-notices/` and are not automatically inserted into model conversations.

## 2. Traceable research and training history

1. **Pilot stage:** bounded positive-direction training, error-direction training, and subtractive combinations were actually performed. Reload checks, hashes, and quality results were retained. A change in weights alone was not treated as release readiness.
2. **Earlier formal candidates:** historical experiments investigated SFT, DPO, different initializations, and equal-weight merging. Trained candidates and unused drafts were recorded separately. Some earlier identity and provenance-response requirements were withdrawn following changes in user requirements and must not be reinstated in this version.
3. **Product contracts and execution evidence:** development addressed tool JSON, negation and conditional branches, actual read/write evidence, complete file reads, replanning after failures, and final response delivery. These software and data changes do not each constitute a new weight-training run.
4. **Formal v13 training:** 1,799 rows were frozen and trained for three complete epochs on two GPUs. All 675 planned optimizer updates completed. Per-epoch weights, cross-device parameter agreement, and reload evidence were retained.
5. **Deployment diagnostics:** native adapter execution was compared with local GGUF inference. A corrupted local Ollama adapter blob was discovered and repaired. Subsequent evaluations added checks of actual model files before and after inference.
6. **v0.1 archival build:** this package preserves the v13 epoch3 candidate used in ongoing diagnostics. Another 256 content-training rows and 32 development evaluation cases have been prepared but **were not used to retrain this version**. The 32 cases have not yet been evaluated with the model.

This history is based on existing training receipts and source code. It does not equate every directory version with an independent completed training run, and it does not discard historical failures. Unless otherwise stated, numerical results below refer to v13, rather than a selection of the best scores across unrelated experiments.

## 3. Training data composition

The actual v13 training set contains **1,799 rows**: 1,633 existing rows plus 88 identity examples without answer cues, 28 action contrasts, and 50 history/quotation contrasts. The table describes the final dataset; its counts must not be added again to the augmentation counts.

| Category | Rows |
|---|---:|
| Tool planning: tools | 390 |
| Completion judgment: completion | 484 |
| Recovery and replanning: recovery | 114 |
| Programming: code | 241 |
| Taiwanese language usage: locale | 46 |
| ASR text repair: asr | 70 |
| Calibration: calibration | 20 |
| Historical events and evidence: history | 94 |
| Literal preservation: literal | 58 |
| Source-grounded answers: grounded | 46 |
| Negation: negation | 32 |
| Conditional planning: conditional_plan | 84 |
| Product identity: identity | 120 |
| **Total** | **1,799** |

Of these, 273 rows carry a capability-retention flag. The `asr` category concerns text repair and understanding; it does not mean that an acoustic speech-recognition model was fine-tuned. Tokenization uses only `system`, `prompt`, and `answer`. Categories, source URLs, authors, licenses, and audit sidecars are not serialized into model inputs. Quotations, code, and factual evidence required by the task itself are preserved.

For example i, define:

$$x_i=\operatorname{ChatTemplate}(s_i,u_i),\qquad y_i=\operatorname{AssistantAnswer}_i.$$

Inputs use the original tokenizer's chat template. The full sequence including the assistant answer must match the generation prefix token by token. Overlength examples must not be silently truncated. This version does not expand the vocabulary as part of product-identity or Taiwanese-language adaptation.

## 4. Training objective: assistant-only SFT

Labels for system and user tokens are ignored. Only the assistant answer contributes to the supervised loss. Let \\(A_i\\) denote the valid answer positions in row i:

$$\ell_i(\theta)=-\frac{1}{|A_i|}\sum_{t\in A_i}\log p_\theta(y_{i,t}\mid x_i,y_{i,<t}).$$

The global batch uses a mean over sequences, rather than automatically giving more weight to rows with longer answers:

$$\mathcal L_{\mathrm{SFT}}(\theta)=\frac{1}{|\mathcal B|}\sum_{i\in\mathcal B}\ell_i(\theta).$$

This objective encourages the specified answers. Training loss alone cannot distinguish memorization from generalization or establish that desktop tasks can be completed. Separate evaluations therefore cover functional code, conditional branches, source text, actual files, and identity under a neutral system prompt.

## 5. LoRA and quantized training

The base weights \\(W_0\\) remain frozen while a low-rank update is trained:

$$W=W_0+\Delta W,\qquad \Delta W=\frac{\alpha}{r}BA.$$

Here, \\(A\in\mathbb R^{r\times d_{in}}\\) and \\(B\in\mathbb R^{d_{out}\times r}\\). This version uses \\(r=32\\), \\(\alpha=64\\), a scaling factor of \\(\alpha/r=2\\), zero dropout, and PEFT's `all-linear` target selection. For one matrix, the trainable parameter count changes from \\(d_{out}d_{in}\\) under full fine-tuning to:

$$N_{\mathrm{LoRA}}=r(d_{in}+d_{out}).$$

This describes how parameters are updated. It does not prove that the low-rank matrices contain only product-identity information. [LoRA paper](https://arxiv.org/abs/2106.09685)

Training uses 4-bit NF4, double quantization, and BF16 computation. Gradient checkpointing reduces activation memory. Conceptually, the forward computation is:

$$h=\operatorname{dequant}(Q_{\mathrm{NF4}}(W_0))x+\frac{\alpha}{r}BAx.$$

NF4 is the training-time quantization configuration, **not** the Q4_K_M format of the local inference file. Their numerical approximations differ, so native training-backend evaluations do not replace GGUF inference evaluations. This run does not claim to implement every optimization in the QLoRA paper; the implemented optimizer is AdamW. [QLoRA paper](https://arxiv.org/abs/2305.14314)

## 6. Two-GPU global batching and optimization

| Setting | Actual v13 value |
|---|---|
| Base revision | `c03e6d358207e414f1eca0bb1891e29f1db0e242` |
| Random seed | 20260906 |
| Devices | 2; the original training configuration used two A100 GPUs |
| Epochs | 3, all completed |
| Learning rate | 0.00002 |
| Optimizer | Fresh AdamW |
| Global batch | 8 sequences |
| Warmup ratio | 0.05 |
| Maximum sequence length | 12,288 tokens |
| LoRA rank / alpha | 32 / 64 |
| Optimizer updates | 675 / 675 |
| Time recorded by the training program | Approximately 4,065.59 seconds, or 67.76 minutes |

The two devices use a strided partition without duplicating examples to pad device-local batches. For the final batch containing fewer than 8 rows, the denominator is the actual number of sequences:

$$g=\frac{1}{|\mathcal B|}\sum_{k=1}^{K}\sum_{i\in\mathcal B_k}\nabla_\theta\ell_i,\qquad K=2.$$

After the explicit gradient SUM, gradients are not incorrectly divided by the device count again. The number of updates is:

$$N_{\mathrm{updates}}=3\left\lceil\frac{1799}{8}\right\rceil=3\times225=675.$$

This is not a global batch of 16 produced by assigning batch8 to each GPU. Rows are not duplicated because two GPUs are used. Three epochs produce 5,397 sequence presentations, not 5,397 independent examples.

## 7. Capability retention and checkpoint selection

Programming, literal-preservation, and other existing capability examples remain in the SFT mixture. Although the configuration includes a KL field, the actual value is `retention_kl_weight=0.0`. A reference-model KL constraint was therefore not enabled. A general extension can be written as:

$$\mathcal L=\mathcal L_{\mathrm{SFT}}+\lambda\,D_{\mathrm{KL}}(p_{ref}\Vert p_\theta),\qquad \boxed{\lambda=0\text{ in this run}}.$$

Development NLL is summarized using a macro-average across categories:

$$\overline{\mathcal L}_{macro}=\frac{1}{C}\sum_{c=1}^{C}\overline{\mathcal L}_c.$$

| Epoch | Macro dev NLL | Code NLL | Literal NLL |
|---:|---:|---:|---:|
| 1 | 0.211025 | 0.196222 | 0.004388 |
| 2 | **0.175926** | 0.183218 | 0.001177 |
| 3 | 0.179875 | 0.181978 | 0.001128 |

The training program's NLL selector chose **epoch2**. This repository archives **epoch3**, which was used in subsequent product diagnostics. This does not establish that epoch3 is better overall or constitute a completed release-selection decision. Selection still requires actual generation, functional behavior, and full task outcomes; lower loss or a later checkpoint is insufficient.

## 8. Subtractive updates, DPO, and merging: historical research

These methods describe historical research, not the production method used for this adapter. Earlier work explored subtracting an error direction:

$$W_{candidate}=W_0+\beta\Delta W_{correct}-\gamma\Delta W_{error}.$$

\\(\Delta W_{error}\\) is a direction learned from observed error examples, not an isolated set of political-bias neurons. Subtraction may also damage subject knowledge, formatting, or coding ability. The earlier error-direction adapters were not applied to v13 epoch3, and permanent removal of all upstream knowledge has not been demonstrated.

Independently averaging LoRA factor matrices is generally not equivalent to combining their weight updates:

$$\Big(\sum_j a_jB_j\Big)\Big(\sum_j a_jA_j\Big)\ne\sum_j a_jB_jA_j.$$

The expression on the left introduces cross terms. Merging or subtraction should operate on the full \\(\Delta W\\), or a mathematically equivalent block construction, and be revalidated. These equations explain historical methods; they do not imply that this release contains a merged single-file model.

Historical DPO candidates used preferred and rejected answers \\((y^+,y^-)\\) for the same prompt:

$$\mathcal L_{DPO}=-\mathbb E\log\sigma\left(\beta\left[\log\frac{\pi_\theta(y^+|x)}{\pi_{ref}(y^+|x)}-\log\frac{\pi_\theta(y^-|x)}{\pi_{ref}(y^-|x)}\right]\right).$$

DPO and subtractive weight updates are different methods. **The v13 run used SFT with a freshly initialized LoRA adapter; it did not use a DPO loss during these three epochs.** [DPO paper](https://arxiv.org/abs/2305.18290)

## 9. Weight and conversion integrity

The process includes locking data and configuration, a longest-row forward/backward preflight, cross-device parameter agreement, per-epoch saves, reload-logit checks, download hashes, GGUF adapter conversion, and Ollama import. Existing verification for all three native checkpoints is retained; the downloaded artifacts totaled approximately 1.04GB. Training completion was not inferred merely from copying a final file.

Each delivered file is checked using:

$$h_f=\operatorname{SHA256}(\operatorname{bytes}(f))$$

Filenames, sizes, and timestamps are not substitutes for this check. A local Ollama blob previously had the expected filename but corrupted contents; it was restored from a verified backup. The cause remains unknown. Earlier manifest-only records cannot retrospectively establish physical weight integrity. Subsequent model evaluations require matching hashes of actual files before and after inference.

| Artifact | SHA256 |
|---|---|
| Base model | `60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463` |
| Epoch3 LoRA | `2963b2e99d2df37f1393f3d8f16fde8cbeca37469620865ee721997b601c643e` |

Matching hashes establish identical file bytes. They do not establish correct answers, error-free GPU memory, or universal computer-task completion.

## 10. Recorded evaluations and their scope

| Evaluation | Result | Supported conclusion |
|---|---:|---|
| v13 optimizer updates | 675 / 675 | All planned updates across three epochs completed |
| Native epoch3 identity with a neutral system prompt | 16 / 16 | Passed that suite in that native execution environment |
| Local Q4 + epoch3 identity with a neutral system prompt | **15 / 16** | A date-format case returned a JSON string instead of the required object |
| Original eight file tasks under runtime-v9 | **6 / 8; 0 false-completion reports** | Some file tasks completed; the full suite did not pass |
| New eight-case content/operation separation candidate | **3 / 8; 2 false-completion reports** | The candidate is not ready for product integration |
| Operation-obligation extraction candidate | **5 / 24** | Negation, preservation, and ordering remain unreliable |
| Executable packaging checks for this delivery | Actual EXE imports, Qt loading, and UI input checks passed | Does not establish full desktop-task acceptance |
| Deployment identity smoke check for this delivery | Responded with CrossGen-AGI-μ | Uses the product system prompt; does not replace neutral-system testing |

These suites, environments, and versions differ and must not be combined into a single accuracy figure. Offline success of a candidate module does not replace end-to-end product evaluation. Development tests are not an unseen final holdout.

The product's completion criteria require content, operations, delivery, and evidence to agree. The design objective can be expressed as:

$$\operatorname{Complete}=C_{content}\land C_{operations}\land C_{delivery}\land C_{evidence}.$$

This expresses acceptance conditions; it does not mean that every \\(C\\) has a fully reliable implementation. Known failures include rejecting valid translations or code, overlooking source preservation or readback, and incorrectly judging completion for empty files.

## 11. Prepared data not included in this version's training

The new content-contrast component contains 256 rows in 128 pairs, with 128 positive and 128 negative examples: 192 factual-summary rows, 48 coding rows, and 16 status-sentence translation rows. Within each pair, the request, source, and filenames are identical; only the output changes. This reduces opportunities to infer labels from filenames. Earlier versions containing odd/even filename cues were withdrawn.

The actual tokenizer audit found a maximum length of 713 tokens. Answer-mask and truncation checks passed for all 256 rows. Another 32 development cases use different subtasks and templates, including data selection, list-processing code, conditional translation, and constrained writing. **These data have not been used for retraining; model inference on the 32 cases has not yet been run.** They must not be counted as new capabilities already learned by this version.

## 12. Demonstration and usage limitations

- The Windows application uses a one-directory executable package. Keep its `_internal` dependency directory. The initial packaging issue involving an incompatible ICU DLL was fixed, and local checks of the actual executable were retained.
- The target demonstration machine is Windows 11 with an RTX 4050, 6GB VRAM, and 24GB RAM. **Memory use, latency, and stability have not been validated on that machine.** Measurements from another computer are not target-hardware results.
- The voice repair package includes an offline Whisper small speech model and a dedicated Windows speech helper. Recognition runs on CPU INT8; recorded audio stays in memory and is not uploaded. The transcript is inserted into the composer for review before task submission. Vision models are not included. Support for every native application or on-screen action is not claimed.
- The repaired frozen speech helper passed a synthetic zh-TW transcription check, local microphone recording/stop checks, cancellation during recording and before transcription results, and restart after cancellation. The UI insertion/cancellation check uses simulated transcripts. These checks are not a human speech accuracy benchmark or an RTX 4050 hardware acceptance test. See [VOICE_VALIDATION.json](./VOICE_VALIDATION.json). Long-task recovery, native applications, end-to-end performance, and the full set of release gates remain incomplete.
- Historical and political training aims to support evidence-based factual answers. This version does not guarantee unbiased answers to every political question or comprehensive historical fact-checking.
- The executable is not code-signed. Verify the published SHA256 values; disabling antivirus software is unnecessary.
- Ongoing development was paused after this delivery and requires an explicit user request to resume. No cloud GPU was rented for this backup.

## 13. Reproducibility and technical records

Data-lock SHA256: `e8af99592566e41a9cb133e3a8770a1c26a410fe3bbadd73e13003f3b47fdcf6`.

Training-data SHA256: `411adb64906026cc142b5ffed377d45c2349753945c0c5c30f646759947666da`.

Development-data SHA256: `7a4cce9a7b110543db9865d12867d7a99359548ee201189e3bd0bd15156fe6bc`.

Original training sources include `release_v13/config.json`, `train_distributed.py`, `distributed_engine.py`, `distributed_update.py`, and `artifacts/outputs/manifest.json`. This repository's `TRAINING_EVIDENCE.json` summarizes the corresponding values. `DELIVERY_MANIFEST.json` and `MODEL_SMOKE.json` record direct checks of the demonstration package.

This model card is a verifiable technical description, not peer review, a generalization guarantee, or release certification. Its equations explain algorithms and acceptance logic; they do not replace empirical evidence.
