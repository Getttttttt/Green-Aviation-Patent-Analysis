from PIL import Image
import os

# 图片文件夹路径
folder_path = './'

# 读取所有图片文件
files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
files.sort()  # 这假设文件名能正确地排序

# 假设所有图片大小相同
sample_image = Image.open(os.path.join(folder_path, files[0]))
width, height = sample_image.width, sample_image.height

# 创建新的画布（背景设为白色）
canvas = Image.new('RGB', (5 * width, 3 * height), 'white')

# 按位置放置每个图片
for i, file in enumerate(files):
    img = Image.open(os.path.join(folder_path, file))
    # 计算放置位置
    x = (i % 5) * width
    y = (i // 5) * height
    canvas.paste(img, (x, y))

# 保存新图片
canvas.save(os.path.join(folder_path, './combined_image.png'))
