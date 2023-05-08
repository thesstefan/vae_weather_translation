import torch
from torch import nn
from typing import TypeAlias, cast

from teshub.extra_typing import Color

DEFAULT_SEG_COLORS: list[Color] = [
    (0, 0, 0),
    (22, 21, 22),
    (204, 204, 204),
    (46, 6, 243),
    (154, 147, 185),
    (198, 233, 255),
    (255, 53, 94),
    (250, 250, 55),
    (255, 255, 255),
    (115, 51, 128),
    (36, 179, 83),
    (119, 119, 119),
]
DEFAULT_SEG_COLOR2ID = {
    color: id for id, color in enumerate(DEFAULT_SEG_COLORS)
}

DEFAULT_SEG_LABELS: list[str] = [
    "background",
    "black_clouds",
    "white_clouds",
    "blue_sky",
    "gray_sky",
    "white_sky",
    "fog",
    "sun",
    "snow",
    "shadow",
    "wet_ground",
    "shadow_snow"
]
DEFAULT_SEG_LABEL2ID = {
    label: id for id, label in enumerate(DEFAULT_SEG_LABELS)
}

DEFAULT_LABELS: list[str] = [
    "snowy", "rainy", "foggy", "cloudy"
]
DEFAULT_LABELS_TO_ID = {
    label: id for id, label in enumerate(DEFAULT_LABELS)
}

# Should this be moved to teshub.extra_typing?
# Not sure if introducing the torch dependency there is worth it
NestedTorchDict: TypeAlias = (
    dict[str, "NestedTorchDict"] | list["NestedTorchDict"] | str | int |
    float | bool | None | torch.Tensor
)


def upsample_logits(logits: torch.Tensor, size: torch.Size) -> torch.Tensor:
    upsampled_logits: torch.Tensor = nn.functional.interpolate(
        logits, size=size, mode="bilinear", align_corners=False
    )

    return upsampled_logits.argmax(dim=1)


def load_model_hyperparams_from_checkpoint(
    checkpoint_path: str,
    device: torch.device
) -> dict[str, NestedTorchDict]:
    checkpoint: dict[str, NestedTorchDict] = torch.load(
        checkpoint_path, map_location=device)

    return cast(dict[str, NestedTorchDict], checkpoint['hyper_parameters'])