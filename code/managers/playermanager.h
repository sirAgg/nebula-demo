#pragma once
//------------------------------------------------------------------------------
/**
	@class	Demo::PlayerManager

	(C) 2020 Individual contributors, see AUTHORS file
*/
//------------------------------------------------------------------------------
#include "core/refcounted.h"
#include "core/singleton.h"
#include "game/manager.h"
#include "util/stringatom.h"
#include "renderutil/freecamerautil.h"
#include "game/entity.h"
#include "Math/vector.h"
#include "Math/vec4.h"
#include "properties/input.h"

namespace Demo
{

class PlayerManager
{
	__DeclareSingleton(PlayerManager);
public:
	/// Create the singleton
	static Game::ManagerAPI Create();

	/// Destroy the singleton
	static void Destroy();

    inline Game::Entity get_player() {return playerEntity;}
    inline void set_target_pos(Math::point pos) {target_pos = pos.vec;}

    static Math::vec3 RayCastMousePos();

private:
	/// constructor
	PlayerManager();
	/// destructor
	~PlayerManager();

	/// called when attached to game server.
	static void OnActivate();
    /// called once before every rendered frame
    static void OnBeginFrame();
	/// called once every frame
	static void OnFrame();

	Game::Entity playerEntity;

    // Mainly used for changing camera rotation and height, probably not nessesary in release
    Demo::TopdownCamera tdc;

    Math::vec4 target_pos = {0,0,0,0};

    Math::vec3 ray_cast_mouse_pos = {0,0,0}; // only updated when mouse buttons is pressed
};;

} // namespace Demo
