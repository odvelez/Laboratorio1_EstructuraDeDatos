"""
Vista visual de la tabla hash de jugadores (solo lectura de la estructura existente).

No modifica persistence.hash_table.HashTable: solo lee estado vía PlayerManager.
Dibujo optimizado para pygbag (pocos primitivos por frame, sin rejilla densa).
"""
import pygame

from persistence.hash_table import HashTable

# ── Colores ───────────────────────────────────
BG = (8, 8, 26)
BUCKET_EMPTY = (30, 34, 70)
BUCKET_USED = (60, 110, 210)
CHAIN_COLOR = (250, 150, 80)
TEXT_COLOR = (230, 230, 245)
DIM_COLOR = (140, 140, 180)
ACCENT = (255, 220, 0)
BAR_BG = (26, 24, 60)
BAR_LOW = (80, 220, 140)
BAR_MID = (230, 200, 90)
BAR_HIGH = (255, 90, 90)
ARROW_COLOR = (180, 180, 210)
GRID_LINE = (22, 18, 55)


def _build_hashtable():
    """Retorna el HashTable real del PlayerManager (misma fuente que consola)."""
    try:
        from crud.player import get_manager

        mgr = get_manager()
        return mgr.players
    except Exception:
        return HashTable(size=16)


def _bucket_stats(ht):
    """Lista de (índice, [keys…]) por bucket; solo lectura de ht.table."""
    result = []
    for i in range(ht.size):
        chain = []
        entry = ht.table[i]
        while entry is not None:
            chain.append(entry.key)
            entry = entry.next
        result.append((i, chain))
    return result


def _draw_light_grid(screen, w, h):
    """Líneas espaciadas (pocas operaciones; apto para WASM)."""
    step = 72
    for x in range(0, w + 1, step):
        pygame.draw.line(screen, GRID_LINE, (x, 0), (x, h), 1)
    for y in range(0, h + 1, step):
        pygame.draw.line(screen, GRID_LINE, (0, y), (w, y), 1)


