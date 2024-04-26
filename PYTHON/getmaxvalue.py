class Result:
    @staticmethod
    def getMaxValue(arr):
        arr[0] -= 1
        arr.sort()

        for i in range(1, len(arr)):
            if arr[i] > arr[i - 1] + 1:
                arr[i] = arr[i - 1] + 1

        return max(arr)

if __name__ == '__main__':
    import sys

    arr_count = int(input().strip())
    arr = [int(input().strip()) for _ in range(arr_count)]

    result = Result.getMaxValue(arr)

    print(result)
