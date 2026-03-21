import time
def measure(func, *args):
    start=time.time()
    result=func(*args)
    end =time.time()
    print(f"Execution Time :{round(end-start,4)}sec")
    return result