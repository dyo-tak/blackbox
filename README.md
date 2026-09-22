# blackbox

**A replay debugger + observability platform for non-generative AI decisions.**

AI apps make thousands of micro-decisions every day — classify, score, verify, route — and then the probabilities vanish. LLM tracing tools (LangSmith, Langfuse) exist, but nothing is built for *System-1 decision models* (typed decision engines like Laya/Jev that return probabilities instead of text).

This project is the black box for those decisions.

## What it does
- **Record** — event-source every decision: state, questions, raw probabilities, confidence, model version, outcome.
- **Replay** — time-travel debug: re-run any historical decision against a new model version and diff the results (which decisions flip?).
- **Calibrate** — reliability curves, Brier score, ECE: does "92% confident" actually mean 92% right?
- **Detect drift** — calibration metrics over time windows; alert when confidence stops matching reality.

## Status
🚧 Early — scaffold created. See ROADMAP below.

## Roadmap
- [ ] Recorder client + SQLite event store (schema v1)
- [ ] Calibration report (Brier / ECE / reliability curves)
- [ ] Drift detection across time windows
- [ ] Replay engine + model-version diff table
- [ ] Dashboard + demo workload (Discord bot decisions)
- [ ] First Hinglish eval set as a bundled dataset

## Stack
Python 3.11 · SQLite · FastAPI · scikit-learn (calibration) · ONNX Runtime (Laya inference)

## License
MIT
