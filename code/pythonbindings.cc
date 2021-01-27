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
//#include "scripting/python/conversion.h"

#define defPropertyAccessor(type, name) def_property(#name,\
        [](Game::Entity& e){\
            if(Game::HasProperty(e, Game::GetPropertyId(#name))) {\
                return py::cast(Game::GetProperty<type>(e, Game::GetPropertyId(#name)));\
            } else {\
                PyErr_SetNone(Py_None); return pybind11::cast(NULL);\
            }\
        }, [](Game::Entity& e, pybind11::object obj) {\
            if(Game::HasProperty(e, Game::GetPropertyId(#name))) {\
                Game::SetProperty<type>(e, Game::GetPropertyId(#name), pybind11::cast<type>(obj));\
            } else {\
                PyErr_SetNone(Py_None);\
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
        .defPropertyAccessor(Demo::Marker,          Marker);
    m.def("Delete", [](Game::Entity& e)
            {
                Game::DeleteEntity(e);
            });

    py::class_<Demo::PlayerInput>(m, "PlayerInput")
        .defReadWrite(Demo::PlayerInput, forward)
        .defReadWrite(Demo::PlayerInput, strafe)
        .defReadWrite(Demo::PlayerInput, spawn_marker);
    
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
            return Game::CreateEntity(info);
            });

    ////m.def("SpawnEntity")

    m.def("GetFrameTime", [](){return Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->frameTime;});
    m.def("PauseTime", [](){return Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->pauseCounter++;});
    m.def("UnPauseTime", [](){return Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->pauseCounter--;});
}


}