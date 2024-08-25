"""Specify the default values for excalidraw primitives."""
import os

# Font family for estimating font size
current_file_dir = os.path.dirname(os.path.abspath(__file__))
_fonts = {
    1: "fonts/Virgil.ttf",
    2: "fonts/Assistant-VariableFont.ttf",
    3: "fonts/CascadiaCode.ttf",
}
FONT_FAMILY = {x: os.path.join(current_file_dir, y) for x, y in _fonts.items()}

# Settings for Rectangle, Ellipse, Diamond
BOX_DEFAULTS = dict(
    angle=0,
    strokeColor="#000000",
    backgroundColor="transparent",
    fillStyle="hachure",
    strokeStyle="solid",
    strokeWidth=1,
    roughness=0,
    opacity=100,
    roundness={"type": 3},
    version=1,
    versionNonce=0,
    isDeleted=False,
    boundElements=[],
    updated=0,
    link=None,
    locked=False,
)

# Extra properties for Text
TEXT_DEFAULTS = dict(
    fontSize=20,
    fontFamily=3,
    textAlign="left",
    verticalAlign="top",
    baseline=18,
    containerId=None,
    originalText="default text",
    roundness=None,
)


# Extra properties for Line
LINE_DEFAULTS = dict(
    lastCommitedPoint=None,
    startBinding=None,
    endBinding=None,
    startArrowhead=None,
    endArrowhead=None,
    roundess={"type": 2},  # It has only two configurations None and type 2
)