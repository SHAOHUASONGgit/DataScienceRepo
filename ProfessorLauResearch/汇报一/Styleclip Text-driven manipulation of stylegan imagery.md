### Styleclip: Text-driven manipulation of stylegan imagery

### 文本驱动的StyleGan图像操纵



CLIP模型：基于文本对图像进行分类的模型，根据自然语言输入预测与其描述图像最相关的文本片段

GAN模型：GAN由生成器G与分类器D两套独立的神经网络组成。生成器G用于生成样本，分类器D用于分辨生成样本的真实性。如果D判断正确，则调整G参数；如果D判断错误，则调整D参数，最终得到一个质量较高的生成器与判断能力较强的分类器

Styleclip原理：结合CLIP模型与StyleGAN模型，基于CLIP的损失修改输入的潜向量来响应输入文本提示；提出一种方法，将文本提示映射到StyleGAN的风格空间中，实现交互式的文本驱动的图像操纵
