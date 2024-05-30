import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import math
import json

class NFAEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("NFA Editor")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.state_counter = 0
        self.states = {}
        self.transitions = {}
        self.selected_states = []
        self.start_state = None
        self.final_states = set()
        self.last_selected_color = 'blue'  # 新增属性记录上次选中的颜色

        self.init_buttons()

    def init_buttons(self):
        self.add_state_button = tk.Button(self.root, text="Add State", command=self.add_state)
        self.add_state_button.pack(side=tk.LEFT)

        self.delete_state_button = tk.Button(self.root, text="Delete State", state=tk.DISABLED, command=self.delete_state)
        self.delete_state_button.pack(side=tk.LEFT)

        self.add_transition_button = tk.Button(self.root, text="Add Transition", state=tk.DISABLED, command=self.add_transition)
        self.add_transition_button.pack(side=tk.LEFT)

        self.set_start_button = tk.Button(self.root, text="Set Start", state=tk.DISABLED, command=self.set_start_state)
        self.set_start_button.pack(side=tk.LEFT)

        self.set_final_button = tk.Button(self.root, text="Set Final", state=tk.DISABLED, command=self.set_final_state)
        self.set_final_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.root, text="Save NFA", command=self.save_nfa)
        self.save_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(self.root, text="Load NFA", command=self.load_nfa)
        self.load_button.pack(side=tk.LEFT)

    def add_state(self):
        x, y = 100 , 100 
        state_id = f"q{self.state_counter}"
        self.state_counter += 1

        state_circle = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, outline='black', width=2)
        state_text = self.canvas.create_text(x, y, text=state_id, fill='black')

        self.states[state_id] = (state_circle, state_text, x, y)

        self.canvas.tag_bind(state_circle, '<Button-1>', lambda event, sid=state_id: self.select_state(event, sid))
        self.canvas.tag_bind(state_text, '<Button-1>', lambda event, sid=state_id: self.select_state(event, sid))

        self.canvas.tag_bind(state_circle, '<B1-Motion>', lambda event, sid=state_id: self.move_state(event, sid))
        self.canvas.tag_bind(state_text, '<B1-Motion>', lambda event, sid=state_id: self.move_state(event, sid))

    def select_state(self, event, state_id):
        if state_id in self.selected_states:
            self.canvas.itemconfig(self.states[state_id][0], outline='black')
            self.selected_states.remove(state_id)
        else:
            if len(self.selected_states) == 2:
                # 取消前两个选中的状态
                for sid in self.selected_states:
                    self.canvas.itemconfig(self.states[sid][0], outline='black')
                self.selected_states.clear()

            self.canvas.itemconfig(self.states[state_id][0], outline='red' if len(self.selected_states) == 1 else 'blue')
            self.selected_states.append(state_id)

        if len(self.selected_states) == 1:
            self.delete_state_button.config(state=tk.NORMAL)
            self.add_transition_button.config(state=tk.DISABLED)
            self.set_start_button.config(state=tk.NORMAL)
            self.set_final_button.config(state=tk.NORMAL)
        elif len(self.selected_states) == 2:
            self.delete_state_button.config(state=tk.DISABLED)
            self.add_transition_button.config(state=tk.NORMAL)
            self.set_start_button.config(state=tk.DISABLED)
            self.set_final_button.config(state=tk.DISABLED)
        else:
            self.delete_state_button.config(state=tk.DISABLED)
            self.add_transition_button.config(state=tk.DISABLED)
            self.set_start_button.config(state=tk.DISABLED)
            self.set_final_button.config(state=tk.DISABLED)

    def delete_state(self):
        if len(self.selected_states) == 1:
            state_id = self.selected_states.pop()
            self.canvas.delete(self.states[state_id][0])
            self.canvas.delete(self.states[state_id][1])
            del self.states[state_id]

            if state_id == self.start_state:
                self.start_state = None

            if state_id in self.final_states:
                self.final_states.remove(state_id)

            transitions_to_remove = []
            for (from_state, to_state), (transition, transition_text, char) in self.transitions.items():
                if from_state == state_id or to_state == state_id:
                    self.canvas.delete(transition)
                    self.canvas.delete(transition_text)
                    transitions_to_remove.append((from_state, to_state))

            for key in transitions_to_remove:
                del self.transitions[key]

            self.delete_state_button.config(state=tk.DISABLED)
            self.set_start_button.config(state=tk.DISABLED)
            self.set_final_button.config(state=tk.DISABLED)

    def add_transition(self):
        if len(self.selected_states) == 2:
            from_state, to_state = self.selected_states
            transition_char = simpledialog.askstring("Input", "Enter transition character (leave empty for ε):")
            if transition_char == "":
                transition_char = "ε"

            x1, y1 = self.states[from_state][2], self.states[from_state][3]
            x2, y2 = self.states[to_state][2], self.states[to_state][3]

            # Calculate points on the edge of the circles
            angle = math.atan2(y2 - y1, x2 - x1)
            x1_edge = x1 + 20 * math.cos(angle)
            y1_edge = y1 + 20 * math.sin(angle)
            x2_edge = x2 - 20 * math.cos(angle)
            y2_edge = y2 - 20 * math.sin(angle)

            transition = self.canvas.create_line(x1_edge, y1_edge, x2_edge, y2_edge, arrow=tk.LAST)
            transition_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=transition_char, fill='green', font=('Helvetica', 12, 'bold'))

            self.transitions[(from_state, to_state)] = (transition, transition_text, transition_char)

            self.canvas.itemconfig(self.states[from_state][0], outline='black')
            self.canvas.itemconfig(self.states[to_state][0], outline='black')
            self.selected_states = []

            self.add_transition_button.config(state=tk.DISABLED)
            self.set_start_button.config(state=tk.DISABLED)
            self.set_final_button.config(state=tk.DISABLED)

    def move_state(self, event, state_id):
        x, y = event.x, event.y

        # 删除旧的起始状态或终止状态圆圈
        self.clear_inner_circle(state_id)

        self.canvas.coords(self.states[state_id][0], x - 20, y - 20, x + 20, y + 20)
        self.canvas.coords(self.states[state_id][1], x, y)
        self.states[state_id] = (self.states[state_id][0], self.states[state_id][1], x, y)

        # 更新状态位置后重新绘制起始状态或终止状态圆圈
        if state_id == self.start_state:
            self.update_start_state_circle(state_id)
        if state_id in self.final_states:
            self.update_final_state_circle(state_id)

        for (from_state, to_state), (transition, transition_text, transition_char) in self.transitions.items():
            if from_state == state_id or to_state == state_id:
                x1, y1 = self.states[from_state][2], self.states[from_state][3]
                x2, y2 = self.states[to_state][2], self.states[to_state][3]

                # Calculate points on the edge of the circles
                angle = math.atan2(y2 - y1, x2 - x1)
                x1_edge = x1 + 20 * math.cos(angle)
                y1_edge = y1 + 20 * math.sin(angle)
                x2_edge = x2 - 20 * math.cos(angle)
                y2_edge = y2 - 20 * math.sin(angle)

                self.canvas.coords(transition, x1_edge, y1_edge, x2_edge, y2_edge)
                self.canvas.coords(transition_text, (x1 + x2) / 2, (y1 + y2) / 2)
    
    def clear_inner_circle(self, state_id):
        """Helper function to clear inner circle of a start or final state"""
        if state_id == self.start_state:
            self.canvas.delete(f"start_{state_id}")
        if state_id in self.final_states:
            self.canvas.delete(f"final_{state_id}")

    def set_start_state(self):
        if len(self.selected_states) == 1:
            new_start_state = self.selected_states[0]
            if self.start_state:
                self.update_start_state_circle(self.start_state, clear=True)
            self.start_state = new_start_state
            self.update_start_state_circle(new_start_state)

            self.canvas.itemconfig(self.states[new_start_state][0], outline='black')
            self.selected_states = []

            self.set_start_button.config(state=tk.DISABLED)
            self.set_final_button.config(state=tk.DISABLED)

    def set_final_state(self):
        if len(self.selected_states) == 1:
            final_state = self.selected_states[0]
            if final_state in self.final_states:
                self.update_final_state_circle(final_state, clear=True)
                self.final_states.remove(final_state)
            else:
                self.final_states.add(final_state)
                self.update_final_state_circle(final_state)

            self.canvas.itemconfig(self.states[final_state][0], outline='black')
            self.selected_states = []

            self.set_start_button.config(state=tk.DISABLED)
            self.set_final_button.config(state=tk.DISABLED)

    def update_start_state_circle(self, state_id, clear=False):
        x, y = self.states[state_id][2], self.states[state_id][3]
        if clear:
            self.canvas.delete(f"start_{state_id}")
        else:
            self.canvas.delete(f"start_{state_id}")
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, outline='black', width=2, tags=f"start_{state_id}")

    def update_final_state_circle(self, state_id, clear=False):
        x, y = self.states[state_id][2], self.states[state_id][3]
        if clear:
            self.canvas.delete(f"final_{state_id}")
        else:
            self.canvas.delete(f"final_{state_id}")
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, outline='red', width=2, tags=f"final_{state_id}")

    def save_nfa(self):
        nfa = {
            "states": {state_id: {"x": x, "y": y} for state_id, (circle, text, x, y) in self.states.items()},
            "transitions": [
                {"from": from_state, "to": to_state, "char": char}
                for (from_state, to_state), (line, text, char) in self.transitions.items()
            ],
            "start_state": self.start_state,
            "final_states": list(self.final_states)
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(nfa, f, indent=4)

    def load_nfa(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                nfa = json.load(f)

            self.clear_nfa()

            self.state_counter = 0
            for state_id, pos in nfa["states"].items():
                x, y = pos["x"], pos["y"]
                state_circle = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, outline='black', width=2)
                state_text = self.canvas.create_text(x, y, text=state_id, fill='black')

                self.states[state_id] = (state_circle, state_text, x, y)
                self.state_counter = max(self.state_counter, int(state_id[1:]) + 1)

                self.canvas.tag_bind(state_circle, '<Button-1>', lambda event, sid=state_id: self.select_state(event, sid))
                self.canvas.tag_bind(state_text, '<Button-1>', lambda event, sid=state_id: self.select_state(event, sid))

                self.canvas.tag_bind(state_circle, '<B1-Motion>', lambda event, sid=state_id: self.move_state(event, sid))
                self.canvas.tag_bind(state_text, '<B1-Motion>', lambda event, sid=state_id: self.move_state(event, sid))

            for transition in nfa["transitions"]:
                from_state, to_state, char = transition["from"], transition["to"], transition["char"]
                x1, y1 = self.states[from_state][2], self.states[from_state][3]
                x2, y2 = self.states[to_state][2], self.states[to_state][3]

                # Calculate points on the edge of the circles
                angle = math.atan2(y2 - y1, x2 - x1)
                x1_edge = x1 + 20 * math.cos(angle)
                y1_edge = y1 + 20 * math.sin(angle)
                x2_edge = x2 - 20 * math.cos(angle)
                y2_edge = y2 - 20 * math.sin(angle)

                transition_line = self.canvas.create_line(x1_edge, y1_edge, x2_edge, y2_edge, arrow=tk.LAST)
                transition_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=char, fill='green', font=('Helvetica', 12, 'bold'))

                self.transitions[(from_state, to_state)] = (transition_line, transition_text, char)

            self.start_state = nfa["start_state"]
            self.final_states = set(nfa["final_states"])

            if self.start_state:
                self.update_start_state_circle(self.start_state)
            for final_state in self.final_states:
                self.update_final_state_circle(final_state)

    def clear_nfa(self):
        for state_id, (circle, text, x, y) in self.states.items():
            self.canvas.delete(circle)
            self.canvas.delete(text)
        for (from_state, to_state), (line, text, char) in self.transitions.items():
            self.canvas.delete(line)
            self.canvas.delete(text)
        self.states.clear()
        self.transitions.clear()
        self.state_counter = 0
        self.selected_states.clear()
        self.start_state = None
        self.final_states.clear()

if __name__ == "__main__":
    root = tk.Tk()
    editor = NFAEditor(root)
    root.mainloop()
