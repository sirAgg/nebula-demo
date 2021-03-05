//------------------------------------------------------------------------------
//  inputmanager.cc
//  (C) 2020 Individual contributors, see AUTHORS file
//------------------------------------------------------------------------------
#include "application/stdneb.h"
#include "inputmanager.h"
#include "input/inputserver.h"
#include "input/mouse.h"
#include "input/keyboard.h"
#include "basegamefeature/managers/entitymanager.h"
#include "properties/input.h"
#include "imgui.h"
#include "graphicsfeature/graphicsfeatureunit.h"

namespace Demo
{

__ImplementSingleton(InputManager)

//------------------------------------------------------------------------------
/**
*/
Game::ManagerAPI
InputManager::Create()
{
    n_assert(!InputManager::HasInstance());
    Singleton = n_new(InputManager);

    Game::ManagerAPI api;
    api.OnActivate = &InputManager::OnActivate;
    api.OnBeginFrame = &InputManager::OnBeginFrame;
    return api;
}

//------------------------------------------------------------------------------
/**
*/
void
InputManager::Destroy()
{
    n_assert(InputManager::HasInstance());
    n_delete(Singleton);
}

//------------------------------------------------------------------------------
/**
*/
void
InputManager::OnActivate()
{
}

//------------------------------------------------------------------------------
/**
*/
void
ProcessPlayerInput()
{
    Ptr<Input::Keyboard> const& keyboard = Input::InputServer::Instance()->GetDefaultKeyboard();
    Ptr<Input::Mouse> const& mouse = Input::InputServer::Instance()->GetDefaultMouse();

    Game::FilterCreateInfo info;
    info.inclusive[0] = Game::GetPropertyId("PlayerInput"_atm);
    info.access[0]    = Game::AccessMode::WRITE;
    info.numInclusive = 1;

    Game::Filter filter = Game::CreateFilter(info);

    Game::Dataset data = Game::Query(filter);
    for(int v = 0; v < data.numViews; v++)
    {
        Game::Dataset::CategoryTableView const& view = data.views[v];
        Demo::PlayerInput* const player_inputs = (Demo::PlayerInput*)view.buffers[0];

        for(int i = 0; i < view.numInstances; i++)
        {
            Demo::PlayerInput& input = player_inputs[i];

            auto& io = ImGui::GetIO();
            if(!io.WantCaptureMouse)
            {
                input.forward = (char)io.KeysDown[Input::Key::W] - (char)io.KeysDown[Input::Key::S];
                input.strafe  = (char)io.KeysDown[Input::Key::D] - (char)io.KeysDown[Input::Key::A];
                input.left_mouse  = mouse->ButtonPressed(Input::MouseButton::Code::LeftButton);
                input.right_mouse = mouse->ButtonPressed(Input::MouseButton::Code::RightButton);
                input.scroll  = (char)mouse->WheelForward();
                if(mouse->WheelForward())  IO::Console::Instance()->Print("Forward");
                if(mouse->WheelBackward()) IO::Console::Instance()->Print("Backward");

            }
            else
            {
                input.forward = 0;
                input.strafe  = 0;
                input.left_mouse = false;
                input.right_mouse = false;
                input.scroll = 0;
            }
        }
    }
}

//------------------------------------------------------------------------------
/**
*/
void
InputManager::OnBeginFrame()
{
    ProcessPlayerInput();
}

//------------------------------------------------------------------------------
/**
*/
InputManager::InputManager()
{
    // empty
}

//------------------------------------------------------------------------------
/**
*/
InputManager::~InputManager()
{
    // empty
}


} // namespace Game


