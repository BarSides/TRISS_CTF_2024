#!/usr/bin/env python

import argparse
from base64 import b64encode


def b64_script(s: bytes, flag: str = None) -> bytes:
    flag = f"flag: '{flag}'" if flag is not None else ""
    return f"""#!/usr/bin/env python3
import base64
{flag}
exec(base64.b64decode({str(b64encode(s))}).decode())
""".encode("utf-8")


def get_options(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int)
    parser.add_argument('-f', type=int)
    parser.add_argument('--flag')
    parser.add_argument('script')
    parser.add_argument('output')
    return parser.parse_args(argv)


def main(argv=None):
    options = get_options(argv)

    n, f = options.n, options.f
    flag = f"Barsides{{{options.flag}}}"

    assert f > 0 and n > 0 and n > f, f"invalid: {f} {n}"

    with open(options.script, 'rb') as fh:
        py_code = fh.read()

    for n in range(options.n):
        py_code = b64_script(py_code, flag if n == f else None)

    with open(options.output, 'w') as fh:
        fh.write(py_code.decode())


if __name__ == '__main__':
    main()
