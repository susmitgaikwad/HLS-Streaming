import datetime
from kafka import KafkaConsumer
import numpy as np
import cv2

# Fire up the Kafka Consumer
topic = "TATA"

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=['10.30.0.120:9092'])

def get_video_stream():
    """
    Here is where we recieve streamed images from the Kafka Server and convert
    them to a Flask-readable format.
    """
    frames = 0
    for msg in consumer:
        # For every frame that is consumed, value contains image bytes
        msg = np.frombuffer(msg.value, np.uint8)
        # key = np.frombuffer(msg.key, np.uint8)

        # Decode bytes into an image
        msg = cv2.imdecode(msg, cv2.IMREAD_COLOR)

        # Get arguments for VideoWriter object
        date = datetime.datetime.now().replace(microsecond=0)
        name = 'VID_' + str(date).replace(' ', '_') + '.mp4'
        height, width, layers = msg.shape

        # Create new VideoWriter
        if frames == 0:
            # fourcc = cv2.VideoWriter_fourcc('F', 'M', 'P', '4')
            video = cv2.VideoWriter(name, 0x7634706d, 5, (width, height))

        # Write frame to video and increase frame count
        video.write(msg)
        frames += 1
        # cv2.imwrite(name,msg)

        # If 80 frames are done, relesea video and start frame count again
        if frames == 80:
            cv2.destroyAllWindows()
            video.release()
            frames = 0


if __name__ == "__main__":
    get_video_stream()