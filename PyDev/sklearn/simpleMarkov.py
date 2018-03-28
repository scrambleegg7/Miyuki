#coding:utf-8

 # simple markov model (HMM)
 
 # 状態変数
states = ('Rainy', 'Sunny')

# 観測列
observations = ['walk', 'shop', 'clean']

# 初期確率
start_probability = {'Rainy': 0.6, 'Sunny': 0.4}
 
# 遷移確率
transition_probability = {
   'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3},
   'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6},
   }

# 出力確率 
emission_probability = {
   'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
   'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
   }

# Forward Algorithm
def forward(y1, prior, states, trans_p, emit_p):
    post = {}
    for x1 in states:
        post[x1] = emit_p[x1][y1] * sum([ trans_p[x][x1] * prior[x] for x in states ])
        print "emit x1:%1.6f" % emit_p[x1][y1]
        print "post x1:%1.6f" % post[x1]
    s = sum(post.values())
    for k,v in post.items():
        post[k] = v/s
    return post

# Filtering
def filtering(observations, states, start_p, trans_p, emit_p):
    prior = start_p
    T = len(observations)
    for t in range(T):
        post = forward( observations[t], prior, states, trans_p, emit_p )
        prior = post
    return post

print filtering(observations, states, start_probability, transition_probability, emission_probability)  