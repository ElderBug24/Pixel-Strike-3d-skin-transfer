# Little project helping people transfer Minecraft skins into Pixel Strike 3D

## Requirements:
 - <ins>**Python 3**</ins>
   - Pillow
   - Matplotlib
   - Pyautogui

Note that when running the script it will automatically install all of the required dependencies (except Python of course).

Skin Transferer allows you to transfer your Minecraft skin to Pixel Strike 3D.

## Here are all the available functions and their description.

<ins>**help**</ins> : Displays all the currently available functions

<ins>**version**</ins> : Displays the version of the current release of the application.

<ins>**exit**</ins> : Exits the application.

<ins>**open**</ins> : Opens an image file as the skin to use.
 - Usage: open [filename]

<ins>**select**</ins> : Selects the area to transfer.
 - Usage: select [mode]
 - The two modes are:
  - "position": select position x1 y1 x2 y2
   - Here x1 and x2 represent the coordinates of the top left corner of the selection
   - And x2 and y2 the coordinates of the bottom right corner
  - "part": select part [part]
   - Here [part] represents the part. Here are the available part presets:
    - All the part have this form: [part]_[face] or [part]_[face]_[layer].
    - The available parts are "head", "body", "rarm", "larm", "rleg" and "lleg".
    - The available faces are "front", "right", "left", "back", "top" and "bottom".

<ins>**store**</ins> : Stores the current selection in memory. Confirmation required if a selection is already stored.

<ins>**restore**</ins> : Restores the stored selection from the memory as the active selection. Confirmation required.

<ins>**show**</ins> : Displays the current selection.
 - Type "show stored" to show the stored selection.

<ins>**add_on_top**</ins> : Adds the current selection on top of the stored selection.

<ins>**transfer**</ins> : Transfers the selected area using a specific pattern that you specify.
 - Usage: transfer [preset]
  - Here [preset] represents the preset you want to use.
  - You can choose any of the following:
   - "head": 16 x 16
   - "body0": 8 x 12
   - "body1": 4 x 12
   - "body2": 12 x 4
   - "arm0": 4 x 12
   - "arm1": 4 x 4
   - "leg0": 4 x 12
   - "leg1": 4 x 4

<ins>**auto_transfer_face**</ins> : Transfers a face of a part of the skin while adding the layer of the face on top of it as well.
 - Usage: auto_transfer_face [part]_[face].
  - The available parts are "head", "body", "rarm", "larm", "rleg" and "lleg".
  - The available faces are "front", "right", "left", "back", "top" and "bottom".

<ins>**auto_transfer_part**</ins> : Transfers a part of the skin.
 - Usage: auto_transfer_face [part].
  - The available parts are "head", "body", "rarm", "larm", "rleg" and "lleg".

<ins>**auto_transfer_skin**</ins> : Transfers the skin. Need to open an image file as the skin to use first.
