#ifndef TOPDOWNCAMERA_H
#define TOPDOWNCAMERA_H 

#include "Math/mat4.h"
#include "Math/point.h"

namespace Demo
{

class TopDownCamera
{
public:

    /// sets up camera
    void Setup(Math::scalar height, Math::scalar pitch, Math::scalar yaw);
    /// updates camera matrix
    void Update();
    /// returns transform of camera
    const Math::mat4& GetTransform();

    void SetForwardKey(bool state);
    void SetBackwardKey(bool state);
    void SetRightKey(bool state);
    void SetLeftKey(bool state);

    void DrawCameraControlUI();

private:

    Math::mat4  view_mat;

    Math::point position;

    Math::scalar pitch;
    Math::scalar yaw;

    bool forwardKey;
    bool backwardKey;
    bool rightKey;
    bool leftKey;
    
};

inline void TopDownCamera::SetForwardKey(bool state)
{
    this->forwardKey = state;
}
inline void TopDownCamera::SetBackwardKey(bool state)
{
    this->backwardKey = state;
}
inline void TopDownCamera::SetRightKey(bool state)
{
    this->rightKey = state;
}
inline void TopDownCamera::SetLeftKey(bool state)
{
    this->leftKey = state;
}

} // namespace Demo
#endif /* TOPDOWNCAMERA_H */
