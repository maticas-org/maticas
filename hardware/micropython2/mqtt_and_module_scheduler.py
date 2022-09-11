from time import sleep, ticks_ms


class MQTTModuleScheduler():

    def __init__(self, mqtt_conn, module):

        self.mqtt_conn  = mqtt_conn
        self.module     = module
        self.pub_topics = self.module.pub_topics

    def send_messages(self):

        for alias in self.pub_topics.keys():

            # gets the measurement

            if self.pub_topics[alias]["exec"] == "":
                print("topic \"{}\" has no candidate for answering a call".format(alias))
                continue

            value = str(self.pub_topics[alias]["exec"]())

            # sends the measurement
            self.mqtt_conn.publish(topic = self.pub_topics[alias]["topic"], msg = value)
            sleep(0.1)
            print("message sent on topic {}".format(self.pub_topics[alias]["topic"]))

    def deep_sleep(self):

        """
            Sets the module on deep sleep.
        """

        pass 

    def wake_up(self):
        """
            Wakes the module up, and connects back to wifi and mqtt broker.
        """
        pass


    def loop(self):

        while True:

            self.send_messages()
            sleep(0.1)
            self.deep_sleep()
            self.wake_up()


