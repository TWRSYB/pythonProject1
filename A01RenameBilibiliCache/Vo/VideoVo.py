import VideoPageDataVo


class VideoVo:
    def __init__(self, media_type, has_dash_audio, is_completed, total_bytes, downloaded_bytes, title, type_tag, cover,
                 video_quality, prefered_video_quality, guessed_total_bytes, total_time_milli, danmaku_count,
                 time_update_stamp, time_create_stamp, can_play_in_advance, interrupt_transform_temp_file,
                 quality_pithy_description, quality_superscript, cache_version_code, preferred_audio_quality,
                 audio_quality, avid, spid, seasion_id, bvid, owner_id, owner_name, owner_avatar, page_data):
        self.media_type: int = media_type  # 2
        self.has_dash_audio: bool = has_dash_audio  # True
        self.is_completed: bool = is_completed  # True
        self.total_bytes: int = total_bytes  # 3989296
        self.downloaded_bytes: int = downloaded_bytes  # 3989296
        self.title: str = title  # 【创2024主题曲Summer Dream翻跳】说好了，我先过盛夏！
        self.type_tag: str = type_tag  # 80
        self.cover: str = cover  # http://i2.hdslb.com/bfs/archive/e15e9362af0b3e9f6c897ccbc5020b1762bdc482.jpg
        self.video_quality: int = video_quality  # 80
        self.prefered_video_quality: int = prefered_video_quality  # 80
        self.guessed_total_bytes: int = guessed_total_bytes  # 0
        self.total_time_milli: int = total_time_milli  # 51547
        self.danmaku_count: int = danmaku_count  # 0
        self.time_update_stamp: int = time_update_stamp  # 1704469732310
        self.time_create_stamp: int = time_create_stamp  # 1704469722838
        self.can_play_in_advance: bool = can_play_in_advance  # True
        self.interrupt_transform_temp_file: bool = interrupt_transform_temp_file  # False
        self.quality_pithy_description: str = quality_pithy_description  # 1080P
        self.quality_superscript: str = quality_superscript  #
        self.cache_version_code: int = cache_version_code  # 7490200
        self.preferred_audio_quality: int = preferred_audio_quality  # 0
        self.audio_quality: int = audio_quality  # 0
        self.avid: int = avid  # 283328518
        self.spid: int = spid  # 0
        self.seasion_id: int = seasion_id  # 0
        self.bvid: str = bvid  # BV1Ec41187j8
        self.owner_id: int = owner_id  # 284194350
        self.owner_name: str = owner_name  # Huhu安
        self.owner_avatar: str = owner_avatar  # https://i0.hdslb.com/bfs/face/858ef89ae710dfdcbbef99296c2565a49c0c7da1.jpg
        self.page_data: VideoPageDataVo = page_data  # {'cid': 1395425474, 'page': 2, 'from': 'vupload', 'part': '裸眼3D', 'link': '', 'vid': '', 'has_alias': False, 'tid': 199, 'width': 3840, 'height': 2160, 'rotate': 0, 'download_title': '视频已缓存完成', 'download_subtitle': '【创2024主题曲Summer Dream翻跳】说好了，我先过盛夏！ 裸眼3D'}
