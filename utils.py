def add_escape_seq(codes,str):
    """`codes` would be the string between here => '\\033[(`codes`)'.
    For example: 31;1m to make the terminal output red and bold text"""
    return f"\033[{codes}{str}\033[0m"