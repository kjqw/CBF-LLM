# CBF-LLM Modules
from torch_utils import *
from filter import Filter, FilterResult, get_next_CLF_list
from language_constraint_functions import LanguageCF
# Other Modules
from typing import Any
from transformers import PreTrainedTokenizerBase
# PyTorch
import torch
Tensor = torch.Tensor
zeros = torch.zeros
float32 = torch.float32


class CBFFilter(Filter):
    def __init__(
        self,
        top_k: int,
        alpha: float,
        tokenizer: PreTrainedTokenizerBase,
        lcf: LanguageCF,
        chunk_size: int = 32
    ) -> None:
        """
        Parameters
        ----------
        top_k: int
            生成パラメータトップk
        alpha: float
            CBFパラメータα
        tokenizer: PreTrainedTokenizerBase
            生成言語モデルのトークナイザ
        clf: LanguageCF
            制約言語関数
        chunk_size: int=32
            制約言語関数へ問い合わせる際のチャンクサイズ
        """
        self.top_k = top_k
        if alpha == 1.0:
            print("alpha=1は`BlacklistFilter`と等価であり，そちらを使う方がパフォーマンスが高いです．")
        self.alpha = alpha
        self.tokenizer = tokenizer
        self.lcf = lcf
        self.chunk_size = chunk_size

        self.vocab_size = len(tokenizer.get_vocab())
        self.all_disallowed_Q = zeros((self.vocab_size,), dtype=float32)
        self.one_minus_alpha = 1. - alpha

        self.chunk_size = chunk_size

    def scan(self, x: Tensor, P: Tensor) -> Any:
        assert (P.sum() - 1.0).abs() < 1e-5, f"Sum of input distribution P = {
            tofloat(P.sum())}, expected around 1."
        R = FilterResult()

        xstr = self.tokenizer.decode(x)
        hx = self.lcf.get_for_text(xstr)
        A = self.one_minus_alpha * hx

        sorted_next_tokens = P.argsort(descending=True)

        chunk_idx = 0
        searched_cnt = 0
        allowed_cnt = 0
        while allowed_cnt < self.top_k and searched_cnt < self.vocab_size:
            offset = self.chunk_size * chunk_idx
            chunk_next_token_list = sorted_next_tokens[offset:offset+self.chunk_size]
            chunk_next_h_list = get_next_CLF_list(
                x, chunk_next_token_list, self.tokenizer, self.lcf)

            for t, h in zip(tolist(chunk_next_token_list), chunk_next_h_list):
                R.clf_mapping[t] = h
                if h >= A:
                    R.allowed.append(t)
                    allowed_cnt += 1
                    if allowed_cnt >= self.top_k:
                        break
                else:
                    R.disallowed.append(t)
                searched_cnt += 1
            chunk_idx += 1
        return R
