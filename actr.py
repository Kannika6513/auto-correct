import customtkinter as ctk
from tkinter import filedialog, messagebox
import language_tool_python

#  SETTINGS 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

#  APP WINDOW 
root = ctk.CTk()
root.title("⚡ AI Autocorrect ")
root.geometry("900x650")

#  TOOL INIT
tool = language_tool_python.LanguageTool('en-US')

#  GLOBALS 
last_text = ""   # for undo feature
live_autocorrect = False  # toggle

#  FUNCTIONS 
def correct_text():
    global last_text
    text = input_box.get("1.0", "end-1c")
    if not text.strip():
        messagebox.showwarning("Warning", "Please enter some text first!")
        return
    last_text = text  # store for undo
    matches = tool.check(text)
    corrected = language_tool_python.utils.correct(text, matches)
    output_box.delete("1.0", "end")
    output_box.insert("1.0", corrected)
    update_status(text, matches)

def show_suggestions():
    text = input_box.get("1.0", "end-1c")
    matches = tool.check(text)
    if not matches:
        messagebox.showinfo("Suggestions", "✅ No mistakes found!")
        return
    sug_text = ""
    for m in matches[:10]:  # show only first 10
        sug_text += f"- {m.context}\n👉 Suggestion: {m.replacements}\n\n"
    messagebox.showinfo("Suggestions", sug_text)

def clear_text():
    input_box.delete("1.0", "end")
    output_box.delete("1.0", "end")
    status_label.configure(text="")

def insert_example():
    example_text = "This is a simple example with a few mistake to corect."
    input_box.insert("end", example_text)

def save_output():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output_box.get("1.0", "end-1c"))
        messagebox.showinfo("Saved", "Output saved successfully!")

def undo_correction():
    if last_text:
        output_box.delete("1.0", "end")
        output_box.insert("1.0", last_text)
    else:
        messagebox.showinfo("Undo", "No previous correction found!")

def toggle_live():
    global live_autocorrect
    live_autocorrect = not live_autocorrect
    status = "ON" if live_autocorrect else "OFF"
    messagebox.showinfo("Live Autocorrect", f"Live autocorrect is now {status}")

def on_type(event=None):
    if live_autocorrect:
        text = input_box.get("1.0", "end-1c")
        matches = tool.check(text)
        corrected = language_tool_python.utils.correct(text, matches)
        output_box.delete("1.0", "end")
        output_box.insert("1.0", corrected)
        update_status(text, matches)

def update_status(text, matches):
    words = len(text.split())
    mistakes = len(matches)
    status_label.configure(text=f"Words: {words} | Mistakes found: {mistakes}")

#  UI 
title_label = ctk.CTkLabel(root, text="⚡ AI Autocorrect",
                           font=("Arial Rounded MT Bold", 28, "bold"),
                           text_color="#E0B3FF")
title_label.pack(pady=20)

main_frame = ctk.CTkFrame(root, fg_color="#2B0B3A", corner_radius=20)
main_frame.pack(padx=20, pady=10, fill="both", expand=True)

# Input Box
input_label = ctk.CTkLabel(main_frame, text="✏ Input Text", font=("Arial", 16, "bold"))
input_label.pack(pady=(15, 5))
input_box = ctk.CTkTextbox(main_frame, height=120, width=700, corner_radius=15,
                           fg_color="#1E1E2F", text_color="white", font=("Consolas", 14))
input_box.pack(pady=5)
input_box.bind("<KeyRelease>", on_type)  # live autocorrect

# Buttons
btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame, text="✅ Correct", command=correct_text,
              fg_color="#9C27B0", hover_color="#BA68C8", corner_radius=12).grid(row=0, column=0, padx=10)
ctk.CTkButton(btn_frame, text="💡 Suggestions", command=show_suggestions,
              fg_color="#FF9800", hover_color="#FFB74D", corner_radius=12).grid(row=0, column=1, padx=10)
ctk.CTkButton(btn_frame, text="↩ Undo", command=undo_correction,
              fg_color="#607D8B", hover_color="#78909C", corner_radius=12).grid(row=0, column=2, padx=10)
ctk.CTkButton(btn_frame, text="🧹 Clear", command=clear_text,
              fg_color="#FF4081", hover_color="#F06292", corner_radius=12).grid(row=0, column=3, padx=10)
ctk.CTkButton(btn_frame, text="📄 Insert Example", command=insert_example,
              fg_color="#03A9F4", hover_color="#4FC3F7", corner_radius=12).grid(row=0, column=4, padx=10)
ctk.CTkButton(btn_frame, text="💾 Save Output", command=save_output,
              fg_color="#4CAF50", hover_color="#66BB6A", corner_radius=12).grid(row=0, column=5, padx=10)
ctk.CTkButton(btn_frame, text="⚡ Toggle Live", command=toggle_live,
              fg_color="#673AB7", hover_color="#9575CD", corner_radius=12).grid(row=0, column=6, padx=10)

# Output Box
output_label = ctk.CTkLabel(main_frame, text="📜 Corrected Output", font=("Arial", 16, "bold"))
output_label.pack(pady=(15, 5))
output_box = ctk.CTkTextbox(main_frame, height=120, width=700, corner_radius=15,
                            fg_color="#1E1E2F", text_color="#A5FFAF", font=("Consolas", 14))
output_box.pack(pady=5)

# Status Bar
status_label = ctk.CTkLabel(root, text="", font=("Arial", 14), text_color="#E0B3FF")
status_label.pack(pady=5)

#  RUN 
root.mainloop()
