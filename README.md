# DeepSceneDetect
Machine learning to detect scene changes in video (WIP)

## Training
### Generating training data
`gen.py` is used for generating training data. It does this by cutting up and combining input uncut footage.
The way it is cut up and combined can be fine-tuned programmatically.<!--, code examples are given below. -->

Make sure that the input footage does not have cuts in it. `pre_gen.py` may be used to aid preprocessing using existing scene detection techniques.

---
this README is a work in progress