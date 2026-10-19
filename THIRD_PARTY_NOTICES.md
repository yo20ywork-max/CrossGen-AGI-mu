# Third-party components

CrossGen-AGI-μ is developed by 跨世代媒體科技股份有限公司, Taiwan.
The inference core is based on Qwen2.5-Coder-7B-Instruct, revision
`c03e6d358207e414f1eca0bb1891e29f1db0e242`, under Apache-2.0.
The original model license and provenance notice are in `model-notices/`.
This provenance record is separate from the product's conversational identity.

The Windows distribution includes third-party components such as Python,
PySide6 / Qt, Playwright, faster-whisper, CTranslate2, PyAV, OpenCC and sounddevice.
Keep the complete `_internal` directory, including bundled license records.
PySide6 / Qt retain applicable LGPL/GPL/commercial licensing terms.
The speech component uses Systran/faster-whisper-small; see
`docs/VOICE_MODEL_MANIFEST.json` for its recorded revision and file hashes.
Ollama and Chromium are downloaded separately by the installer and retain their
original licenses. No external model or software license is replaced by the
product-source copyright notice.
