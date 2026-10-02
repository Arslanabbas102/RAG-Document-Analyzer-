from typing import Iterable

from gradio.themes import Soft
from gradio.themes.utils import colors, fonts, sizes

# slate-based neutral scale: light steps for surfaces/borders, dark steps for
# dark mode surfaces
gray = colors.Color(
    name="slate",
    c50="#f8fafc",
    c100="#f1f5f9",
    c200="#e2e8f0",
    c300="#cbd5e1",
    c400="#94a3b8",
    c500="#64748b",
    c600="#475569",
    c700="#334155",
    c800="#1e293b",
    c900="#0f172a",
    c950="#020617",
)

err_dark = "rgba(228, 98, 98, 1)"
err_dark_muted = "rgba(228, 98, 98, 0.75)"

err = "rgba(239, 68, 68, 1)"
err_muted = "rgba(220, 38, 38, 1)"


common = dict(
    # element colours
    color_accent="*primary_500",
    # shadows
    shadow_drop="0 1px 2px 0 rgb(15 23 42 / 0.06)",
    shadow_drop_lg="0 4px 12px -2px rgb(15 23 42 / 0.08)",
    # layout atoms
    block_label_margin="*spacing_md",
    block_label_padding="*spacing_md",
    block_label_shadow="none",
    block_radius="*radius_lg",
    block_border_width="1px",
    layout_gap="*spacing_xl",
    section_header_text_size="*text_lg",
    # inputs
    input_radius="*radius_md",
    input_border_width="1px",
    input_shadow="none",
    # buttons
    button_shadow="none",
    button_shadow_active="none",
    button_shadow_hover="*shadow_drop",
    button_large_radius="*radius_md",
    button_small_radius="*radius_md",
    button_large_text_weight="600",
    button_small_text_weight="600",
    button_border_width="1px",
)
dark_mode = dict(
    # body attributes
    body_background_fill_dark="*neutral_950",
    body_text_color_dark="*neutral_100",
    body_text_color_subdued_dark="*neutral_400",
    # element colours
    background_fill_primary_dark="*neutral_900",
    background_fill_secondary_dark="*neutral_950",
    border_color_accent_dark="*primary_500",
    border_color_primary_dark="*neutral_800",
    color_accent_soft_dark="*neutral_800",
    # text
    link_text_color_dark="*primary_300",
    link_text_color_active_dark="*primary_200",
    link_text_color_visited_dark="*primary_300",
    # layout atoms
    block_background_fill_dark="*neutral_900",
    block_border_color_dark="*neutral_800",
    block_label_background_fill_dark="*neutral_900",
    block_label_border_width_dark="0px",
    block_label_text_color_dark="*neutral_300",
    block_shadow_dark="none",
    block_title_text_color_dark="*neutral_200",
    panel_background_fill_dark="*neutral_900",
    panel_border_width_dark="0px",
    # component atoms
    checkbox_background_color_selected_dark="*primary_500",
    checkbox_border_color_focus_dark="*primary_400",
    checkbox_border_color_selected_dark="*primary_500",
    checkbox_label_background_fill_dark="*neutral_800",
    checkbox_label_background_fill_selected_dark="*primary_900",
    checkbox_label_text_color_selected_dark="*primary_100",
    error_border_color_dark=err_dark,
    error_text_color_dark="*neutral_100",
    error_icon_color_dark=err_dark,
    input_background_fill_dark="*neutral_950",
    input_border_color_dark="*neutral_700",
    input_border_color_focus_dark="*primary_400",
    input_placeholder_color_dark="*neutral_500",
    loader_color_dark="*primary_300",
    slider_color_dark="*primary_400",
    stat_background_fill_dark="*primary_500",
    table_border_color_dark="*neutral_800",
    table_even_background_fill_dark="*neutral_900",
    table_odd_background_fill_dark="*neutral_950",
    table_row_focus_dark="*neutral_800",
    # buttons
    button_primary_background_fill_dark="*primary_500",
    button_primary_background_fill_hover_dark="*primary_400",
    button_primary_border_color_dark="*primary_500",
    button_primary_text_color_dark="white",
    button_secondary_background_fill_dark="*neutral_800",
    button_secondary_background_fill_hover_dark="*neutral_700",
    button_secondary_border_color_dark="*neutral_700",
    button_secondary_text_color_dark="*neutral_100",
    button_cancel_background_fill_dark=err_dark,
    button_cancel_background_fill_hover_dark=err_dark_muted,
)
light_mode = dict(
    # body attributes
    body_background_fill="*neutral_50",
    body_text_color="*neutral_800",
    body_text_color_subdued="*neutral_500",
    # element colours
    background_fill_primary="white",
    background_fill_secondary="*neutral_50",
    border_color_accent="*primary_300",
    border_color_primary="*neutral_200",
    color_accent_soft="*primary_50",
    # text
    link_text_color="*primary_600",
    link_text_color_active="*primary_700",
    link_text_color_visited="*primary_600",
    # layout atoms
    block_background_fill="white",
    block_border_color="*neutral_200",
    block_label_border_width="0px",
    block_label_background_fill="white",
    block_label_text_color="*neutral_600",
    block_shadow="none",
    block_title_text_color="*neutral_700",
    block_title_text_weight="600",
    panel_background_fill="white",
    panel_border_width="0px",
    # component atoms
    checkbox_background_color_selected="*primary_600",
    checkbox_border_color_focus="*primary_400",
    checkbox_border_color_selected="*primary_600",
    checkbox_label_background_fill="*neutral_100",
    checkbox_label_background_fill_selected="*primary_50",
    checkbox_label_border_color="*neutral_200",
    checkbox_label_text_color_selected="*primary_700",
    error_background_fill="#fef2f2",
    error_border_color=err_muted,
    error_text_color="*neutral_800",
    input_background_fill="white",
    input_border_color="*neutral_300",
    input_border_color_focus="*primary_400",
    input_placeholder_color="*neutral_400",
    loader_color="*primary_500",
    slider_color="*primary_500",
    stat_background_fill="*primary_500",
    table_border_color="*neutral_200",
    table_even_background_fill="white",
    table_odd_background_fill="*neutral_50",
    table_row_focus="*primary_50",
    # buttons
    button_primary_background_fill="*primary_600",
    button_primary_background_fill_hover="*primary_700",
    button_primary_border_color="*primary_600",
    button_primary_text_color="white",
    button_secondary_background_fill="white",
    button_secondary_background_fill_hover="*neutral_100",
    button_secondary_border_color="*neutral_300",
    button_secondary_text_color="*neutral_700",
    button_cancel_background_fill=err_muted,
    button_cancel_background_fill_hover=err,
    button_cancel_text_color="white",
)


class Kotaemon(Soft):
    """
    Official theme of Kotaemon.
    Public version: https://huggingface.co/spaces/lone17/kotaemon
    """

    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.indigo,
        secondary_hue: colors.Color | str = colors.indigo,
        neutral_hue: colors.Color | str = gray,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_md,
        font: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Inter"),
            "ui-sans-serif",
            "system-ui",
            "sans-serif",
        ),
        font_mono: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        self.name = "kotaemon"
        super().set(
            **common,
            **dark_mode,
            **light_mode,
        )
