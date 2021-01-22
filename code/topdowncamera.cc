#include "application/stdneb.h"

#include "topdowncamera.h"
#include "imgui.h"
#include "Math/vector.h"

namespace Demo
{

void TopDownCamera::Setup(Math::scalar height, Math::scalar pitch, Math::scalar yaw)
{
    this->position = Math::point(0,0,0);
    this->pitch = pitch;
    this->yaw = yaw;

    this->Update();
}

void TopDownCamera::Update()
{
    float speed_scalar = 1.0f;
    Math::vec4 move = {0,0,0,0};

    if(this->forwardKey)
        move.z -= 0.03f*speed_scalar;
    if(this->backwardKey)
        move.z += 0.03f*speed_scalar;

    if(this->leftKey)
        move.x -= 0.03f*speed_scalar;
    if(this->rightKey)
        move.x += 0.03f*speed_scalar;

    Math::mat4 yaw_rot = Math::rotationy(-this->yaw);
    move = yaw_rot * move;

    position += Math::vector(move.x, -move.y, move.z);

    view_mat = Math::translation(position.x, position.y, position.z);

    this->forwardKey = false;
    this->backwardKey = false;
    this->leftKey = false;
    this->rightKey = false;
}

const Math::mat4& TopDownCamera::GetTransform()
{
    return this->view_mat;
}
    
void TopDownCamera::DrawCameraControlUI()
{
    ImGui::Begin("Camera config");
    ImGui::SliderFloat("Camera height", &position.y, 0.0f, 100.0f);
    ImGui::SliderFloat("Camera pitch", &pitch, -N_PI_HALF, 0.0f);
    ImGui::SliderFloat("Camera yaw", &yaw, 0.0f, 2*N_PI_DOUBLE);
    ImGui::End();
}

} // namespace Demo
