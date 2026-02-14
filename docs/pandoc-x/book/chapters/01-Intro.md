# Introduction

This PDF is an example of using Pandoc to build LaTex/PDF documents from
Markdown sources.

It has all the features of book or article formats ready for publishing: title,
author, abstract, table of contents (with links), numbered chapters and
sections, bibliography (with references), appendix, code blocks with syntax
highlighting and line numbers, as well as equations, figures, and tables with
cross-references (and links).

At the same time, the source Markdown files are straightforward and readable
with Markdown Preview showing properly rendered equations, figures, and tables.
That makes source Markdown files to be proper documentation in itself while
serving as the source for the PDF.

This example is based
on [pandoc-book-template](https://github.com/wikiti/pandoc-book-template).

It also borrows freely from the approach used by Nathan Lambert for his book
"Reinforcement Learning from Human Feedback"
in <https://github.com/natolambert/rlhf-book/tree/main/book>.

_As a side note, the "Reinforcement Learning from Human Feedback" by Nathan
Lambert <https://rlhfbook.com/> is an excellent book written by a top expert in
the field of RLHF. It is not just very informative but also a delight to read.
Read this book to get a sense of where the present cutting-edge AI research is
going._

## Implementation Example

Implementing the reward modeling loss is quite simple. More of the
implementation challenge is on setting up a separate data loader and inference
pipeline. Given the correct dataloader with tokenized, chosen, and rejected
prompts with completions, the loss is implemented as:
```python
import torch.nn as nn

# inputs_chosen / inputs_rejected include the prompt tokens x and the respective
# completion tokens (y_c or y_r) that the reward model scores jointly.
rewards_chosen = model(**inputs_chosen)
rewards_rejected = model(**inputs_rejected)

loss = -nn.functional.logsigmoid(rewards_chosen - rewards_rejected).mean()
```

As for the bigger picture, this is often within a causal language model that has
an additional head added (and learned with the above loss) that transitions from
the final hidden state to the score of the inputs. This model will have a
structure as follows:

```python {.numberLines}
import torch
import torch.nn as nn
import torch.nn.functional as F


class BradleyTerryRewardModel(nn.Module):
    """
    Standard scalar reward model for Bradley-Terry preference learning.

    Usage (pairwise BT loss):
        rewards_chosen = model(**inputs_chosen)    # (batch,)
        rewards_rejected = model(**inputs_rejected)  # (batch,)
        loss = -F.logsigmoid(rewards_chosen - rewards_rejected).mean()
    """

    def __init__(self, base_lm):
        super().__init__()
        self.lm = base_lm  # e.g., AutoModelForCausalLM
        self.head = nn.Linear(self.lm.config.hidden_size, 1)

    def _sequence_rep(self, hidden, attention_mask):
        """
        Get a single vector per sequence to score.
        Default: last non-padding token (EOS token); if no mask, last token.
        hidden: (batch, seq_len, hidden_size)
        attention_mask: (batch, seq_len)
        """

        # Index of last non-pad token in each sequence
        # attention_mask is 1 for real tokens, 0 for padding
        lengths = attention_mask.sum(dim=1) - 1  # (batch,)
        batch_idx = torch.arange(hidden.size(0), device=hidden.device)
        return hidden[batch_idx, lengths]  # (batch, hidden_size)

    def forward(self, input_ids, attention_mask):
        """
        A forward pass designed to show inference structure of a standard reward model.
        To train one, this function will need to be modified to compute rewards from both
         chosen and rejected inputs, applying the loss above.
        """
        outputs = self.lm(
            input_ids=input_ids,
            attention_mask=attention_mask,
            output_hidden_states=True,
            return_dict=True,
        )
        # Final hidden states: (batch, seq_len, hidden_size)
        hidden = outputs.hidden_states[-1]

        # One scalar reward per sequence: (batch,)
        seq_repr = self._sequence_rep(hidden, attention_mask)
        rewards = self.head(seq_repr).squeeze(-1)

        return rewards
```

