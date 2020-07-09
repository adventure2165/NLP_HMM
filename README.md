Hidden Markov Model & Viterbi Algorithm
========
# 1. Hidden Markov Model을 이용하여 문장에 다음에 특정 태그가 등장할지에 대해서 여부를 학습하고 예측하는 Code
사용한 데이터는 출처를 공개할 수 없는 관계로 업로드 하지 아니하였음.

# 2. 비터비 알고리즘 구현
HMM을 기반으로 사용되는 Viterbi Algorithm을 간단하게 구현하였음. 이를 위해 Reference Repo에서 관련 자료를 참조하였고, 코드 구현시 코드 참조를 하였으며 해당 reference는 따로 적어둠.

# 3. 유의사항
Reference Repo에 있는 자료대로 계산한다면 출력을 "Sunny", "Rainy"로 설정할 때 "Sunny", "Rainy", "Rainy" 와 같은 결과가 나온다고 설명하고 있다. 하지만 본인이 돌려본 결과 Sunny", "Rainy", "Sunny" 가 나왔다. 이는 자료가 계산 실수를 한 것으로 추정되며, 자세한 내용은 추후 직접 계산을 진행하여 올리기로 하겠다.

## Reference Repo
- http://www.davidsbatista.net/assets/documents/posts/2017-11-12-hmm_viterbi_mini_example.pdf : theory reference
- https://github.com/WuLC/ViterbiAlgorithm : Code Reference

## 참조하면 좋은 사이트
- https://ratsgo.github.io/data%20structure&algorithm/2017/11/14/viterbi/
- https://yujuwon.tistory.com/entry/TENSORFLOW-HMM-viterbi-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98