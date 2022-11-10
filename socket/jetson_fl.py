from pickle_socket import Client, Message, FLAGS
import tensorflow as tf
import numpy as np

class FLClient:
    def __init__(self, id, host = 'localhost', port = 20000):
        self.id = id
        self.sock_client = Client()
        self.sock_client.connect(id, host, port)
       
     
    def task(self):
        while True:
            msg = self.sock_client.recv()

            if msg.flag == FLAGS.TERMINATE:
                return

            if msg.flag == FLAGS.FLAG_START_TRAIN:
                self.respond_train(msg)

            if msg.flag == FLAGS.FLAG_SETUP:
                self.respond_setup(msg) 
        
        
    
    def respond_setup(self, msg):
        print(f"client {self.id} setup started")
        try:
            # 1. gets dataset
            data = msg.data
            dataset_name = data['dataset_name']
            (self.x_train, self.y_train), (self.x_test, self.y_test) = self.prepare_dataset(dataset_name)
           
           
            # 2. builds model from json
            model_arch = data['arch']
            import threading
            lock = threading.Lock()
            self.model = tf.keras.models.model_from_json(model_arch, custom_objects={"null":None})

            # 3. compile model 
            optimizer, loss, metrics = tf.keras.optimizers.deserialize(data['optim']), tf.keras.losses.deserialize(data['loss']), data['metrics']
            self.model.compile(optimizer=optimizer,loss=loss,metrics=metrics)
            
            # 4. test model
            test_idxs = np.random.choice(len(self.x_train), 100)
            split_x_train, split_y_train = self.x_train[test_idxs], self.y_train[test_idxs]

            print(f"client {self.id} started test training")
            lock.acquire()
            self.model.fit(split_x_train, split_y_train, epochs=1, batch_size=8, verbose=2)
            lock.release()
            self.send_msg(flag=FLAGS.FLAG_HEALTH_CODE, data=FLAGS.RESULT_OK)
        
        except Exception as e:
            print(e)
            self.send_msg(flag=FLAGS.FLAG_HEALTH_CODE, data=FLAGS.RESULT_BAD)

    def respond_train(self, msg):
        print(f"client {self.id} training started")
        data = msg.data
        data_idxs = data['data_idxs']
        param = data['param']
        epochs = data['epochs']
        batch_size = data['batch_size']

        if param != None:
            param = list(map(lambda weight: np.array(weight), param))
            self.model.set_weights(param)
            
        split_x_train, split_y_train = self.x_train[data_idxs], self.y_train[data_idxs]

        self.model.fit(split_x_train, split_y_train, epochs=epochs, batch_size=batch_size, verbose=0)

        self.send_msg(FLAGS.FLAG_START_TRAIN, data=list(map(lambda layer: layer.tolist(), self.model.get_weights())))
        print(f"client {self.id} training completed")

    def prepare_dataset(self, name):
        if name == "mnist":
            (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
            x_train = x_train.reshape(-1, 28, 28, 1) # infer length (-1), h, w, c
            x_test  = x_test.reshape(-1, 28, 28, 1)
            return (x_train, y_train), (x_test, y_test)
            
        if name == "cifar10":
            return tf.keras.datasets.cifar10.load_data()

        if name == "fmnist":
            (x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
            x_train = x_train.reshape(-1, 28, 28, 1) # infer length (-1), h, w, c
            x_test  = x_test.reshape(-1, 28, 28, 1)
            return (x_train, y_train), (x_test, y_test)

    def send_msg(self, flag, data=None):
        msg = Message(source=self.id, flag=flag, data=data)
        self.sock_client.send(msg)