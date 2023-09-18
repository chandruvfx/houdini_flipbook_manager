# houdini flipbook manager

![flip_book_tool_1](https://github.com/chandruvfx/houdini_flipbook_manager/assets/45536998/5d69beeb-de47-4af0-8127-8b1b71ca6cca)

## Overview

An Houdini Flip Book manager HDA is a play blast tool which expedite artist to create batteries-included text based hud displays, favors submitting into the farm and publish the version to shotgrid. The HDA splitted into two sections. one is do all flipbook related task and another one is for RV related.

The Flip book tool features were,

* Text based tool includes all the text operations like resizing, colouring and positioning.
* Houdini Open-GL Farm submission support.
* Artist free lights inclusion from the houdini scene.
* Artist friendly real time channel parameters inclusion.
* Options that do , Draft Mov creations inside deadline and Publish into the shotgrid as versions.
* Play multiple exr files using RV for the given folder path.

## HDA Properties
### Folder Path & Version

![flip_book_tool_4](https://github.com/chandruvfx/houdini_flipbook_manager/assets/45536998/a4623d2f-ce63-44c5-ae8f-3b0d41cbe5fe)
The folder path field automatically resolve sgtk template path 'houdini_file_cache' of the respective project. Users were allowed to break this if they want to enter own folder path. //Note: Make sure the given path is the folder path not a file path//.

Artist can choose the choice of the version.// Note: Please Maintain the order in ascending order. random choice of number selection leads to confusions at certain time!!//

### Camera & Flip Book Name 

![flip_book_tool_5](https://github.com/chandruvfx/houdini_flipbook_manager/assets/45536998/44c6f97f-ea6e-4714-b769-e9ad19dced1f)

Artist can either manually select the camera or fill the current viewport camera by pressing `Use Viewport Camera` button.

A Flip book name is the name literal of the current HDA node and the name of the selected camera

### Header Text Settings 

![flip_book_tool_6](https://github.com/chandruvfx/houdini_flipbook_manager/assets/45536998/e57bba94-6c4d-40d6-b345-c2015e031fff)

Center Text and Right Text itself describes the placement of the hud text in the houdini viewport. center text places the custom hud text in the top center of the viewport . Right Text places the ud text into top right corner

### Center Text Settings 

![flip_book_tool_7](https://github.com/chandruvfx/houdini_flipbook_manager/assets/45536998/45af5ad4-352c-469b-8ff8-2b9715c22a46)

Text placed on the left top corner. This is in multi string format. Artist can add more than one line in the text

### Lights 
![flip_book_tool_8](https://github.com/chandruvfx/houdini_flipbook_manager/assets/45536998/260a4db2-ea62-43c6-b93f-481ec553756f)

Default it is empty. When submitting Open-GL render take no lights , all geos rendered as houdini raw viewport. Artist are allowed to add lights if they want

### Deadline Submission

![flip_book_tool_9](https://github.com/chandruvfx/houdini_flipbook_manager/assets/45536998/29280be2-c33b-4eb5-93d0-c3d10cb4e9da)

  * Job Name - Deadline job name. Default it is the cachename plus version name. Artist can enter his own prefered name
  * Comment - Valid textual deadline comments
  * Pool & Secondary pool - Drop-Down consist of deadline pools.
  * Group - Deadline Groups
  * Priority - Determine Deadline Priority
  * Frames-Per-Task - Determine Chunk size aka the split of frame ranges into the machines
  * **Make Mov** - A special case, Switching on this parameter while submission, shoot a dependency Draft deadline job. which created the mov of the generated exr files by the flipbook tool
  * **Publish Mov** - Another special case, Switching on this parameter, publishes the generated Mov to the Shotgrid version tab. Shotgrid automatically makes the thumbnail mov in minutes !!
  * Submit To Deadline - Push button collects all the deadline parameters values and submit into the deadline farm

### RV 

![flip_book_tool_10](https://github.com/chandruvfx/houdini_flipbook_manager/assets/45536998/78f7ab49-d180-47b7-b211-704b6259d36f)

For given folder path, Once artist click the load button, it list all the folders containing exrs. Artist Switch on the check box for the list of flipbook exrs to play in RV. Pressing play button open the RV with the loaded exr's!!



:point_down: [Youtube Link]

[![Houdini Flip book manager HDA Video](https://img.youtube.com/vi/hnLAP-H8VjE/0.jpg)](https://www.youtube.com/watch?v=hnLAP-H8VjE)

# houdini flipbook manager(Shotgrid Media upload)

[![Houdini Flip book manager with SG publish HDA Video](https://img.youtube.com/vi/-Dtw5MkruRU/0.jpg)](https://youtu.be/-Dtw5MkruRU)


VEX Pulling Camera Properties.
![cam_ptoperty](https://github.com/chandruvfx/houdini_flipbook_manager/assets/45536998/72fe07de-5daa-4133-aff0-81041ff89bc6)

VEX Used For Font SOP.
![cam_resolve](https://github.com/chandruvfx/houdini_flipbook_manager/assets/45536998/5a12efa7-1471-4d5b-bb78-61811a9d64ad)
