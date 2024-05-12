import json


def start(the_json):
    print('CREATE TABLE xxx (')
    json_obj = json.loads(the_json)
    for key, value in json_obj.items():
        db_type = ''
        value_type = type(value).__name__
        if value_type == str:
            db_type = f'VARCHAR({len(value)*5})'
        elif value_type == str:
            db_type = f'VARCHAR({len(value) * 5})'
        print(f"{key}, Value: {value}, Type: {value_type}")
    print("""
        MS_RESUME									VARCHAR(300)		NOT NULL		DEFAULT ' '							COMMENT '简述',
        MS_DETAIL									VARCHAR(1000)		NOT NULL		DEFAULT ' '							COMMENT '详细',
        RC_RECORD_TIME								TIMESTAMP			NOT NULL		DEFAULT CURRENT_TIMESTAMP			COMMENT '收录时间',
        RC_RECORDER									VARCHAR(50)			NOT NULL		DEFAULT '未收录'						COMMENT '收录人',
        RC_LAST_MODIFIED_TIME						TIMESTAMP			COMMENT '最后修改时间',
        RC_LAST_MODIFIER							VARCHAR(50)			NOT NULL		DEFAULT '未收录'						COMMENT '最后修改人',
        RC_DATA_STATUS								CHAR(1)				NOT NULL		DEFAULT '0'							COMMENT '数据状态: 0-未生效, 1-正常, 2-不可用,9-废弃',
        CONSTRAINT class_pk PRIMARY KEY (,)
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8
    COLLATE=utf8_bin
    COMMENT=;
    """)

the_json = '{"media_type":2,"has_dash_audio":true,"is_completed":true,"total_bytes":6241839,"downloaded_bytes":6241839,"title":"【创2024主题曲Summer Dream翻跳】说好了，我先过盛夏！","type_tag":"80","cover":"http:\/\/i2.hdslb.com\/bfs\/archive\/e15e9362af0b3e9f6c897ccbc5020b1762bdc482.jpg","video_quality":80,"prefered_video_quality":80,"guessed_total_bytes":0,"total_time_milli":53590,"danmaku_count":4,"time_update_stamp":1704469739673,"time_create_stamp":1704469724850,"can_play_in_advance":true,"interrupt_transform_temp_file":false,"quality_pithy_description":"1080P","quality_superscript":"","cache_version_code":7490200,"preferred_audio_quality":0,"audio_quality":0,"avid":283328518,"spid":0,"seasion_id":0,"bvid":"BV1Ec41187j8","owner_id":284194350,"owner_name":"Huhu安","owner_avatar":"https:\/\/i0.hdslb.com\/bfs\/face\/858ef89ae710dfdcbbef99296c2565a49c0c7da1.jpg","cid":1395320270,"page":1,"from":"vupload","part":"正常版","link":"","vid":"","has_alias":false,"tid":199,"width":2160,"height":3840,"rotate":0,"download_title":"视频已缓存完成","download_subtitle":"【创2024主题曲Summer Dream翻跳】说好了，我先过盛夏！ 正常版"}'


start(the_json)