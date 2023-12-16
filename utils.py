def add_escape_seq(codes,str):
    """`codes` would be the string between here => '\\033[(`codes`)'.
    For example: 31;1m to make the terminal output red and bold text"""
    return f"\033[{codes}{str}\033[0m"
def pascal_case_with_space(str:str):
    """Get slices of PascalCaseWords to then place spaces between them (becomes 'Pascal Case Words')"""
    slices:[(int,int)]=[]
    slice_begin:int=0
    for i,ch in enumerate(str):
        if ch.isupper():
            slices.append((slice_begin,i))
            slice_begin=i
    if len(slices)==0 or slices[-1][0]!=len(str)-1:
        slices.append((slice_begin,len(str)))
    return " ".join([str[sl[0]:sl[1]] for sl in slices]).strip()