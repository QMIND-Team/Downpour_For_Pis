"""Socket helper"""

def mysend(conn, data):
    """Add the header and send data"""
    length = len(data)
    length_in_bytes = length.to_bytes(4, 'big')
    conn.send(length_in_bytes)
    total_sent = 0
    while total_sent < length:
        bytes_sent = conn.send(data[total_sent:])
        total_sent += bytes_sent


def myrecv(conn):
    """Receive, parse header, and receive data"""
    length = int.from_bytes(conn.recv(4), 'big')
    chunks = []
    total_received = 0
    while total_received < length:
        chunk = conn.recv(min(length - total_received, 2048))
        total_received += len(chunk)
        chunks.append(chunk)
    data = b''.join(chunks)
    return data
