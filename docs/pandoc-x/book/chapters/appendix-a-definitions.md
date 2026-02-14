# Definitions & Background

This chapter includes all the definitions, symbols, and operations frequently
used in the RLHF process, with a quick overview of language models, which is the
guiding application of this book.

## Language Modeling Overview

The majority of modern language models are trained to learn the joint
probability distribution of sequences of tokens (words, subwords, or characters)
in an autoregressive manner. Autoregression simply means that each next
prediction depends on the previous entities in the sequence. Given a sequence of
tokens $x = (x_1, x_2, \ldots, x_T)$, the model factorizes the probability of
the entire sequence into a product of conditional distributions:

$$P_{\theta}(x) = \prod_{t=1}^{T} P_{\theta}(x_{t} \mid x_{1}, \ldots, x_{t-1}).$$
{#eq:llming}

In order to fit a model that accurately predicts this, the goal is often to
maximize the likelihood of the training data as predicted by the current model.
To do so, we can minimize a negative log-likelihood (NLL) loss:

$$\mathcal{L}_{\text{LM}}(\theta)=-\,\mathbb{E}_{x \sim \mathcal{D}}\left[\sum_{t=1}^{T}\log P_{\theta}\left(x_t \mid x_{< t}\right)\right].$$
{#eq:nll}

In practice, one uses a cross-entropy loss with respect to each next-token
prediction, computed by comparing the true token in a sequence to what was
predicted by the model.

Language models come in many architectures with different trade-offs in terms of
knowledge, speed, and other performance characteristics. Modern LMs, including
ChatGPT, Claude, Gemini, etc., most often use **decoder-only Transformers**
[@Vaswani2017AttentionIA]. The core innovation of the Transformer was heavily
utilizing the **self-attention** [@Bahdanau2014NeuralMT] mechanism to allow the
model to directly attend to concepts in context and learn complex mappings.
Throughout this book, particularly when covering reward models in Chapter 5, we
will discuss adding new heads or modifying a language modeling (LM) head of the
transformer. The LM head is a final linear projection layer that maps from the
model's internal embedding space to the tokenizer space (a.k.a. vocabulary).
We'll see in this book that different "heads" of a language model can be applied
to fine-tune the model to different purposes -- in RLHF this is most often done
when training a reward model, which is highlighted in Chapter 5.
