//------------------------------------------------------------------------------
//  pythonbindings.cc
//  (c) 2020 Magnus Lind
//------------------------------------------------------------------------------
#include "foundation/stdneb.h"
#include "pythonbindings.h"
#include "pybind11/pybind11.h"
#include "pybind11/operators.h"
#include "pybind11/cast.h"
#include "pybind11/pytypes.h"
#include "io/console.h"
#include "basegamefeature/managers/entitymanager.h"
#include "basegamefeature/managers/timemanager.h"
#include "game/api.h"
#include "math/mat4.h"
#include "math/point.h"
#include "timing/timer.h"
#include "properties/input.h"
#include "properties/movement.h"
#include "imgui.h"
#include "dynui/im3d/im3dcontext.h"
#include "input/keyboard.h"
#include "managers/playermanager.h"
#include "graphicsfeature/graphicsfeatureunit.h"
#include "ids/idgenerationpool.h"

#define defPropertyAccessor(type, name) def_property(#name,\
        [](Game::Entity& e){\
            if(Game::HasProperty(e, Game::GetPropertyId(#name))) {\
                return py::cast(Game::GetProperty<type>(e, Game::GetPropertyId(#name)));\
            } else {\
                throw pybind11::value_error("This entity does not have a '" #name "' property.");\
            }\
        }, [](Game::Entity& e, pybind11::object obj) {\
            if(Game::HasProperty(e, Game::GetPropertyId(#name))) {\
                Game::SetProperty<type>(e, Game::GetPropertyId(#name), pybind11::cast<type>(obj));\
            } else {\
                throw pybind11::value_error("This entity does not have a '" #name "' property.");\
            }\
        })

#define defReadWrite(s, field) def_readwrite(#field, &s::field)
#define defReadWriteVec3(s, field) def_property(#field,\
        [](s& e){ return pybind11::cast(Math::point(e.field));},\
        [](s& e, pybind11::object obj){ e.field = pybind11::cast<Math::point>(obj).vec;})

namespace Python
{

namespace py = pybind11;

PYBIND11_EMBEDDED_MODULE(demo, m)
{
    py::class_<Game::Entity>(m, "Entity")
        .defPropertyAccessor(Math::mat4,            WorldTransform)
        .defPropertyAccessor(Demo::PlayerInput,     PlayerInput)
        .defPropertyAccessor(Demo::TopdownCamera,   TopdownCamera)
        .defPropertyAccessor(Demo::Movement,        Movement)
        .defPropertyAccessor(Demo::Marker,          Marker)
        .defPropertyAccessor(Demo::Agent,           Agent)
        .defPropertyAccessor(GraphicsFeature::Camera, Camera);

    m.def("Delete", [](Game::Entity& e)
            {
                Game::DeleteEntity(e);
            });

    m.def("IsValid", [](Game::Entity& e)
            {
                return Game::IsValid(e);
            });

    py::class_<Demo::PlayerInput>(m, "PlayerInput")
        .defReadWrite(Demo::PlayerInput, forward)
        .defReadWrite(Demo::PlayerInput, strafe)
        .defReadWrite(Demo::PlayerInput, left_mouse)
        .defReadWrite(Demo::PlayerInput, right_mouse);

    py::class_<GraphicsFeature::Camera>(m, "Camera")
        .defReadWrite(GraphicsFeature::Camera, viewHandle)
        .defReadWrite(GraphicsFeature::Camera, localTransform)
        .defReadWrite(GraphicsFeature::Camera, fieldOfView)
        .defReadWrite(GraphicsFeature::Camera, aspectRatio)
        .defReadWrite(GraphicsFeature::Camera, zNear)
        .defReadWrite(GraphicsFeature::Camera, zFar)
        .defReadWrite(GraphicsFeature::Camera, orthographicWidth);
    
    py::class_<Demo::TopdownCamera>(m, "TopdownCamera")
        .defReadWrite(Demo::TopdownCamera, height)
        .defReadWrite(Demo::TopdownCamera, pitch)
        .defReadWrite(Demo::TopdownCamera, yaw);
    
    py::class_<Demo::Movement>(m, "Movement")
        .defReadWriteVec3(Demo::Movement, direction)
        .defReadWrite(Demo::Movement, speed)
        .defReadWrite(Demo::Movement, wanderRadius)
        .defReadWrite(Demo::Movement, wanderDistance)
        .defReadWrite(Demo::Movement, wanderJitter)
        .defReadWrite(Demo::Movement, maximumDistance)
        .defReadWrite(Demo::Movement, target_entity);
    
    py::class_<Demo::Marker>(m, "Marker")
        .defReadWriteVec3(Demo::Marker, position);
 
    py::class_<Demo::Agent>(m, "Agent")
        .defReadWriteVec3(Demo::Agent, position)
        .defReadWrite(Demo::Agent, tiredness)
        .defReadWrite(Demo::Agent, hunger)
        .defReadWrite(Demo::Agent, thirst)
        .defReadWrite(Demo::Agent, social_metric)
        .defReadWrite(Demo::Agent, money)
        .defReadWrite(Demo::Agent, food_storage);


    m.def("HelloSayer", [](){IO::Console::Instance()->Print("I am saying HELLO!!!");}, "Says hello.");
    m.def("SpawnCube", [](Math::point& p){
            Game::EntityCreateInfo info;
            info.immediate = true;
            info.templateId = Game::GetTemplateId("MovingEntity/cube"_atm);
            Game::Entity entity = Game::CreateEntity(info);
            Game::SetProperty(entity, Game::GetPropertyId("WorldTransform"_atm), Math::translation(p.vec));
            return entity;
            });

    m.def("SpawnEntity", [](char* name){
            Util::StringAtom atom = Util::StringAtom(name);
            Game::EntityCreateInfo info;
            info.immediate = true;
            info.templateId = Game::GetTemplateId(atom);
            auto e = Game::CreateEntity(info);
            n_printf("created entity %d %d\n", Ids::Generation(e.id), Ids::Index(e.id));
            return e;
            });

    m.def("GetPlayer", [](){return Demo::PlayerManager::Instance()->get_player();});
    m.def("SetCameraPos", [](Math::point p){Demo::PlayerManager::Instance()->set_target_pos(p);});


    m.def("GetTime",       [](){return Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->time;});
    m.def("GetFrameTime",  [](){return Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->frameTime;});
    m.def("PauseTime",     [](){Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->pauseCounter++;});
    m.def("UnPauseTime",   [](){Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->pauseCounter--;});
    m.def("SetTimeFactor", [](float factor){Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->timeFactor = factor;});

    m.def("IsLeftMouseDown", []() -> bool
            {
                 auto input = Game::GetProperty<Demo::PlayerInput>(Demo::PlayerManager::Instance()->get_player(), Game::GetPropertyId("PlayerInput"_atm));
                 return input.left_mouse;
            });
    m.def("IsRightMouseDown", []() -> bool
            {
                 auto input = Game::GetProperty<Demo::PlayerInput>(Demo::PlayerManager::Instance()->get_player(), Game::GetPropertyId("PlayerInput"_atm));
                 return input.right_mouse;
            });
    m.def("RayCastMousePos", []()
            {
                auto p = Demo::PlayerManager::RayCastMousePos();
                return Math::point(p.vec);
            });

    m.def("IsTabDown", []()
            {
                auto& io = ImGui::GetIO();
                if (!io.WantCaptureMouse)
                    return io.KeysDown[Input::Key::Tab];
                else
                    return false;
            });
    m.def("IsPdown", []()
            {
                auto& io = ImGui::GetIO();
                if (!io.WantCaptureMouse)
                    return io.KeysDown[Input::Key::P];
                else
                    return false;
            });
    m.def("IsUpdown", []()
            {
                auto& io = ImGui::GetIO();
                if (!io.WantCaptureMouse)
                    return io.KeysDown[Input::Key::Up];
                else
                    return false;
            });
    m.def("IsDowndown", []()
            {
                auto& io = ImGui::GetIO();
                if (!io.WantCaptureMouse)
                    return io.KeysDown[Input::Key::Down];
                else
                    return false;
            });

    m.def("DrawDot", [](Math::point& p, float size, Math::vec4& color)
            {
                Math::vec3 v = p.vec;
                Im3d::Im3dContext::DrawPoint(v, size, color);
            });
    m.def("DrawLine", [](Math::point& p1, Math::point& p2, float size, Math::vec4& color)
            {
                Im3d::Im3dContext::DrawLine(Math::line(p1,p2), size, color);
            });
    m.def("DrawBox", [](Math::point& p, float size, Math::vec4& color)
            {
                Math::mat4 m = Math::scaling(size) * Math::translation(p.vec);
                Im3d::Im3dContext::DrawBox(m, color);
            });
}



PYBIND11_EMBEDDED_MODULE(imgui, m)
{
    m.def("Begin", &ImGui::Begin);
    m.def("End", &ImGui::End);
    m.def("Text", [](const char* text){ImGui::TextUnformatted(text);});
}

}
