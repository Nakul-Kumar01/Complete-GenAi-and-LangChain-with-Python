

"""
###  How LLM works ??

- GPT : generatice pre-trained transformer
G - to generate new content
P - by its pre trained data
T - special type of neural networks architecture hai, which can generate new text  -> uses attention mechanism
    attention mechanism : allows LLMs to establish relationships b/w multiple words in an input
    ex. The Bank was too steep to climb     -> now whether it is Financial Bank or river Bank  -> decided by attention mechanism


- basiclly Transformer krta kya hai :

we finally sat  -> Transformer -> it predict the next word
we finally sat  -> Transformer -> again it will predict the next word




## Tokens & Tokenization 

who is PM of india  (break this into chunks) -> ["who" , "is", "PM", "of" , "india"] (these are tokens)

["who" , "is", "PM", "of" , "india"] (these are tokens)  -> assign unique token id to each word(each llm has its own dictionary for this)

so we get ,say,  [15, 20 , 52, 45, 107]  now these numbers can be understood by the LLM
and LLM will predict the next number for this 

This process is called Tokenization



## Context window :
- how much data we can send to any LLM model & how much data we can get from any LLM model

"""