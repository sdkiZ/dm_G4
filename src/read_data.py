#各種ファイル読み込みの関数モジュール

CHANNELS_FILE = "./src/channel_ids.txt"



def get_channel_data(channels_file=CHANNELS_FILE):
    """対象チャンネルをファイルから読み込む

    Args:
        channels_file (str): ファイルのパス

    Returns:
        list: 対象チャンネルのセット
    """
    
    with open(channels_file, "r", encoding="utf-8") as f:
        file_data = f.readlines()
    
    datas = []
    
    for channel_set in file_data:
        datas.append(channel_set.split())
      
    datasets = []

    #ファイル名を整形
    for data in datas:
        name = " ".join(data[1:])
        name = name.replace(" ", "_")
        name = name.replace("/", "_")
        name = name.replace("[", "_")
        name = name.replace("]", "_")
        datasets.append([data[0], name])
    
    return datasets


#チャンネル名の変換
def conv_channel_name(name):
    """チャンネル名の変換を行う

    Args:
        name (str): チャンネル名

    Returns:
        str: 変換後のチャンネル名
    """
    channel_name = name.replace(" ", "_").lower()
    channel_name = channel_name.replace("/", "_")
    channel_name = channel_name.replace("[", "_")
    channel_name = channel_name.replace("]", "_")
    return channel_name


if __name__ == "__main__":
    d = get_channel_data()
    print(d)