class HashTableScene:
    def __init__(self):
        self.next_scene = None
        self.should_quit = False

        self.ht = _build_hashtable()
        self.buckets = _bucket_stats(self.ht)

        self.scroll = 0
        self.ROWS_VISIBLE = 8

        self.hovered_bucket = -1
        self.bucket_rects = []

        self.title_font = pygame.font.Font(None, 52)
        self.label_font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 24)
        self.stat_font = pygame.font.Font(None, 28)

        self.back_rect = pygame.Rect(0, 0, 0, 0)
        self.back_hover = False

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.back_hover = self.back_rect.collidepoint(mouse_pos)

        self.hovered_bucket = -1
        for idx, rect in enumerate(self.bucket_rects):
            if rect.collidepoint(mouse_pos):
                self.hovered_bucket = self.scroll + idx
                break

        for event in events:
            if event.type == pygame.QUIT:
                self.should_quit = True
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._go_back()
                elif event.key == pygame.K_DOWN:
                    max_scroll = max(0, len(self.buckets) - self.ROWS_VISIBLE)
                    self.scroll = min(self.scroll + 1, max_scroll)
                elif event.key == pygame.K_UP:
                    self.scroll = max(self.scroll - 1, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.back_rect.collidepoint(mouse_pos):
                    self._go_back()
                if event.button == 4:
                    self.scroll = max(self.scroll - 1, 0)
                if event.button == 5:
                    max_scroll = max(0, len(self.buckets) - self.ROWS_VISIBLE)
                    self.scroll = min(self.scroll + 1, max_scroll)

    def _go_back(self):
        from scenes.menu import MenuScene

        self.next_scene = MenuScene()

    def update(self):
        pass

    def draw(self, screen):
        w, h = screen.get_size()
        screen.fill(BG)
        _draw_light_grid(screen, w, h)

        header_rect = pygame.Rect(0, 0, w, 90)
        pygame.draw.rect(screen, (30, 16, 80), header_rect)
        pygame.draw.rect(screen, ACCENT, header_rect, 2)

        title = self.title_font.render("HASH TABLE VISUALIZER", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(w // 2, 38)))

        subtitle = self.small_font.render(
            "Buckets  |  Stats  |  Players in table", True, DIM_COLOR
        )
        screen.blit(subtitle, subtitle.get_rect(center=(w // 2, 70)))

        footer_h = 56
        panels_top = 100
        panels_bottom_margin = 10
        panels_h = max(220, h - panels_top - footer_h - panels_bottom_margin)

        panel_left_w = int(w * 0.60)
        panel_right_x = panel_left_w + 24

        left_panel = pygame.Rect(20, panels_top, panel_left_w - 30, panels_h)
        right_panel = pygame.Rect(panel_right_x - 4, panels_top, w - panel_right_x - 24, panels_h)
        pygame.draw.rect(screen, (16, 12, 50), left_panel, border_radius=16)
        pygame.draw.rect(screen, (120, 90, 255), left_panel, 2, border_radius=16)
        pygame.draw.rect(screen, (16, 12, 50), right_panel, border_radius=16)
        pygame.draw.rect(screen, (120, 200, 255), right_panel, 2, border_radius=16)

        self._draw_buckets(
            screen,
            left_panel.x + 14,
            left_panel.y + 16,
            left_panel.width - 20,
            left_panel.height - 30,
            clip_rect=left_panel.inflate(-10, -10),
        )
        self._draw_stats(
            screen,
            right_panel.x + 18,
            right_panel.y + 16,
            right_panel.width - 24,
            right_panel.height - 30,
            clip_rect=right_panel.inflate(-10, -10),
        )

        footer = pygame.Rect(0, h - footer_h, w, footer_h)
        pygame.draw.rect(screen, (12, 10, 40), footer)
        pygame.draw.line(screen, (70, 70, 120), (20, footer.top), (w - 20, footer.top), 1)

        hint = self.small_font.render(
            "Up/Down or wheel: scroll   |   ESC: back", True, DIM_COLOR
        )
        screen.blit(hint, (30, footer.top + 18))

        back_color = ACCENT if self.back_hover else (210, 210, 230)
        back_text = self.stat_font.render("BACK (ESC)", True, back_color)
        self.back_rect = back_text.get_rect(midright=(w - 30, footer.centery))
        screen.blit(back_text, self.back_rect)

    def _draw_buckets(self, screen, x, y, panel_w, panel_h, clip_rect=None):
        prev_clip = screen.get_clip()
        if clip_rect is not None:
            screen.set_clip(clip_rect)

        label = self.label_font.render("BUCKETS", True, ACCENT)
        screen.blit(label, (x, y))
        y += 30

        row_h = (panel_h - 30) // self.ROWS_VISIBLE
        row_h = max(row_h, 42)
        idx_w = 42
        node_w = 120
        node_h = row_h - 10
        arrow_w = 24

        visible = self.buckets[self.scroll : self.scroll + self.ROWS_VISIBLE]
        self.bucket_rects = []

        for row, (bucket_idx, chain) in enumerate(visible):
            ry = y + row * row_h
            is_hover = self.hovered_bucket == bucket_idx

            idx_rect = pygame.Rect(x, ry + (row_h - node_h) // 2, idx_w, node_h)
            idx_bg = (50, 70, 120) if is_hover else (30, 40, 80)
            pygame.draw.rect(screen, idx_bg, idx_rect, border_radius=5)
            idx_txt = self.label_font.render(str(bucket_idx), True, DIM_COLOR)
            screen.blit(idx_txt, idx_txt.get_rect(center=idx_rect.center))

            row_rect = pygame.Rect(x, ry, panel_w, row_h - 2)
            self.bucket_rects.append(row_rect)

            if not chain:
                empty_rect = pygame.Rect(
                    x + idx_w + 8,
                    ry + (row_h - node_h) // 2,
                    node_w,
                    node_h,
                )
                pygame.draw.rect(screen, BUCKET_EMPTY, empty_rect, border_radius=6)
                pygame.draw.rect(screen, (70, 80, 130), empty_rect, 1, border_radius=6)
                nil = self.small_font.render("NULL", True, DIM_COLOR)
                screen.blit(nil, nil.get_rect(center=empty_rect.center))
            else:
                cx_node = x + idx_w + 8
                for ni, key in enumerate(chain):
                    color = (
                        CHAIN_COLOR
                        if ni > 0
                        else (BUCKET_USED if not is_hover else (90, 150, 230))
                    )
                    node_rect = pygame.Rect(
                        cx_node,
                        ry + (row_h - node_h) // 2,
                        node_w,
                        node_h,
                    )
                    pygame.draw.rect(screen, color, node_rect, border_radius=6)
                    border = (255, 255, 255) if is_hover else (80, 100, 130)
                    pygame.draw.rect(screen, border, node_rect, 1, border_radius=6)

                    display = key if len(key) <= 11 else key[:10] + "…"
                    ktxt = self.small_font.render(display, True, TEXT_COLOR)
                    screen.blit(ktxt, ktxt.get_rect(center=node_rect.center))

                    cx_node += node_w

                    if ni < len(chain) - 1:
                        ax = cx_node
                        ay = ry + row_h // 2
                        pygame.draw.line(
                            screen, ARROW_COLOR, (ax, ay), (ax + arrow_w - 4, ay), 2
                        )
                        pygame.draw.polygon(
                            screen,
                            ARROW_COLOR,
                            [
                                (ax + arrow_w, ay),
                                (ax + arrow_w - 7, ay - 4),
                                (ax + arrow_w - 7, ay + 4),
                            ],
                        )
                        cx_node += arrow_w
                    else:
                        ax = cx_node + 6
                        ay = ry + row_h // 2
                        pygame.draw.line(
                            screen, ARROW_COLOR, (ax - 6, ay), (ax + 12, ay), 2
                        )
                        nil = self.small_font.render("→ NULL", True, DIM_COLOR)
                        screen.blit(nil, nil.get_rect(midleft=(ax + 14, ay)))

        total = len(self.buckets)
        if total > self.ROWS_VISIBLE:
            shown_end = self.scroll + self.ROWS_VISIBLE
            sc_txt = self.small_font.render(
                f"mostrando {self.scroll}–{min(shown_end, total) - 1} / {total - 1}",
                True,
                DIM_COLOR,
            )
            sc_y = (
                (clip_rect.bottom - 22)
                if clip_rect is not None
                else (y + self.ROWS_VISIBLE * row_h + 6)
            )
            screen.blit(sc_txt, (x, sc_y))

        if clip_rect is not None:
            screen.set_clip(prev_clip)

    def _draw_stats(self, screen, x, y, panel_w, panel_h, clip_rect=None):
        prev_clip = screen.get_clip()
        if clip_rect is not None:
            screen.set_clip(clip_rect)

        y_max = (clip_rect.bottom - 10) if clip_rect is not None else (y + panel_h)

        ht = self.ht
        lf = ht.load_factor
        col = sum(1 for _, chain in self.buckets if len(chain) > 1)
        used = sum(1 for _, chain in self.buckets if chain)
        total_buckets = len(self.buckets)

        stats = [
            ("Size (buckets)", str(ht.size)),
            ("Entries", str(ht.count)),
            ("Load factor", f"{lf:.2f}"),
            ("Buckets used", f"{used} / {total_buckets}"),
            ("Collisions", str(col)),
            (
                "Rehash at",
                f">= {ht.LOAD_FACTOR_GROW:.2f}  /  "
                f"<= {ht.LOAD_FACTOR_SHRINK:.2f}",
            ),
        ]

        label = self.label_font.render("STATS", True, ACCENT)
        screen.blit(label, (x, y))
        y += 30

        for key, val in stats:
            if y + 46 > y_max:
                break
            k_surf = self.small_font.render(key, True, DIM_COLOR)
            v_surf = self.stat_font.render(val, True, TEXT_COLOR)
            screen.blit(k_surf, (x, y))
            screen.blit(v_surf, (x, y + 16))
            y += 46

        y += 6
        if y + 1 <= y_max:
            pygame.draw.line(screen, (50, 60, 80), (x, y), (x + panel_w, y), 1)
        y += 12

        if y + 60 > y_max:
            if clip_rect is not None:
                screen.set_clip(prev_clip)
            return

        bar_label = self.label_font.render("LOAD FACTOR", True, ACCENT)
        screen.blit(bar_label, (x, y))
        y += 26

        bar_w = panel_w - 10
        bar_h = 22
        bar_rect = pygame.Rect(x, y, bar_w, bar_h)
        pygame.draw.rect(screen, BAR_BG, bar_rect, border_radius=5)

        fill_w = int(bar_w * min(lf, 1.0))
        if fill_w > 0:
            color = BAR_LOW if lf < 0.5 else (BAR_MID if lf < 0.75 else BAR_HIGH)
            fill_rect = pygame.Rect(x, y, fill_w, bar_h)
            pygame.draw.rect(screen, color, fill_rect, border_radius=5)

        pygame.draw.rect(screen, (80, 100, 130), bar_rect, 1, border_radius=5)

        for mark, label_txt in ((0.25, "0.25"), (0.75, "0.75")):
            mx = x + int(bar_w * mark)
            pygame.draw.line(
                screen, (160, 160, 180), (mx, y - 3), (mx, y + bar_h + 3), 1
            )
            ml = self.small_font.render(label_txt, True, DIM_COLOR)
            screen.blit(ml, ml.get_rect(center=(mx, y + bar_h + 10)))

        pct = self.small_font.render(f"{lf * 100:.0f}%", True, TEXT_COLOR)
        screen.blit(pct, pct.get_rect(center=(x + bar_w // 2, y + bar_h // 2)))
        y += bar_h + 22

        if y + 1 <= y_max:
            pygame.draw.line(screen, (50, 60, 80), (x, y), (x + panel_w, y), 1)
        y += 12

        if y + 90 > y_max:
            if clip_rect is not None:
                screen.set_clip(prev_clip)
            return

        leg_label = self.label_font.render("LEGEND", True, ACCENT)
        screen.blit(leg_label, (x, y))
        y += 26

        legend = [
            (BUCKET_USED, "First node (no collision)"),
            (CHAIN_COLOR, "Chained node (collision)"),
            (BUCKET_EMPTY, "Empty bucket"),
        ]
        sq = 14
        for color, desc in legend:
            if y + 22 > y_max:
                break
            pygame.draw.rect(screen, color, (x, y + 2, sq, sq), border_radius=3)
            pygame.draw.rect(
                screen, (180, 180, 200), (x, y + 2, sq, sq), 1, border_radius=3
            )
            dl = self.small_font.render(desc, True, DIM_COLOR)
            screen.blit(dl, (x + sq + 8, y))
            y += 22

        y += 8
        if y + 1 <= y_max:
            pygame.draw.line(screen, (50, 60, 80), (x, y), (x + panel_w, y), 1)
        y += 12

        if y + 40 > y_max:
            if clip_rect is not None:
                screen.set_clip(prev_clip)
            return

        pl_label = self.label_font.render("PLAYERS IN TABLE", True, ACCENT)
        screen.blit(pl_label, (x, y))
        y += 26

        for nombre, p in self.ht.items():
            if y + 20 > y_max:
                more = self.small_font.render("…", True, DIM_COLOR)
                screen.blit(more, (x, y))
                break
            bucket_idx = ht._hash(nombre)
            chain = (
                self.buckets[bucket_idx][1] if bucket_idx < len(self.buckets) else []
            )
            has_col = len(chain) > 1
            col_mark = "  ⚠ collision" if has_col else ""
            line = self.small_font.render(
                f"[{bucket_idx:02d}] {nombre}  →  {p.max_score}{col_mark}",
                True,
                CHAIN_COLOR if has_col else TEXT_COLOR,
            )
            screen.blit(line, (x, y))
            y += 20

        if clip_rect is not None:
            screen.set_clip(prev_clip)
