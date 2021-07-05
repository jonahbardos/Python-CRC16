def crc16_generator(data):
    '''
    CRC-16-CCITT Algorithm
    '''
    data = bytearray(data)
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(0, 8):
            
            bcarry = crc & 0x0001
            crc >>= 1

            if bcarry:
                crc ^= 0xa001
    return crc


if __name__ == "__main__":
    x = crc16_generator([0xFF, 0xFE, 0xAC, 0x01, 0xed])
    print(hex(x))
    pass
