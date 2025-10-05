import gradio as gr

def load_theme():
    return gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="teal",
        neutral_hue="slate",
        radius_size="md",
        text_size="md",
    ).set(
        button_primary_background_fill="*primary_400",
        button_primary_background_fill_hover="*primary_500",
        button_primary_text_color="white",
        button_primary_background_fill_dark="*primary_600",
        button_secondary_background_fill="*secondary_300",
        button_secondary_background_fill_hover="*secondary_400",
        button_secondary_text_color="white",
        block_title_text_color="*primary_500",
        block_label_text_color="*primary_400",
    )
