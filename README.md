# Python bindings

## Modules

### Demo

##### Functions
- HelloSayer: Says hello.
- SpawnCube: Spawns a cube, takes a nmath.Point as argument as the position to spawn the cube at.
- GetPlayer: Gets the player entity.
- SetCameraPos: The camera will move smoothly to this position, takes a nmath.Point as argument.
- GetFrameTime: Returns the between last and current frame.
- PauseTime: Pause the game time.
- UnPauseTime: Unpause the game time.
- IsTabDown: Returns true if the TAB key is down.
- IsPdown: Returns true if the P key is down.
- IsUpdown: Returns true if the UP arrow is down.
- IsDowndown: Returns true if the DOWN arrow is down.
- DrawBlueDot: Draws a blue dot. Takes pos: nmath.Point and a size: number as arguments.

##### Classes
- Entity: Represents an entity in nebula. Not all entities have all these members.
    - WorldTransform: Is a nmath.Mat4. Represents the WorldTransform property in nebula.
    - PlayerInput: Represents the Demo::PlayerInput property in nebula.
    - TopdownCamera: Represents the Demo::TopdownCamera property in nebula.
    - Movement: Represents the Demo::Movement property in nebula.
    - Marker: Represents the Demo::Marker property in nebula.
    - Agent : Represents the Demo::Agent property in nebula.
    - Camera: Represents the GraphicsFeature::Camera property in nebula.

### imgui
- Begin: Binding for ImGui::Begin.
- End: Binding for ImGui::End.
- Text: Binding for ImGui::TextUnformatted. Takes a string as argument.

