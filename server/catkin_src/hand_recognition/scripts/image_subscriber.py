import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from env import *


class ImageSubscriber():

    def __init__(self):
        self.image_subs = rospy.Subscriber("image", Image, callback=self._callback, queue_size=None)
        self.cvbridge = CvBridge()
        self.img_buf = None

    def wait_for_image(self):
        if self.img_buf is None:
            return None

        img = self.img_buf
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, dsize=(HEIGHT, WIDTH))
        img = (img.astype(np.float32) - 128) / 256

        self.img_buf = None

        return img

    def _callback(self, msg):
        cv_img = self.cvbridge.imgmsg_to_cv2(msg)
        self.img_buf = cv_img

