# IntelligentAlbum
智能云端相册
- **项目描述** :智能云相册能够实现照片的自动归档，从照片类型进行分类（人物、动物、风景、交通工具、建筑），
使用人脸检索集体活动照片自动完成私人照片的快速分发，相册也可以生成精彩瞬间剪辑

- **项目技术**：html、css、vue、elementUI、axios、Django、drf、百度飞桨

  前端采用vue框架构建前端页面，后端使用drf开发，通过百度飞桨paddlepaddle模块深度学习、
  卷积神经网络完成模型训练使得照片智能分类等准确率高于百分之九十五，通过dlib库和OpenCV实现人脸追踪，
  使用dlib官方训练的模型进行人脸识别，实现了私人照片的快速分发，使用OpenCV图像处理和librosa音频处理实现了自定制回忆录，
  用户可以自行选择照片，背景音乐，使用librosa解析出音频的拍点，使用OpenCV进行图像处理，通过ffmpeg进行音视频的合成。
