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


    Singleton->camera.Setup(0, 0, 0);

    GraphicsFeature::GraphicsFeatureUnit::Instance()->AddRenderUICallback([]()
    {

        static Math::line ray;
        static Math::vec3 p;
        static int num_of_boxes = 0;
        if (Input::InputServer::Instance()->GetDefaultMouse()->ButtonPressed(Input::MouseButton::Code::RightButton))
        {
            Math::vec2 mouse_pos = Input::InputServer::Instance()->GetDefaultMouse()->GetScreenPosition();
            //IO::Console::Instance()->Print("mouse_pos: %f, %f", mouse_pos.x, mouse_pos.y);
        
            GraphicsFeature::Camera camera = Game::GetProperty<GraphicsFeature::Camera>(Singleton->playerEntity, Game::GetPropertyId("Camera"_atm));
            Math::mat4 world_transform = Game::GetProperty<Math::mat4>(Singleton->playerEntity, Game::GetPropertyId("WorldTransform"_atm));
            const Math::mat4 view = world_transform * camera.localTransform;    
            const Math::mat4 proj = GraphicsFeature::CameraManager::GetProjection(camera.viewHandle); // viewHandle might be invalid
            ray = RenderUtil::MouseRayUtil::ComputeWorldMouseRay(
                mouse_pos,
                1000.0f,
                Math::inverse(view),
                Math::inverse(proj),
                0.1f
            );


            Math::point p1 = ray.pointat(-1);
            Math::point p2 = ray.pointat(10);

            Math::plane pl = Math::plane({0,0,0}, {0,1,0});
            Math::point intersect_point;
            Math::intersectline(pl, p1, p2, intersect_point);
            
            intersect_point.y += 0.1f;
            p = Math::vec3{intersect_point.x, intersect_point.y, intersect_point.z};
            

            Game::EntityCreateInfo info;
            info.immediate = true;
            info.templateId = Game::GetTemplateId("MarkerEntity/markerentity"_atm);
            Game::Entity entity = Game::CreateEntity(info);
            Math::vec3 new_pos = p + Math::vec3{0,0.5,0};
            Game::SetProperty(entity, Game::GetPropertyId("WorldTransform"_atm), Math::translation(new_pos));


            num_of_boxes++;
            IO::Console::Instance()->Print("boxes: %d", num_of_boxes);
        }





        Im3d::Im3dContext::DrawLine(ray, 2.0f, { 1.0f, 0.3f, 0.0f, 1.0f });
        Im3d::Im3dContext::DrawPoint(p, 20.0, {0,0,1,1});

        ImGui::Begin("Camera config");
        ImGui::SliderFloat("Camera height", &Singleton->tdc.height, 0.0001f, 100.0f);
        ImGui::SliderFloat("Camera pitch", &Singleton->tdc.pitch, 0.0001f, N_PI_HALF);
        ImGui::SliderFloat("Camera yaw", &Singleton->tdc.yaw, 0.0f, 2*N_PI_DOUBLE);
        ImGui::End();

    });
        
    Game::FilterCreateInfo info;
    info.inclusive[0] = Game::GetPropertyId("WorldTransform");
    info.access[0]    = Game::AccessMode::READ;
    info.inclusive[0] = Game::GetPropertyId("Marker");
    info.access[0]    = Game::AccessMode::READ;
    info.numInclusive = 2;

    Game::Filter filter = Game::CreateFilter(info);

    Game::ProcessorCreateInfo processorInfo;
    processorInfo.async = false;
    processorInfo.filter = filter;
    processorInfo.name = "DrawGreenDotsManager";
    processorInfo.OnRenderDebug = [](Game::Dataset data)
    {
        for (int v = 0; v < data.numViews; v++)
        {
            Game::Dataset::CategoryTableView const& view = data.views[v];
            Math::mat4* const transforms = (Math::mat4*)view.buffers[0];

            for(IndexT i = 0; i < view.numInstances; i++)
            {
                Math::vec4 p = transforms[i].position;
                Im3d::Im3dContext::DrawPoint({p.x, p.y, p.z}, 10.0f, {1,0,0,1} );
            }
        }
    };
}

//------------------------------------------------------------------------------
/**
*/
void
PlayerManager::OnBeginFrame()
{
    auto& io = ImGui::GetIO();
    if (!ImGui::GetIO().WantCaptureMouse)
    {
        Singleton->camera.SetForwardKey(io.KeysDown[Input::Key::W]);
        Singleton->camera.SetBackwardKey(io.KeysDown[Input::Key::S]);
        Singleton->camera.SetLeftKey(io.KeysDown[Input::Key::A]);
        Singleton->camera.SetRightKey(io.KeysDown[Input::Key::D]);
        Singleton->camera.Update();
    }

    //Math::mat4 worldTransform = Game::GetProperty(Singleton->playerEntity, Game::GetPropertyId("WorldTransform"_atm));
    Game::SetProperty<Math::mat4>(Singleton->playerEntity, Game::GetPropertyId("WorldTransform"_atm), Singleton->camera.GetTransform());
    Math::mat4 camera_local_transform = Math::rotationy(Singleton->tdc.yaw) * Math::rotationx(Singleton->tdc.pitch) * Math::translation(0,0,-Singleton->tdc.height/Math::sin(Singleton->tdc.pitch));
    GraphicsFeature::Camera camera = Game::GetProperty<GraphicsFeature::Camera>(Singleton->playerEntity, Game::GetPropertyId("Camera"_atm));
    camera.localTransform = camera_local_transform;
    Game::SetProperty<GraphicsFeature::Camera>(Singleton->playerEntity, Game::GetPropertyId("Camera"_atm), camera);
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

} // namespace Game


