
import rclpy
from std_msgs.msg import String
from rclpy.node import Node


class SubscriberNodeClass(Node):

    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            String, 'topic_object_color', self.listener_callbackFunction, 10)

    def listener_callbackFunction(self, color_msg):
        self.get_logger().info('Received object color: %s' % color_msg.data)


def main(args=None):
    rclpy.init(args=args)
    subscriberNode = SubscriberNodeClass()
    rclpy.spin(subscriberNode)
    subscriberNode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
