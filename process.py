import tkinter as tk
from tkinter import messagebox

class Process:
    def __init__(self, name, arrival_time, burst_time, priority):
        self.name = name
        self.arrival_time = int(arrival_time)
        self.burst_time = int(burst_time)
        self.priority = int(priority)
        self.completion_time = 0
        self.turn_around_time = 0
        self.waiting_time = 0
        self.response_time = 0
        self.remaining_time = int(burst_time)

def fcfs(processes):
    current_time = 0
    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        current_time += process.burst_time
        process.completion_time = current_time
        process.turn_around_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turn_around_time - process.burst_time

def sjf(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    current_time = 0
    while processes:
        available_processes = [p for p in processes if p.arrival_time <= current_time]
        if not available_processes:
            current_time += 1
            continue
        next_process = min(available_processes, key=lambda x: x.burst_time)
        processes.remove(next_process)
        current_time += next_process.burst_time
        next_process.completion_time = current_time
        next_process.turn_around_time = next_process.completion_time - next_process.arrival_time
        next_process.waiting_time = next_process.turn_around_time - next_process.burst_time

def round_robin(processes, time_quantum):
    queue = processes.copy()
    current_time = 0
    while queue:
        process = queue.pop(0)
        if process.remaining_time > time_quantum:
            current_time += time_quantum
            process.remaining_time -= time_quantum
            queue.append(process)
        else:
            current_time += process.remaining_time
            process.completion_time = current_time
            process.turn_around_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turn_around_time - process.burst_time
            process.remaining_time = 0

def non_preemptive_priority(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.priority))
    current_time = 0
    while processes:
        available_processes = [p for p in processes if p.arrival_time <= current_time]
        if not available_processes:
            current_time += 1
            continue
        next_process = min(available_processes, key=lambda x: x.priority)
        processes.remove(next_process)
        current_time += next_process.burst_time
        next_process.completion_time = current_time
        next_process.turn_around_time = next_process.completion_time - next_process.arrival_time
        next_process.waiting_time = next_process.turn_around_time - next_process.burst_time

def preemptive_priority(processes):
    current_time = 0
    while processes:
        available_processes = [p for p in processes if p.arrival_time <= current_time]
        if not available_processes:
            current_time += 1
            continue
        
        next_process = min(available_processes, key=lambda x: x.priority)
        next_process.remaining_time -= 1
        if next_process.remaining_time == 0:
            processes.remove(next_process)
            next_process.completion_time = current_time + 1
            next_process.turn_around_time = next_process.completion_time - next_process.arrival_time
            next_process.waiting_time = next_process.turn_around_time - next_process.burst_time
        current_time += 1

def srtf(processes):
    current_time = 0
    while processes:
        available_processes = [p for p in processes if p.arrival_time <= current_time]
        if not available_processes:
            current_time += 1
            continue
        
        next_process = min(available_processes, key=lambda x: x.remaining_time)
        next_process.remaining_time -= 1
        if next_process.remaining_time == 0:
            processes.remove(next_process)
            next_process.completion_time = current_time + 1
            next_process.turn_around_time = next_process.completion