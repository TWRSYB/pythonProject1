class VideoPageDataVo:
    def __init__(self, cid, page, from_, part, link, vid, has_alias, tid, width, height, rotate, download_title,
                 download_subtitle):
        self.cid: int = cid  # 1395425474
        self.page: int = page  # 2
        self.from_: str = from_  # vupload
        self.part: str = part  # 裸眼3D
        self.link: str = link  #
        self.vid: str = vid  #
        self.has_alias: bool = has_alias  # False
        self.tid: int = tid  # 199
        self.width: int = width  # 3840
        self.height: int = height  # 2160
        self.rotate: int = rotate  # 0
        self.download_title: str = download_title  # 视频已缓存完成
        self.download_subtitle: str = download_subtitle  # 【创2024主题曲Summer Dream翻跳】说好了，我先过盛夏！ 裸眼3D
