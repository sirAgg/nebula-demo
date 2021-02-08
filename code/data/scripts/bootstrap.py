try:
    import demo, nmath, util, imgui
    print("Bootstrap successful.");

    def SetFieldOfView(fov):
        p = demo.GetPlayer()
        c = p.Camera
        c.fieldOfView = fov
        p.Camera = c

        p.Camera.fieldOfView = fov

except:
    print("Bootstrap failed.")

def NebulaUpdate():
    pass
def NebulaDraw():
    pass



