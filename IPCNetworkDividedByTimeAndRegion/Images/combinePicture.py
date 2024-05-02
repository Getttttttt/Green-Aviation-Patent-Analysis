from PIL import Image, ImageDraw, ImageFont
import os

# 图片文件夹路径
folder_path = './'
file_path = "./combined_image.png"
# 检查文件是否存在
if os.path.exists(file_path):
    # 删除文件
    os.remove(file_path)
    print(f"文件已被删除。")

# 定义排序顺序
years = ['2013-2015', '2013-2020', '2013-2024']
countries = ['total', '中国', '欧洲专利局','俄罗斯', '美国']

# 读取所有图片文件
files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# 根据定义的年份和国家顺序进行排序
files.sort(key=lambda x: (years.index(x.split('_')[0]), countries.index(x[:-4].split('_')[1])))

# 假设所有图片大小相同
sample_image = Image.open(os.path.join(folder_path, files[0]))
width, height = sample_image.width, sample_image.height

# 创建新的画布（背景设为白色），为文本留出额外空间
text_height = 200  # 文本区域的高度
canvas = Image.new('RGB', (5 * width, 3 * (height + text_height)), 'white')

# 选择一个字体和大小
try:
    font = ImageFont.truetype("./times.ttf", 55)
    print("自定义字体加载成功。")
except IOError:
    print("自定义字体加载失败，使用默认字体。")
    font = ImageFont.load_default()  # 默认字体，可能不支持调整大小

# 初始化draw对象
draw = ImageDraw.Draw(canvas)

# 按位置放置每个图片并添加文本
count = 0
# 获取名称
# network_path = '../IPCDividedNetwork'
# file_names = os.listdir(network_path)
# print(file_names)
file_names = ['              2132_6447_0.59_0.60_4.17.gexf', '             1048_1505_0.47_0.85_4.54.gexf', '                333_1089_0.77_0.73_3.28.gexf', '                    289_245_0.41_0.96_2.12.gexf', '                 644_2900_0.81_0.61_3.20.gexf', 
              '              5612_29563_0.60_0.43_4.10.gexf', '              3755_11613_0.57_0.69_4.93.gexf', '                 834_3976_0.76_0.58_3.36.gexf', '                   752_885_0.49_0.86_4.45.gexf', '                 1428_10553_0.77_0.37_2.95.gexf', 
              '              6563_40362_0.61_0.41_3.93.gexf', '              4465_16207_0.59_0.70_4.64.gexf', '                 1038_5449_0.74_0.48_3.34.gexf', '                   858_1087_0.50_0.85_4.92.gexf', '                 1772v14189_0.75_0.36_2.93.gexf']

for i, file in enumerate(files):
    name = file_names[count][:-5]
    count+=1
    img = Image.open(os.path.join(folder_path, file))
    # 计算放置图片的位置
    x = (i % 5) * width
    y = (i // 5) * (height + text_height)
    canvas.paste(img, (x, y))
    # 计算文本宽度和居中位置
    # text = file[:-4]
    # text_width, _ = draw.textsize(text,font=font)
    # text_x = x + (width - text_width) / 2  # 更新文本x位置以居中
    # 添加文本
    draw.text((x, y + height), name, font=font, fill='black')

# 保存新图片
canvas.save(os.path.join(folder_path, './combined_image.png'))
