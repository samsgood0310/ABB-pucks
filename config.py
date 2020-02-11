import math
import cv2

cap = cv2.VideoCapture(1)
px_width = 1280
px_height = 960
cap.set(3, px_width)
cap.set(4, px_height)

puckdict = {}

if __name__ == "__main__":

    if "hei" not in puckdict:
        puckdict["puck3"] = {"position": (10, 20), "angle": 5}
        puckdict["puck2"] = {"position": (30, 50), "angle": 50}
        puckdict["puck7"] = {"position": (25, 30), "angle": -40}
        puckdict["puck4"] = {"position": (23, 10), "angle": 31}


        """for key, value in puckdict.items():
            print(value["position"])
            
        for key, value in puckdict.items():
            puckdict[value]["position"] = tuple()"""

        #for key in puckdict:
            #puckdict[key]["position"] = (puckdict[key]["position"][1], puckdict[key]["position"][0])
            #print(value["position"])

        print(puckdict)

        a,b=(1,0,0,1),(2,1,0,1)
        print(a+b)
        c = map(lambda x,y: x+y,a,b)
        print((c))

        trans = [[20,30,40],[50,20,30]]

        print("[[" + ','.join(
                    [str(s) for s in trans]) + "],[0, 1, 0, 0],[-1,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]]")

        print("[[" + str(trans) + "], [0, 1, 0, 0]]")
        #print(puckdict.items())
        for key in sorted(puckdict):
            puckdict[key]["position"] = list(puckdict[key]["position"] + (90,))
            print(puckdict[key])

        #robtarget = puckdict["puck4"]["position"] + (90,)
        #print(robtarget)

        a = (2,3)
        b = list(a)
        print(b)
        w,x,y,z = [0,0.71,0.71,0]
        t1 = +2.0 * (w * z + x * y)
        t2 = +1.0 - 2.0 * (y * y + z * z)
        rotation_z = math.degrees(math.atan2(t1, t2))
        print(rotation_z, "hei")