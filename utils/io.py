import os
from typing import Optional
from pathlib import Path
from inputimeout import inputimeout, TimeoutOccurred


from .distributed import print_once

def resolve_resume_id(log_dir: str, id: str, **kwargs) -> str:
    if id == "latest_run":
        base_path = Path(log_dir).absolute()
        latest_id = os.readlink(next((base_path / "wandb").glob('*latest-run*')))[-8:]
        print_once(f'Resuming from latest run: {latest_id}')
        return latest_id
    return id

def yes_or_no(q: str, default: Optional[bool] = None, timeout: Optional[int] = None) -> bool:
    assert not (timeout is not None and default is None), 'If using timeout, must set default value.'
    q = f"{q} [{'Y' if default is True else 'y'}/{'N' if default is False else 'n'}]: "
    if timeout is not None:
        def input_fn(prompt):
            try:
                return inputimeout(prompt=prompt, timeout=timeout)
            except TimeoutOccurred:
                print(f'Input timed out. Using default value of {default}.')
                return ''
    else:
        input_fn = input
    a = input_fn(q).lower().strip()
    print("")
    valid = ['y', 'n', 'yes', 'no']
    if default is not None:
        valid.append('')
    while a not in valid:
        print("Input yes or no")
        a = input_fn(q).lower().strip()
        print("")
    if a == "":
        return default
    elif a[0] == "y":
        return True
    else:
        return False    