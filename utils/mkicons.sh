#!/bin/sh


BASEDIR="icons"

LIGHTDIR="$BASEDIR/ubuntu-mono-light"
DARKDIR="$BASEDIR/ubuntu-mono-dark"

APP=classicmenu-indicator

LIGHT_ICON="$BASEDIR/hicolor/scalable/apps/${APP}-light.svg"
DARK_ICON="$BASEDIR/hicolor/scalable/apps/${APP}-dark.svg"


LIGHT=3c3c3c
DARK=dfdbd2


mkicon(){
    COLOR="$1"
    FILE="$2"
    mkdir -pv "$(dirname "$FILE")"
cat<<EOF > "$FILE"
<?xml version="1.0" encoding="utf-8"?>

<!-- License Agreement at http://iconmonstr.com/license/ -->

<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
         width="512px" height="512px" viewBox="0 0 512 512" enable-background="new 0 0 512 512" xml:space="preserve">
<path id="menu-3-icon" d="M275,163.5H50v-65h225V163.5z M275,223.5H50v65h225V223.5z M275,348.5H50v65h225V348.5z M319.105,217.908
        l71.447,87.121L462,217.908H319.105z"
style="fill:#$COLOR;fill-opacity:1;fill-rule:nonzero;stroke:none"/>
</svg>
EOF
}


mkicon "$LIGHT" "$LIGHT_ICON"
mkicon "$DARK" "$DARK_ICON"


for size in 16 22 24; do
    dir="$LIGHTDIR/status/$size"
    mkdir -pv "$dir"
    cp "$LIGHT_ICON" "$dir/${APP}.svg"

    dir="$DARKDIR/status/$size"
    mkdir -pv "$dir"
    cp "$DARK_ICON" "$dir/${APP}.svg"
done
