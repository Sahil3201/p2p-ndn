from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64, random

class Base():
    def __init__(self, id):
        # Generate RSA key pair
        self.name = str(id)
        self.data = id+"_data"
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        self.public_key = self._private_key.public_key()

    def save_public_key(self, save_to_disk=True, return_type_string=True):
        # Serialize and save the public key
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        if(save_to_disk):
            with open(str(self.name).replace('/','')+'public_key.pem', 'wb') as f:
                f.write(pem)
        if(return_type_string):
            return pem.decode('utf-8')
        return pem

    def encrypt_message(self, message: str, public_key=None, public_key_str:str=None):
        assert public_key!=None or public_key_str!=None

        if(public_key_str):
            # Convert string to bytes
            pem_bytes = public_key_str.encode('utf-8')

            # Deserialize the public key from PEM format
            public_key = serialization.load_pem_public_key(
                pem_bytes,
                backend=default_backend()
            )

        ret = public_key.encrypt(
            message.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # print('encrypted_bytes:', ret, "\nencyrpted usign:", public_key_str)
        ret = base64.b64encode(ret).decode('utf-8')
        return ret #.encode()

    def decrypt_message(self, message):
        encrypted_bytes = base64.b64decode(message)
        # print('encrypted_bytes:', encrypted_bytes, "\nencyrpted usign:", self.save_public_key(save_to_disk=False))
        # Decrypt the message using the private key
        return self._private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def sign_message(self, message):
        return self._private_key.sign(
            str.encode(message),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def verify_messsage_with_publicKey(self, message, signature, pubKey):
        try:
            pubKey.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except InvalidSignature:
            print("Invalid signature!")
            return False
        except Exception as e:
            print("Exception:", e)
        else:
            return True

    def update(self):
        pass


class TrueFalse(Base):
    def __init__(self,id):
        super().__init__(id)
        self.data = random.choice([str(self.name)+' is on.', str(self.name)+' is off.'])

    def update(self):
        self.data = random.choice([str(self.name)+' is on.', str(self.name)+' is off.'])

class ValueRange(Base):
    def __init__(self, id, _min, _max, postfix_text=''):
        super().__init__(id)
        self._min = _min
        self._max = _max
        self.sensor_name = self.name.split('/')[-1]
        self.postfix_text = postfix_text
        self.data = self.sensor_name + ' level: ' + str(random.randint(self._min, self._max)) + self.postfix_text

    def update(self):
        self.data = self.sensor_name + ' level: ' + str(random.randint(self._min, self._max)) + self.postfix_text

class RandomText(Base):
    def __init__(self, id, _texts):
        super().__init__(id)
        self._texts = _texts
        self.sensor_name = self.name.split('/')[-1]
        self.data = self.sensor_name + ' level: ' + random.choice(self._texts)

    def update(self):
        self.data = self.sensor_name + ' level: ' + random.choice(self._texts)
