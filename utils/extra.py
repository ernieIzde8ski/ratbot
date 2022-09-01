def codeblock(string: str, lang: str | None = None):
    return f"```{lang or ''}\n{string.rstrip()}\n```"
