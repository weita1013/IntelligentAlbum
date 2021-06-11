import os
import shutil
import cv2
import dlib
import numpy as np
import matplotlib.pyplot as plt


def show_image(image):
    img_RGB = image[:, :, ::-1]  # BGR转RGB
    plt.imshow(img_RGB)
    plt.axis('off')


# 绘制人脸矩形
def plot_rectangle(image, faces):
    img_range_list = []
    for face in faces:
        cv2.rectangle(image, (face.left() - 10, face.top() - 20), (face.right() + 10, face.bottom() + 10),
                      (0, 255, 0), 2)
        img_range_list.append([(face.top() - 20), (face.bottom() + 10), (face.left() - 10), (face.right() + 10)])
    return image, img_range_list


# 识别
def trace(img_path, img_save_path):
    # 读取一张照片
    img = cv2.imread(img_path)
    # 灰度转换
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 调用dlib库中的检测器
    detector = dlib.get_frontal_face_detector()
    detector_result = detector(gray, 2)  # 放大一倍
    # 绘制矩形
    img_res, range_list = plot_rectangle(img.copy(), detector_result)

    # img_save_path = '../media/faces'
    shutil.rmtree(img_save_path, ignore_errors=True)
    os.makedirs(img_save_path)
    i = 0
    for img_range in range_list:
        image_range = img_res[img_range[0]:img_range[1], img_range[2]:img_range[3]]
        cv2.imwrite('{}/{}.jpg'.format(img_save_path, i), image_range)
        i = i + 1
    show_image(img_res)
    p_path = img_save_path + '/face_trace.jpg'
    plt.savefig(p_path)
    return len(range_list)


# 关键点编码为128维
def encoder_face(image, detector, predictor, encoder, upsample=1, jet=1):
    # 检测人脸
    faces = detector(image, upsample)
    # 对每张人脸进行关键点检测
    faces_keypoints = [predictor(image, face) for face in faces]
    return [np.array(encoder.compute_face_descriptor(image, faces_keypoint, jet)) for faces_keypoint in faces_keypoints]


# 人脸比较（欧式距离）
def compare_faces(face_encoding, test_encoding, name_list):
    distance = list(np.linalg.norm(np.array(face_encoding) - np.array(test_encoding), axis=1))
    return zip(*sorted(zip(distance, name_list)))


def recognition(img_path, test_path, img_save_path):
    # 加载人脸检测器
    detector = dlib.get_frontal_face_detector()
    # 加载关键点的检测器
    predictor = dlib.shape_predictor('utils/shape_predictor_68_face_landmarks.dat')
    # 加载人脸特征编码模型
    encoder = dlib.face_recognition_model_v1('utils/dlib_face_recognition_resnet_model_v1.dat')
    len_img = trace(img_path, img_save_path)
    name_list = []
    img_list = []
    test = cv2.imread(test_path)
    test = test[:, :, ::-1]
    test_128D = encoder_face(test, detector, predictor, encoder)[0]
    for i in range(len_img):
        img = cv2.imread('{}/{}.jpg'.format(img_save_path, i))
        img = img[:, :, ::-1]
        img_128D = encoder_face(img, detector, predictor, encoder)[0]
        img_list.append(img_128D)
        name_list.append(i)
        i + 1

    distance, name = compare_faces(img_list, test_128D, name_list)
    res = name[0]
    return '{}/{}.jpg'.format(img_save_path, res)
