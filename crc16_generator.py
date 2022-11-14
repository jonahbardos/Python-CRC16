def crc16_generator_decimal(data: list[int]) -> int:
    """CRC-16-MODBUS Decimal Algorithm

    Parameters
    ----------
    data : list[int]
        Data packets received.

    Returns
    -------
    int
        CRC as an integer.
        
    Raises
    ----------
    ValueError
        If data packet in each index contains a byte > 256
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
    """CRC-16-MODBUS Hex Algorithm

    Parameters
    ----------
    data : list[int]
        Data packets received.

    Returns
    -------
    str
        CRC as hex string
    
    Raises
    ----------
    ValueError
        If data packet in each index contains a byte > 256
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


def crc16_generator_to_send(data: list[int], debug=False) -> list[int]:
    """CRC-16-MODBUS Algorithm to send to receiver.

    Parameters
    ----------
    data : list[int]
        Data packet to create a checksum.
    debug : bool, optional
        Prints out generated CRC, by default False

    Returns
    -------
    list[int]
        Returns generated CRC into hex format flipped.
    
    Raises
    ----------
    ValueError
        If data packet in each index contains a byte > 256
    """
    crc_to_send = list()
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
    
    if crc > 0xff:
        msb = crc >> 0x08 & 0xff
        lsb = crc & 0xff
        crc_to_send = [lsb, msb]
    else:
        crc_to_send = [crc]

    if debug:
        print(f'Generated CRC: {crc}')
        print(f'Converted CRC to hex: {hex(crc)}')
        print(f'CRC to send to receiver: {crc_to_send}')

    return crc_to_send


def crc16_verify(data_packet: list[int], debug=False) -> bool:
    """https://crccalc.com
       Algorithm - CRC-16/MODBUS

    Parameters
    ----------
    data_packet : list[int]
        Data packet with CRC to verify.

    Returns
    -------
    bool
        True if CRC checksum no errors found, else False
    """
    data = bytearray(data_packet)
    remainder = crc16_generator_to_send(data)
    if debug:
        print(f'Data packet: {data_packet} -> Remainder: {remainder}')
    return (True if sum(remainder) == 0 else False)
    

if __name__ == "__main__":
    data_packet = [0xff, 0xfe]
    bad_data_packet = [0xff]
    
    # Driver Code Decimal
    print(True if crc16_generator_decimal(data_packet) == 49345 else False)
    
    # Drive code Hex
    print(True if crc16_generator_hex(data_packet) == '0xc0c1' else False)
    
    # Verify CRC is correct
    data_packet.extend(crc16_generator_to_send(data_packet))
    print(True if crc16_verify(data_packet) == True else False)
    
    bad_data_packet.extend(crc16_generator_to_send(bad_data_packet) + [0xff])
    print(True if crc16_verify(bad_data_packet, debug=True) == True else False)
