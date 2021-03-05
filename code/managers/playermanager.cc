//------------------------------------------------------------------------------
//  playermanager.cc
//  (C) 2020 Individual contributors, see AUTHORS file
//------------------------------------------------------------------------------
#include "application/stdneb.h"
#include "playermanager.h"
#include "input/inputserver.h"
#include "graphics/cameracontext.h"
#include "visibility/visibilitycontext.h"
#include "imgui.h"
#include "dynui/im3d/im3dcontext.h"
#include "graphicsfeature/graphicsfeatureunit.h"
#include "basegamefeature/managers/entitymanager.h"
#include "input/mouse.h"
#include "renderutil/mouserayutil.h"
#include "game/api.h"
#include "properties/movement.h"
#include "properties/input.h"
#include "scripting/python/pythonserver.h"
#include "math/scalar.h"

namespace Demo
{

__ImplementSingleton(PlayerManager)

//------------------------------------------------------------------------------
/**
*/
Game::ManagerAPI
PlayerManager::Create()
{
    n_assert(!PlayerManager::HasInstance());
    Singleton = n_new(PlayerManager);

    Game::ManagerAPI api;
    api.OnActivate = &PlayerManager::OnActivate;
    api.OnBeginFrame = &PlayerManager::OnBeginFrame;
    api.OnFrame = &PlayerManager::OnFrame;
    return api;
}

//------------------------------------------------------------------------------
/**
*/
void
PlayerManager::Destroy()
{
    n_assert(PlayerManager::HasInstance());
    n_delete(Singleton);
}

//------------------------------------------------------------------------------
/**
*/
void
PlayerManager::OnActivate()
{
    auto view = GraphicsFeature::GraphicsFeatureUnit::Instance()->GetDefaultView();
    auto stage = GraphicsFeature::GraphicsFeatureUnit::Instance()->GetDefaultStage();

    auto const windowId = Base::DisplayDeviceBase::Instance()->GetMainWindow();
    auto const displayMode = CoreGraphics::WindowGetDisplayMode(windowId);
    SizeT width = displayMode.GetWidth();
    SizeT height = displayMode.GetHeight();

    Game::EntityCreateInfo playerCreateInfo;
    playerCreateInfo.templateId = Game::GetTemplateId("Player/player"_atm);
    playerCreateInfo.immediate = true;
    Singleton->playerEntity = Game::CreateEntity(playerCreateInfo);
    
    Singleton->tdc = Game::GetProperty<Demo::TopdownCamera>(Singleton->playerEntity, Game::GetPropertyId("TopdownCamera"_atm));



    Math::mat4 camera_local_transform = Math::rotationx(Singleton->tdc.pitch) * Math::translation(0,0,-Singleton->tdc.height/Math::sin(Singleton->tdc.pitch));
    GraphicsFeature::Camera camera = Game::GetProperty<GraphicsFeature::Camera>(Singleton->playerEntity, Game::GetPropertyId("Camera"_atm));
    camera.aspectRatio = (float)width / (float)height;
    camera.viewHandle = GraphicsFeature::GraphicsFeatureUnit::Instance()->GetDefaultViewHandle();
    camera.localTransform = camera_local_transform;
    Game::SetProperty<GraphicsFeature::Camera>(Singleton->playerEntity, Game::GetPropertyId("Camera"_atm), camera);


    GraphicsFeature::GraphicsFeatureUnit::Instance()->AddRenderUICallback([]()
    {
        ImGui::Begin("Camera config");
        ImGui::SliderFloat("Camera height", &Singleton->tdc.height, 0.0001f, 100.0f);
        ImGui::SliderFloat("Camera pitch", &Singleton->tdc.pitch, 0.0001f, N_PI_HALF);
        ImGui::SliderFloat("Camera yaw", &Singleton->tdc.yaw, 0.0f, 2*N_PI_DOUBLE);
        ImGui::End();
    });



}

//------------------------------------------------------------------------------
/**
*/
void
PlayerManager::OnBeginFrame()
{
     auto input = Game::GetProperty<Demo::PlayerInput>(Singleton->playerEntity, Game::GetPropertyId("PlayerInput"_atm));
    // Move
    float move_forward = input.forward*0.2f;
    float move_strafe  = input.strafe *0.2f;
    float yaw          = Singleton->tdc.yaw;
    
    Singleton->target_pos.x += -sin(yaw) * move_forward - cos(yaw) * move_strafe;
    Singleton->target_pos.z +=  cos(yaw) * move_forward - sin(yaw) * move_strafe;
    
    Math::mat4 worldTransform = Game::GetProperty<Math::mat4>(Singleton->playerEntity, Game::GetPropertyId("WorldTransform"_atm));
    Math::vec4 pos = worldTransform.position;

    auto direction = Singleton->target_pos - pos;
    float length = Math::length3(direction);
    if( length > TINY ) // What to do here, maybe set pos to target_pos when dstance is small
    {
        direction = Math::normalize(direction) * (length*0.1);
        pos += direction;

        Game::SetProperty<Math::mat4>(Singleton->playerEntity, Game::GetPropertyId("WorldTransform"_atm), Math::translation({pos.x, pos.y, pos.z}));
    }

    // Update camera rotation and height.
    // Development only
    Math::mat4 camera_local_transform = 
        Math::rotationy(Singleton->tdc.yaw) *
        Math::rotationx(Singleton->tdc.pitch) *
        Math::translation(0,0,Singleton->tdc.height/Math::sin(-Singleton->tdc.pitch));

    GraphicsFeature::Camera camera = Game::GetProperty<GraphicsFeature::Camera>(Singleton->playerEntity, Game::GetPropertyId("Camera"_atm));
    camera.localTransform = camera_local_transform;
    Game::SetProperty<GraphicsFeature::Camera>(Singleton->playerEntity, Game::GetPropertyId("Camera"_atm), camera);

    if(input.scroll != 0)
    {
        Singleton->tdc.height += Singleton->tdc.height * 0.01 * input.scroll;
    }
}

//------------------------------------------------------------------------------
/**
*/
void
PlayerManager::OnFrame()
{
    
}

//------------------------------------------------------------------------------
/**
*/
PlayerManager::PlayerManager()
{
    // empty
}

//------------------------------------------------------------------------------
/**
*/
PlayerManager::~PlayerManager()
{
    // empty
}
    
Math::vec3 PlayerManager::RayCastMousePos()
{
    Math::vec2 mouse_pos = Input::InputServer::Instance()->GetDefaultMouse()->GetScreenPosition();
    GraphicsFeature::Camera camera = Game::GetProperty<GraphicsFeature::Camera>(Singleton->playerEntity, Game::GetPropertyId("Camera"_atm));
    Math::mat4 world_transform = Game::GetProperty<Math::mat4>(Singleton->playerEntity, Game::GetPropertyId("WorldTransform"_atm));
    const Math::mat4 view = world_transform * camera.localTransform;    
    const Math::mat4 proj = GraphicsFeature::CameraManager::GetProjection(camera.viewHandle); // viewHandle might be invalid
    Math::line ray = RenderUtil::MouseRayUtil::ComputeWorldMouseRay(
        mouse_pos,
        1000.0f,
        Math::inverse(view),
        Math::inverse(proj),
        0.1f
    );

    Math::point p1 = ray.pointat(-1);
    Math::point p2 = ray.pointat(0);

    Math::plane pl = Math::plane({0,0,0}, {0,1,0}); // xz-plane
    Math::point intersect_point;
    Math::intersectline(pl, p1, p2, intersect_point);
    
    intersect_point.y += 0.1f;
    Math::vec3 p = Math::vec3{intersect_point.x, intersect_point.y, intersect_point.z};
    
    return p;
}

} // namespace Game


