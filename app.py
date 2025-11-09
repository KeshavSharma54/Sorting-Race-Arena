from flask import Flask, render_template, request, jsonify
import time
import random
import json
import os

app = Flask(__name__)

HISTORY_FILE = "race_history.json"

# --- Sorting Algorithms ---
def bubble_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        for j in range(0, len(a)-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    return a

def selection_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        min_idx = i
        for j in range(i+1, len(a)):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def heap_sort(arr):
    import heapq
    a = arr.copy()
    heapq.heapify(a)
    return [heapq.heappop(a) for _ in range(len(a))]

def shell_sort(arr):
    a = arr.copy()
    gap = len(a) // 2
    while gap > 0:
        for i in range(gap, len(a)):
            temp = a[i]
            j = i
            while j >= gap and a[j-gap] > temp:
                a[j] = a[j-gap]
                j -= gap
            a[j] = temp
        gap //= 2
    return a

# --- Algorithm Dictionary ---
algorithms = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
    "Shell Sort": shell_sort,
}

@app.route('/')
def index():
    return render_template('index.html', algorithms=list(algorithms.keys()))

@app.route('/race', methods=['POST'])
def race():
    data = request.json
    arr = data['array']
    start_times = {}
    results = []

    for name, func in algorithms.items():
        start = time.perf_counter()
        func(arr)
        elapsed = time.perf_counter() - start
        results.append([name, elapsed])

    results.sort(key=lambda x: x[1])

    # Save to history file
    history_entry = {"array": arr, "results": results, "time": time.strftime("%H:%M:%S")}
    if os.path.exists(HISTORY_FILE):
        history = json.load(open(HISTORY_FILE))
    else:
        history = []
    history.insert(0, history_entry)
    json.dump(history[:10], open(HISTORY_FILE, "w"), indent=2)  # keep latest 10

    return jsonify({"results": results})

@app.route('/history')
def history():
    if os.path.exists(HISTORY_FILE):
        history = json.load(open(HISTORY_FILE))
    else:
        history = []
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True)
