//------------------------------------------------------------------------------
//  movementmanager.cc
//  (C) 2020 Individual contributors, see AUTHORS file
//------------------------------------------------------------------------------
#include "application/stdneb.h"
#include "agnetmanager.h"
#include "basegamefeature/managers/entitymanager.h"
#include "properties/movement.h"
#include "properties/input.h"
#include "graphics/graphicsentity.h"
#include "math/scalar.h"
#include "models/modelcontext.h"
#include "timing/timer.h"
#include "util/random.h"
#include "basegamefeature/managers/timemanager.h"
#include "io/console.h"

namespace Demo
{

__ImplementSingleton(AgentManager)

//------------------------------------------------------------------------------
/**
*/
Game::ManagerAPI
AgentManager::Create()
{

    n_assert(!AgentManager::HasInstance());
    Singleton = n_new(AgentManager);

    Game::FilterCreateInfo filterInfo;
    filterInfo.inclusive[0] = Game::GetPropertyId("WorldTransform");
    filterInfo.access[0]    = Game::AccessMode::WRITE;
    filterInfo.inclusive[1] = Game::GetPropertyId("Agent");
    filterInfo.access[1]    = Game::AccessMode::WRITE;

    filterInfo.numInclusive = 2;

    Game::Filter filter = Game::CreateFilter(filterInfo);

    Game::ProcessorCreateInfo processorInfo;
    processorInfo.async = false;
    processorInfo.filter = filter;
    processorInfo.name = "AgentManager"_atm;
    processorInfo.OnBeginFrame = [](Game::Dataset data)
    {
        Game::TimeSource const* const time = Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY);
        for (int v = 0; v < data.numViews; v++)
        {
            Game::Dataset::CategoryTableView const& view = data.views[v];
            Math::mat4* const transforms = (Math::mat4*)view.buffers[0];
            Agent* const agents = (Agent*)view.buffers[1];

            for (IndexT i = 0; i < view.numInstances; ++i)
            {
                Math::mat4& t = transforms[i];
                Agent& a = agents[i];

                Math::vec4 p = Math::vec4(a.position, 1.0);
        
                t.position = p;
            }

        }
    };

    Game::ProcessorHandle pHandle = Game::CreateProcessor(processorInfo);

    Game::ManagerAPI api;
    api.OnActivate = &AgentManager::OnActivate;
    api.OnBeginFrame = &AgentManager::OnBeginFrame;
    api.OnFrame = &AgentManager::OnFrame;
    return api;
}

//------------------------------------------------------------------------------
/**
*/
void
AgentManager::Destroy()
{
    n_assert(AgentManager::HasInstance());
    n_delete(Singleton);
}

//------------------------------------------------------------------------------
/**
*/
void
AgentManager::OnActivate()
{
   
}

//------------------------------------------------------------------------------
/**
*/
void
AgentManager::OnBeginFrame()
{
   
}

//------------------------------------------------------------------------------
/**
*/
void
AgentManager::OnFrame()
{
    // empty
}

//------------------------------------------------------------------------------
/**
*/
AgentManager::AgentManager()
{
    // empty
}

//------------------------------------------------------------------------------
/**
*/
AgentManager::~AgentManager()
{
    // empty
}

} // namespace Game


