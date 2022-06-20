from typing import Any, Union, Optional, Tuple, Dict, List
from numbers import Number
from omegaconf import DictConfig

def scale_logging_rates(d: DictConfig, c: Number, strs: Tuple[str] = ('log', 'every_n_steps'), prefix: str = 'config'):
    if c == 1:
        return
    for k, v in d.items():
        if all([s in k for s in strs]):
            d[k] = type(v)(v * c)
            print_once(f'Scaling {prefix}.{k} from {v} to {type(v)(v * c)} due to gradient accumulation')
        elif isinstance(v, DictConfig):
            scale_logging_rates(v, c, strs, prefix=prefix + '.' + k)