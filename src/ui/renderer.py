import pygame
from typing import Tuple, Dict, Optional
from dataclasses import dataclass

@dataclass
class SubtitleStyle:
    font_name: str = "Arial"
    font_size: int = 24
    color: Tuple[int, int, int] = (255, 255, 255)
    background: Optional[Tuple[int, int, int, int]] = None
    outline: Optional[Tuple[int, int, int]] = None
    position: str = "bottom"

class SubtitleRenderer:
    def __init__(self, display_index: int = 0):
        """
        字幕渲染器
        :param display_index: 显示器索引
        """
        pygame.init()
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (info.current_w, info.current_h),
            pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF,
            display=display_index
        )
        self.font_cache = {}
        self.texture_cache = TTLCache(maxsize=100, ttl=60)
        self.clock = pygame.time.Clock()
        self.active_subtitles = []

    def render(self, text: str, style: SubtitleStyle):
        """
        渲染单条字幕
        :param text: 字幕文本
        :param style: 渲染样式
        """
        # 获取或创建字体
        font_key = (style.font_name, style.font_size)
        if font_key not in self.font_cache:
            try:
                font = pygame.font.Font(style.font_name, style.font_size)
            except:
                font = pygame.font.SysFont(style.font_name, style.font_size)
            self.font_cache[font_key] = font
        
        # 检查纹理缓存
        cache_key = (text, *font_key, style.color)
        if cache_key in self.texture_cache:
            texture = self.texture_cache[cache_key]
        else:
            # 渲染文本表面
            font = self.font_cache[font_key]
            texture = font.render(text, True, style.color)
            if style.outline:
                outline = font.render(text, True, style.outline)
                texture.blit(outline, (-1, -1))
            self.texture_cache[cache_key] = texture

        # 计算位置
        x = self.screen.get_width() // 2 - texture.get_width() // 2
        if style.position == "bottom":
            y = self.screen.get_height() - 100
        else:  # top
            y = 50

        # 渲染背景
        if style.background:
            bg_rect = pygame.Rect(
                x - 5, y - 2,
                texture.get_width() + 10,
                texture.get_height() + 4
            )
            pygame.draw.rect(
                self.screen, 
                style.background[:3],
                bg_rect
            )

        # 绘制文本
        self.screen.blit(texture, (x, y))
        pygame.display.flip()
        self.clock.tick(60)  # 限制60FPS

    def clear(self):
        """清除所有字幕"""
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        self.active_subtitles.clear()