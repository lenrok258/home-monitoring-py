class Serial:
    current_byte_pointer = 0
    bytes_array = [
        b'\x42', b'\x4d',
        b'\xff', b'\xff',
        b'\x00', b'\x01',
        b'\x00', b'\x02',
        b'\x00', b'\x03',
        b'\x00', b'\x04',
        b'\x00', b'\x05',
        b'\x00', b'\x06',
        b'\x00', b'\x07',
        b'\x00', b'\x08',
        b'\x00', b'\x09',
        b'\x00', b'\x0a',
        b'\x00', b'\x0b',
        b'\x00', b'\x0c',
        b'\x00', b'\x0d',
        b'\x00', b'\x0e']

    def __init__(self, dev_file_path, baudrate=9600, timeout=2.0):
        pass

    def close(self):
        pass

    def flushInput(self):
        pass

    def read(self, bytes_to_read=1):
        result_array = self.bytes_array[self.current_byte_pointer:self.current_byte_pointer + bytes_to_read]
        self.__increment_current_byte_pointer(bytes_to_read)
        return "".join(result_array)

    def __increment_current_byte_pointer(self, bytes_read):
        self.current_byte_pointer = (self.current_byte_pointer + bytes_read) % len(self.bytes_array)
