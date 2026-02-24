import torch
import torch.nn as nn

# --- 1. 视觉模型: Vision Transformer (ViT) ---
class EmotionViT(nn.Module):
    def __init__(self, img_size=48, patch_size=6, num_classes=7, dim=128, depth=6, heads=8, mlp_dim=256):
        super().__init__()
        assert img_size % patch_size == 0, "Image dimensions must be divisible by the patch size."
        num_patches = (img_size // patch_size) ** 2
        patch_dim = 3 * patch_size ** 2 # 假设输入是 RGB 3通道

        # Patch Embedding 层
        self.patch_to_embedding = nn.Linear(patch_dim, dim)
        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, dim))
        self.cls_token = nn.Parameter(torch.randn(1, 1, dim))
        self.dropout = nn.Dropout(0.1)

        # Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(d_model=dim, nhead=heads, dim_feedforward=mlp_dim, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=depth)

        # MLP Head
        self.to_cls_token = nn.Identity()
        self.mlp_head = nn.Sequential(
            nn.LayerNorm(dim),
            nn.Linear(dim, num_classes)
        )

    def forward(self, img):
        # img shape: [batch, 3, 48, 48]
        p = 6 # patch_size
        b, c, h, w = img.shape
        
        # 将图片切块并展平 (这里使用 unfold 实现切块)
        # 结果 shape: [batch, num_patches, patch_dim]
        x = img.unfold(2, p, p).unfold(3, p, p).permute(0, 2, 3, 1, 4, 5).contiguous().view(b, -1, p*p*c)
        
        x = self.patch_to_embedding(x)
        b, n, _ = x.shape

        cls_tokens = self.cls_token.expand(b, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)
        x += self.pos_embedding[:, :(n + 1)]
        x = self.dropout(x)

        x = self.transformer(x)

        # 取出 CLS token 进行分类
        return self.mlp_head(x[:, 0])

# --- 2. 文本模型: Text Transformer Encoder ---
class TextEmotionTransformer(nn.Module):
    def __init__(self, vocab_size=5000, max_len=100, dim=128, num_classes=3, depth=4, heads=4):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, dim)
        self.pos_embedding = nn.Parameter(torch.randn(1, max_len, dim))
        
        encoder_layer = nn.TransformerEncoderLayer(d_model=dim, nhead=heads, dim_feedforward=256, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=depth)
        
        self.fc = nn.Sequential(
            nn.Linear(dim, dim),
            nn.ReLU(),
            nn.Linear(dim, num_classes)
        )

    def forward(self, x):
        # x shape: [batch, seq_len]
        x = self.embedding(x)
        b, n, _ = x.shape
        x += self.pos_embedding[:, :n]
        
        output = self.transformer(x)
        
        # 简单使用 Mean Pooling
        output = output.mean(dim=1)
        return self.fc(output)