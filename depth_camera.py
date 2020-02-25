import pyrealsense2 as rs
pipe = rs.pipeline()
devices = rs.context()
number = devices.query_devices()
if len(number) == 0:
    print("fuck")
print(devices)
print(rs.device_list())
profile = pipe.start()
try:
  for i in range(0, 100):
    frames = pipe.wait_for_frames()
    for f in frames:
      print(f.profile)
finally:
    pipe.stop()