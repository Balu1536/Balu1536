import tkinter as tk
from tkinter import messagebox
from collections import deque   # For managing processes in Round Robin
import heapq  
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

# Placeholder functions for scheduling algorithms
def fcfs(processes):
    # Sort processes by their arrival time
    processes.sort(key=lambda p: p.arrival_time)
    
    current_time = 0  # Initialize the current time (starts at 0)
    
    for process in processes:
        # If the process arrives after the current time, the CPU waits until it arrives
        if process.arrival_time > current_time:
            current_time = process.arrival_time
        
        # Completion time is the current time + the burst time
        process.completion_time = current_time + process.burst_time
        
        # Turnaround time is the completion time minus the arrival time
        process.turn_around_time = process.completion_time - process.arrival_time
        
        # Waiting time is the turnaround time minus the burst time
        process.waiting_time = process.turn_around_time - process.burst_time
        
        # Update the current time after the process has completed
        current_time = process.completion_time
 # Implement FCFS algorithm

def sjf(processes):
    # Sort processes first by arrival time, then by burst time
    processes.sort(key=lambda p: (p.arrival_time, p.burst_time))
    
    current_time = 0  # Keep track of the current time
    for process in processes:
        # If the process arrives after the current time, CPU waits until it arrives
        if process.arrival_time > current_time:
            current_time = process.arrival_time
        
        # Completion time is the current time + burst time
        process.completion_time = current_time + process.burst_time
        
        # Turnaround time is the completion time - arrival time
        process.turn_around_time = process.completion_time - process.arrival_time
        
        # Waiting time is the turnaround time - burst time
        process.waiting_time = process.turn_around_time - process.burst_time
        
        # Update the current time after the process has finished
        current_time = process.completion_time


def round_robin(processes, time_quantum):
    queue = deque(processes)
    current_time = 0
    
    while queue:
        process = queue.popleft()
        
        # If the process arrives after the current time, wait until it arrives
        if process.arrival_time > current_time:
            current_time = process.arrival_time
        
        if process.remaining_time > time_quantum:
            current_time += time_quantum
            process.remaining_time -= time_quantum
            queue.append(process)  # Requeue the process
        else:
            current_time += process.remaining_time
            process.completion_time = current_time
            process.remaining_time = 0  # Process finishes
        
        # Turnaround and Waiting Time Calculations
        process.turn_around_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turn_around_time - process.burst_time


def non_preemptive_priority(processes):
    # Sort processes by priority, and in case of tie, by arrival time
    processes.sort(key=lambda p: (p.priority, p.arrival_time))
    
    current_time = 0
    for process in processes:
        if process.arrival_time > current_time:
            current_time = process.arrival_time
        
        process.completion_time = current_time + process.burst_time
        process.turn_around_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turn_around_time - process.burst_time
        current_time = process.completion_time

def preemptive_priority(processes):
    # Priority queue (min-heap), sorted by priority first, and arrival time second
    pq = []
    current_time = 0
    remaining_processes = len(processes)
    
    while remaining_processes > 0:
        # Add all processes that have arrived to the priority queue
        for process in processes:
            if process.arrival_time <= current_time and process.remaining_time > 0 and process not in pq:
                heapq.heappush(pq, (process.priority, process.arrival_time, process))
        
        if pq:
            # Get the process with the highest priority (lowest priority number)
            priority, arrival_time, process = heapq.heappop(pq)
            
            # Process execution
            if process.remaining_time > 0:
                time_slice = min(process.remaining_time, 1)  # Execute for 1 unit of time (time quantum = 1)
                current_time += time_slice
                process.remaining_time -= time_slice
                
                # If the process is finished, update its completion time
                if process.remaining_time == 0:
                    process.completion_time = current_time
                    process.turn_around_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turn_around_time - process.burst_time
                    remaining_processes -= 1  # One less process left to execute
        else:
            current_time += 1  # CPU idle for 1 unit if no processes are ready

def srtf(processes):
    # Sort processes based on arrival time
    processes.sort(key=lambda p: p.arrival_time)
    
    current_time = 0
    remaining_processes = len(processes)
    processes_heap = []
    
    while remaining_processes > 0:
        # Add all processes that have arrived up to the current time
        for process in processes:
            if process.arrival_time <= current_time and process.remaining_time > 0:
                heapq.heappush(processes_heap, (process.remaining_time, process.arrival_time, process))
        
        if processes_heap:
            # Get the process with the shortest remaining time
            remaining_time, arrival_time, process = heapq.heappop(processes_heap)
            
            # Execute the process for 1 unit of time
            time_slice = 1
            current_time += time_slice
            process.remaining_time -= time_slice
            
            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turn_around_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turn_around_time - process.burst_time
                remaining_processes -= 1
        else:
            current_time += 1  # CPU idle


class SchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Process Scheduling in Python")
        self.num_processes = 0
        self.processes = []  # Correct initialization for processes
        self.create_widgets()

    def create_widgets(self):
        self.instruction_label = tk.Label(self.root, text="Enter the number of processes and their details.")
        self.instruction_label.grid(row=0, columnspan=2, pady=10)

        self.num_process_label = tk.Label(self.root, text="Number of Processes:")
        self.num_process_label.grid(row=1, column=0, padx=10, pady=5)
        self.num_process_entry = tk.Entry(self.root)
        self.num_process_entry.grid(row=1, column=1, padx=10, pady=5)

        self.process_entries_frame = tk.Frame(self.root)
        self.process_entries_frame.grid(row=2, columnspan=2, pady=10)

        self.add_process_button = tk.Button(self.root, text="Add Process", command=self.add_process_entry)
        self.add_process_button.grid(row=3, columnspan=2, pady=5)

        self.algorithm_label = tk.Label(self.root, text="Select Scheduling Algorithm:")
        self.algorithm_label.grid(row=4, column=0, padx=10, pady=5)

        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("FCFS")  # default
        self.algorithm_menu = tk.OptionMenu(self.root, self.algorithm_var, "FCFS", "SJF", "Round Robin", "Non-Preemptive Priority", "Preemptive Priority", "SRTF")
        self.algorithm_menu.grid(row=4, column=1, padx=10, pady=5)

        self.start_button = tk.Button(self.root, text="Start Scheduling", command=self.start_scheduling)
        self.start_button.grid(row=5, columnspan=2, pady=20)

        self.output_text = tk.Text(self.root, height=10, width=50)
        self.output_text.grid(row=6, columnspan=2, padx=10, pady=10)

    def add_process_entry(self):
        num = int(self.num_process_entry.get())
        if self.num_processes < num:
            self.process_entries_frame.destroy()
            self.process_entries_frame = tk.Frame(self.root)
            self.process_entries_frame.grid(row=2, columnspan=2, pady=10)

            self.processes = []  # Reset process list on new input
            for i in range(num):
                process_label = tk.Label(self.process_entries_frame, text=f"Process {i+1}:")
                process_label.grid(row=i, column=0, padx=5, pady=5)

                name_entry = tk.Entry(self.process_entries_frame)
                name_entry.grid(row=i, column=1, padx=5, pady=5)
                arrival_time_entry = tk.Entry(self.process_entries_frame)
                arrival_time_entry.grid(row=i, column=2, padx=5, pady=5)
                burst_time_entry = tk.Entry(self.process_entries_frame)
                burst_time_entry.grid(row=i, column=3, padx=5, pady=5)
                priority_entry = tk.Entry(self.process_entries_frame)
                priority_entry.grid(row=i, column=4, padx=5, pady=5)

                self.processes.append({
                    'name': name_entry,
                    'arrival_time': arrival_time_entry,
                    'burst_time': burst_time_entry,
                    'priority': priority_entry
                })
            self.num_processes = num

    def start_scheduling(self):
        self.output_text.delete(1.0, tk.END)
        try:
            self.processes_data = []  # Initialize this list for storing Process objects

            for process in self.processes:
                name = process['name'].get()
                arrival_time = process['arrival_time'].get()
                burst_time = process['burst_time'].get()
                priority = process['priority'].get()

                if name and arrival_time and burst_time and priority:
                    self.processes_data.append(Process(name, arrival_time, burst_time, priority))
                else:
                    messagebox.showerror("Input Error", "Please fill in all fields for each process.")
                    return

            algorithm = self.algorithm_var.get()

            if algorithm == "FCFS":
                fcfs(self.processes_data)
            elif algorithm == "SJF":
                sjf(self.processes_data)
            elif algorithm == "Round Robin":
                time_quantum = 4  # Can be set dynamically too
                round_robin(self.processes_data, time_quantum)
            elif algorithm == "Non-Preemptive Priority":
                non_preemptive_priority(self.processes_data)
            elif algorithm == "Preemptive Priority":
                preemptive_priority(self.processes_data)
            elif algorithm == "SRTF":
                srtf(self.processes_data)

            # Display the result (you can format this better)
            self.output_text.insert(tk.END, "Scheduling Results:\n")
            for p in self.processes_data:
                self.output_text.insert(tk.END, f"{p.name} - Completion Time: {p.completion_time}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulingApp(root)
    root.mainloop()
