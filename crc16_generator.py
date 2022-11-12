def crc16_generator_decimal(data: list[int]) -> int:
    """CRC-16-MODBUS Algorithm

    Parameters
    ----------
    data : list[int]
        Data packets received.

    Returns
    -------
    int
        CRC as an integer.
    """
    data = bytearray(data)
    crc = 0xFFFF
    
    # Calculate CRC-16 checksum for data packet
    for b in data:
        crc ^= b
        for _ in range(0, 8):
            bcarry = crc & 0x0001
            crc >>= 1
            if bcarry:
                crc ^= 0xa001
    
    return crc


def crc16_generator_hex(data: list[int]) -> str:
    """CRC-16-MODBUS Algorithm

    Parameters
    ----------
    data : list[int]
        Data packets received.

    Returns
    -------
    str
        CRC as hex string
    """
    data = bytearray(data)
    crc = 0xFFFF
    
    # Calculate CRC-16 checksum for data packet
    for b in data:
        crc ^= b
        for _ in range(0, 8):
            bcarry = crc & 0x0001
            crc >>= 1
            if bcarry:
                crc ^= 0xa001
    
    return hex(crc)


def crc16_generator(data: list[int]) -> list[int]:
    """CRC-16-MODBUS Algorithm

    Parameters
    ----------
    data : list
        Data packets received.

    Returns
    -------
    list
        Returns CRC flipped
    
    Examples
    --------
    CRC calculated = 0xc0c1
    Returns [0xc1, 0xc0]
    """
    data = bytearray(data)
    crc = 0xFFFF
    
    # Calculate CRC-16 checksum for data packet
    for b in data:
        crc ^= b
        for _ in range(0, 8):
            bcarry = crc & 0x0001
            crc >>= 1
            if bcarry:
                crc ^= 0xa001
    print("Generated CRC", (crc,), (hex(crc),))

    if crc > 255:
        hexstr = hex(crc)
        x, y = int(hexstr[2:4], 16), int(hexstr[4:6], 16)
        arr = [y, x]
        # print("Must send this list to receiever", arr,  hexstr[4:6], hexstr[2:4])
        return arr

    
    arr = [crc]
    print("Must send this list to receiever", arr)
    return arr


def check_crc(data, crc):
    '''
        For validation check:
            - https://crccalc.com
            - Algorithm - CRC-16/MODBUS
    '''
    data = bytearray(data)
    for x in crc:
        data.append(x)
    
    arr = crc16_generator(data)
    if arr[0] == 0:
        print("0 remainder", arr[0])
        return
    print("Invalid CRC")
    print(arr)
    

if __name__ == "__main__":
    data_packet = [0xff, 0xfe]
    
    # Driver Code Decimal
    print(True if crc16_generator_decimal(data_packet) == 49345 else False)
    
    # x = crc16_generator([0xff, 0xfe])
    # check_crc([0xff, 0xfe], x)
