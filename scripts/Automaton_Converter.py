import os
import sys

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))  # Get the parent directory

sys.path.append(os.path.join(parent_dir, 'python_package'))  # Add python_packages to sys.path

import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import math
import json
import Automaton_bindings as Automaton # type: ignore

centers = [
    [100, 100], [140, 100], [180, 100], [220, 100], [260, 100], [300, 100],
    [340, 100], [380, 100], [420, 100], [460, 100], [100, 140], [140, 140],
    [180, 140], [220, 140], [260, 140], [300, 140], [340, 140], [380, 140],
    [420, 140], [460, 140], [100, 180], [140, 180], [180, 180], [220, 180],
    [260, 180], [300, 180], [340, 180], [380, 180], [420, 180], [460, 180],
    [100, 220], [140, 220], [180, 220], [220, 220], [260, 220], [300, 220],
    [340, 220], [380, 220], [420, 220], [460, 220], [100, 260], [140, 260],
    [180, 260], [220, 260], [260, 260], [300, 260], [340, 260], [380, 260],
    [420, 260], [460, 260], [100, 300], [140, 300], [180, 300], [220, 300],
    [260, 300], [300, 300], [340, 300], [380, 300], [420, 300], [460, 300],
    [100, 340], [140, 340], [180, 340], [220, 340], [260, 340], [300, 340],
    [340, 340], [380, 340], [420, 340], [460, 340], [100, 380], [140, 380],
    [180, 380], [220, 380], [260, 380], [300, 380], [340, 380], [380, 380],
    [420, 380], [460, 380], [100, 420], [140, 420], [180, 420], [220, 420],
    [260, 420], [300, 420], [340, 420], [380, 420], [420, 420], [460, 420],
    [100, 460], [140, 460], [180, 460], [220, 460], [260, 460], [300, 460],
    [340, 460], [380, 460], [420, 460], [460, 460]
]
 
class NFAEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Automaton Converter")
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

        self.save_button = tk.Button(self.root, text="Save Automaton", command=self.save_nfa)
        self.save_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(self.root, text="Load Automaton", command=self.load_nfa)
        self.load_button.pack(side=tk.LEFT)

        self.convert_button = tk.Button(self.root, text="Convert to DFA", command=self.convert_to_dfa)
        self.convert_button.pack(side=tk.LEFT)

    def add_state(self):
        if self.state_counter >= len(centers):
            print("No more predefined centers available.")
            return

        x, y = centers[self.state_counter]
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
            self.add_transition_button.config(state=tk.NORMAL)  # 允许在选中一个状态时添加转移
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
            self.clear_inner_circle(state_id)
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

    def add_transition(self, transition_char=None):
        if len(self.selected_states) == 1:
            from_state = to_state = self.selected_states[0]
        elif len(self.selected_states) == 2:
            from_state, to_state = self.selected_states
        else:
            return

        if transition_char is None:
            transition_char = simpledialog.askstring("Input", "Enter transition character (leave empty for ε):")
            # deal with cancel 
            if transition_char is None:
                return
            if transition_char == "":
                transition_char = "ε"

        x1, y1 = self.states[from_state][2], self.states[from_state][3]
        x2, y2 = self.states[to_state][2], self.states[to_state][3]

        if from_state == to_state:
            if (from_state, to_state) in self.transitions:
                existing_transition, existing_text, existing_chars = self.transitions[(from_state, to_state)]
                if transition_char in existing_chars:
                    return
                else:
                    new_chars = existing_chars + "+" + transition_char
                    self.canvas.itemconfig(existing_text, text=new_chars)
                    self.transitions[(from_state, to_state)] = (existing_transition, existing_text, new_chars)
            else:
                loop_radius = 30
                loop = self.canvas.create_oval(x1 - loop_radius, y1 - loop_radius, x1 + loop_radius, y1 + loop_radius, outline='black')
                text_x = x1
                text_y = y1 - loop_radius - 10
                transition_text = self.canvas.create_text(text_x, text_y, text=transition_char, fill='green', font=('Helvetica', 12, 'bold'))
                self.transitions[(from_state, to_state)] = (loop, transition_text, transition_char)
        else:
            # Calculate points on the edge of the circles
            angle = math.atan2(y2 - y1, x2 - x1)
            x1_edge = x1 + 20 * math.cos(angle)
            y1_edge = y1 + 20 * math.sin(angle)
            x2_edge = x2 - 20 * math.cos(angle)
            y2_edge = y2 - 20 * math.sin(angle)

            if (from_state, to_state) in self.transitions:
                existing_transition, existing_text, existing_chars = self.transitions[(from_state, to_state)]
                if transition_char in existing_chars:
                    return
                else:
                    new_chars = existing_chars + "+" + transition_char
                    self.canvas.itemconfig(existing_text, text=new_chars)
                    self.transitions[(from_state, to_state)] = (existing_transition, existing_text, new_chars)
            else:
                transition = self.canvas.create_line(x1_edge, y1_edge, x2_edge, y2_edge, arrow=tk.LAST)
                text_x = x2_edge - (x2_edge - x1_edge) / 4
                text_y = y2_edge - (y2_edge - y1_edge) / 4
                transition_text = self.canvas.create_text(text_x, text_y, text=transition_char, fill='green', font=('Helvetica', 12, 'bold'))

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

                if from_state == to_state:
                    # Update the self-loop position
                    loop_radius = 30
                    self.canvas.coords(transition, x1 - loop_radius, y1 - loop_radius, x1 + loop_radius, y1 + loop_radius)
                    text_x = x1
                    text_y = y1 - loop_radius - 10
                    self.canvas.coords(transition_text, text_x, text_y)
                else:
                    # Calculate points on the edge of the circles
                    angle = math.atan2(y2 - y1, x2 - x1)
                    x1_edge = x1 + 20 * math.cos(angle)
                    y1_edge = y1 + 20 * math.sin(angle)
                    x2_edge = x2 - 20 * math.cos(angle)
                    y2_edge = y2 - 20 * math.sin(angle)

                    self.canvas.coords(transition, x1_edge, y1_edge, x2_edge, y2_edge)

                    # Update the position of the transition text to be closer to the end state
                    text_x = x2_edge - (x2_edge - x1_edge) / 4
                    text_y = y2_edge - (y2_edge - y1_edge) / 4
                    self.canvas.coords(transition_text, text_x, text_y)
    
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
            "transitions": []
        }

        for (from_state, to_state), (line, text, chars) in self.transitions.items():
            for char in chars.split('+'):
                nfa["transitions"].append({"from": from_state, "to": to_state, "char": char})

        nfa["start_state"] = self.start_state
        nfa["final_states"] = list(self.final_states)

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
                self.selected_states = [from_state, to_state] if from_state != to_state else [from_state]
                self.add_transition(char)

            self.start_state = nfa["start_state"]
            self.final_states = set(nfa["final_states"])

            if self.start_state:
                self.update_start_state_circle(self.start_state)
            for final_state in self.final_states:
                self.update_final_state_circle(final_state)


    def clear_nfa(self):
        self.clear_inner_circle(self.start_state)
        for final_state in self.final_states:
            self.clear_inner_circle(final_state)
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

    def convert_to_dfa(self):
        if self.start_state is None:
            messagebox.showerror("Error", "No start state selected.")
            return
        
        if self.transitions == {}:  # 没有转移
            messagebox.showerror("Error", "No transitions added.")
            return

        nfa = Automaton.Automaton()
        
        # add transistions
        for (from_state, to_state), (line, text, chars) in self.transitions.items():
            for char in chars.split('+'):
                from_state = int(from_state[1:])
                to_state = int(to_state[1:])
                if char == "ε":
                    char = '\0'
                nfa.addTransition(from_state, to_state, char)

        # add start state
        if self.start_state:
            nfa.setInitialState(int(self.start_state[1:]))
        
        # add final states
        for final_state in self.final_states:
            nfa.addFinalState(int(final_state[1:]))
        
        dfa = nfa.determinize()

        self.clear_nfa()
        self.load_from_dfa(dfa)    

    def load_from_dfa(self, dfa):
        states = dfa.getStates()
        transitions = dfa.getTransitions()

        for state_id in states:
            self.add_state()

        for i in range(len(transitions)):
            src = "q" + str(i)
            for transition in transitions[i]:
                dst = "q" + str(transition.to)
                char = transition.symbol
                self.selected_states = [src, dst] if src != dst else [src]
                self.add_transition(char)

        start_state = dfa.getInitialState()
        start_state = "q" + str(start_state)
        if start_state is not None:
            self.start_state = start_state
            self.update_start_state_circle(start_state)

        final_states = dfa.getFinalStates()
        for final_state in final_states:
            final_state = "q" + str(final_state)
            self.final_states.add(final_state)
            self.update_final_state_circle(final_state)

if __name__ == "__main__":
    root = tk.Tk()
    editor = NFAEditor(root)
    root.mainloop()
