from multiprocessing import Pool, cpu_count
from time import time


def factorize(*number):
    result = []
    for i in range(len(number)):
        result.append([])
        for n in range(number[i]):
            if number[i] % (n + 1) == 0:
                result[i].append(n + 1)
    return result


def callback(result):
    a, b, c, d = result[0][0], result[1][0], result[2][0], result[3][0]
    print(a == [1, 2, 4, 8, 16, 32, 64, 128], end=', ')
    print(b == [1, 3, 5, 15, 17, 51, 85, 255], end=', ')
    print(c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999], end=', ')
    print(d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060])
    # assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    # assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    # assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    # assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
    #              380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


if __name__ == '__main__':
    print("A normal test.")
    timer = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print(f'Time spent is: {round(time() - timer, 4)} second.')

    cpu = cpu_count()
    print(f'Your computer has: {cpu} CPU')
    for n in range(1, cpu + 1):
        print(f"Test spead CPU: {n}.")
        start_time = time()
        with Pool(processes=n) as pool:
            pool.map_async(factorize, [128, 255, 99999, 10651060], callback=callback)
            pool.close()
            pool.join()
        print(f'Time spent is: {round(time() - start_time, 4)} second.')
