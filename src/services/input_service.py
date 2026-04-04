from services.motion_service import detect_motion

MOTION_QCF = ["Down", "Down-Forward","Forward"]

def processInput(buffer):
    result = detect_motion(buffer.buffer, MOTION_QCF)

    print("DEBUG buffer: ", buffer.buffer)
    print("DEBUG expected: ", MOTION_QCF)
    print("DEBUG result: ",result)

    if result:
        print("QCF Detected!")

        buffer.buffer.clear()

        return True
    return False