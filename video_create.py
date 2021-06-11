import cv2
import librosa
import numpy as np
import os
from PIL import Image

# 最后影片的分辨率片，根据视频来设置，默认是1920*1080
img_size = (int(1280), int(720))


# 图片处理
def resize_image(target_image_path, target_size):
    """
    调整图片大小，缺失的部分用黑色填充
    :param target_image_path: 图片路径
    :param target_size: 分辨率大小
    :return:
    """
    image = Image.open(target_image_path)

    iw, ih = image.size  # 原始图像的尺寸
    w, h = target_size  # 目标图像的尺寸
    scale = min(w / iw, h / ih)  # 转换的最小比例

    # 保证长或宽，至少一个符合目标图像的尺寸
    nw = int(iw * scale)
    nh = int(ih * scale)

    image = image.resize((nw, nh), Image.BICUBIC)  # 缩小图像
    # image.show()

    new_image = Image.new('RGB', target_size, (0, 0, 0, 0))  # 生成黑色图像
    # // 为整数除法，计算图像的位置
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))  # 将图像填充为中间图像，两侧为灰色的样式
    # new_image.show()

    # 覆盖原图片
    new_image.save(target_image_path)


# 临时文件处理
def get_temp_path(file_path, temp_name):
    """
    获取同一级目录下临时文件的完整路径
    :param str:
    :return:
    """
    filepath, filename_with_extension, filename_without_extension, extension = get_filePath_fileName_all(file_path)

    return filepath + "/" + temp_name + extension


# 文件处理
def get_filePath_fileName_all(filename):
    """
    获取文件的路径、文件名【带后缀】、文件名【不带后缀】、后缀名
    :param filename:
    :return:
    """
    (filepath, filename_with_extension) = os.path.split(filename)
    (filename_without_extension, extension) = os.path.splitext(filename_with_extension)

    return filepath, filename_with_extension, filename_without_extension, extension


# 获取节拍点
def getBeats(bgm_path):
    y, sr = librosa.load(bgm_path, sr=None)
    onset_env = librosa.onset.onset_strength(y, sr=sr, aggregate=np.median)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    beats = np.array(librosa.frames_to_time(beats[:-1], sr=sr))  # 转为列表
    # time = librosa.get_duration(filename=bgm_path)
    return beats


def compound_pic_special(images_path, output_video_path, bgm_path, fps=30):
    """
    图片合成视频【卡点视频】
    :param images_path: 图片文件路径
    :param output_video_path:合成视频的路径
    :return:
    """
    res = getBeats(bgm_path)
    beat_list = []
    for i in range(len(res) - 1):
        beat = res[i + 1] - res[i]
        beat_list.append(beat)
    # 获取该目录下的所有文件名
    filelist = os.listdir(images_path)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # 生成一个视频对象
    video = cv2.VideoWriter(output_video_path, fourcc, fps, img_size)
    i = 0
    time_count = 0
    while True:
        if filelist[i].endswith('.jpg'):  # 判断图片后缀是否是.jpg
            image_path = images_path + '/' + filelist[i]
            # 缩放图片到合适的分辨率，并覆盖源文件
            resize_image(image_path, img_size)
            frame = cv2.imread(image_path)
            # 直接缩放到指定大小
            frame_suitable = cv2.resize(frame, (img_size[0], img_size[1]), interpolation=cv2.INTER_CUBIC)
            # 把图片写进视频
            # 重复写入多少次
            count = 0
            total_count = round(30 / beat_list[time_count])
            while count < total_count:
                video.write(frame_suitable)
                count += 1
            time_count += 1
            if time_count == len(beat_list) - 1:
                break
        else:
            print('名称为:%s,文件格式不对，过滤掉~' % filelist[i])
        if i + 1 == len(filelist):
            i = 0
        else:
            i += 1

    # 释放资源
    video.release()


def create_video(images_path, video_path, bgm_path, fps=30):
    """
    通过视频、BGM 合成一段视频
    :param video_path: 视频路径
    :param bgm_path: BGM路径
    :return:
    """
    compound_pic_special(images_path, video_path, bgm_path, fps)
    # 视频、音频合二为一
    video_temp_path = get_temp_path(video_path, 'temp')
    os.system('ffmpeg -i %s  -i %s  -c:v copy -c:a aac -strict -2  %s -y -loglevel quiet' % (
        video_path, bgm_path, video_temp_path))
    os.remove(video_path)
    os.rename(video_temp_path, video_path)
    print('音视频合成完成~')
