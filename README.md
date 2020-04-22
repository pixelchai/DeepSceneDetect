# DeepSceneDetect
Using machine learning to detect scene changes in video (WIP)

## Training
### Generating training data
`gen.py` is used for generating training data. It does this by cutting up and combining input uncut footage,
which you should provide the program with in `data/input/`. 
Note: training data is not included in this repo.

This process can be fine-tuned<!--, as shown in the code examples below. -->

Make sure that the input footage does not have cuts in it. `pre_gen.py` may be used to aid preprocessing using existing scene detection techniques.

---
this README is a work in progress