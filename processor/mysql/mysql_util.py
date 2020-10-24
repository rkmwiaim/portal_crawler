from functional import seq


def escape_single_quote(d: dict) -> dict:
    return seq(d.items()).map(lambda t: (t[0], t[1].replace("'", "''"))).to_dict()
