# 非空输入
def no_empty_input(prompt_text):
    input_str = input(prompt_text)
    while not input_str:
        input_str = input("输入不能为空, " + prompt_text)
    return input_str


def command_input(command_dict):
    """
    输入给定的指令, 若输入不再指令中, 要求重新输入
    :param command_dict: 指令字典
    :return: 输入的有效指令
    """
    prompt = "请选择一下操作指令:"
    for key, value in command_dict.items():
        prompt = f"{prompt}\n\t{key} - {value}"
    prompt = f"{prompt}\n请输入操作指令: "
    op_type = input(prompt)
    while not op_type in command_dict.keys():
        op_type = input("指令无效, 请重新输入:")
    return op_type
