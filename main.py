import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk


class ImageLabeller:
    def __init__(self, root):
        self.root = root
        self.root.title("Nepali Number Plate Labeller")
        self.root.geometry("1200x750")

        # Nepali characters that appear on license plates
        self.nepali_chars = [
            # Vowels (स्वर)
            # "अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ", "अं", "अः",

            # Consonants (व्यंजन)
            "क", "ख", "ग", "घ", "ङ",
            "च", "छ", "ज", "झ", "ञ",
            "ट", "ठ", "ड", "ढ", "ण",
            "त", "थ", "द", "ध", "न",
            "प", "फ", "ब", "भ", "म",
            "य", "र", "ल", "व",
            "श", "ष", "स", "ह",
            "क्ष", "त्र", "ज्ञ",

            # Vowel Signs (मात्रा)
            "ा", "ि", "ी", "ु", "ू", "ृ", "े", "ै", "ो", "ौ", "ं", "ः", '', '', 'प्रदेश', '', '',

            # Numbers (अंक)
            "०", "१", "२", "३", "४", "५", "६", "७", "८", "९"
        ]

        # Variables
        self.folder_path = ""
        self.image_files = []
        self.current_image_index = 0
        self.label_folder = "labels"

        # Create main frames
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        # Top frame widgets
        tk.Label(self.top_frame, text="Folder:").grid(
            row=0, column=0, padx=5, pady=5)
        self.folder_path_var = tk.StringVar()
        self.folder_entry = tk.Entry(
            self.top_frame, textvariable=self.folder_path_var, width=50)
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5)

        self.browse_button = tk.Button(
            self.top_frame, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.progress_label = tk.Label(
            self.top_frame, text="0/0 images labeled")
        self.progress_label.grid(row=0, column=3, padx=20, pady=5)

        # Jump to image feature
        tk.Label(self.top_frame, text="Jump to:").grid(
            row=0, column=4, padx=5, pady=5)
        self.jump_var = tk.StringVar()
        self.jump_entry = tk.Entry(
            self.top_frame, textvariable=self.jump_var, width=5)
        self.jump_entry.grid(row=0, column=5, padx=2, pady=5)
        self.jump_button = tk.Button(
            self.top_frame, text="Go", command=self.jump_to_image)
        self.jump_button.grid(row=0, column=6, padx=5, pady=5)

        # Main frame widgets
        # Image display on the left
        self.image_frame = tk.Frame(
            self.main_frame, width=650, height=500, bd=2, relief=tk.SUNKEN)
        self.image_frame.pack(side=tk.LEFT, fill=tk.BOTH,
                              expand=True, padx=5, pady=5)
        self.image_frame.pack_propagate(False)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Label input on the right
        self.label_frame = tk.Frame(self.main_frame, width=450, height=500)
        self.label_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)

        tk.Label(self.label_frame, text="Number Plate Label:",
                 font=("Arial", 12)).pack(anchor=tk.W, padx=5, pady=5)

        self.label_text = tk.Text(
            self.label_frame, width=30, height=4, font=("Arial", 14))
        self.label_text.pack(fill=tk.X, padx=5, pady=5)

        # Virtual Numpad for Devanagari characters
        numpad_frame = tk.Frame(self.label_frame)
        numpad_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)

        tk.Label(numpad_frame, text="Devanagari Character Pad:",
                 font=("Arial", 12)).pack(anchor=tk.W, padx=5, pady=5)

        # Create a frame for the Devanagari characters buttons
        chars_frame = tk.Frame(numpad_frame)
        chars_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create Devanagari character buttons
        row, col = 0, 0
        for char in self.nepali_chars:
            btn = tk.Button(chars_frame, text=char, width=4, height=2,
                            font=("Arial", 12), command=lambda c=char: self.insert_char(c))
            btn.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 8:  # 9 buttons per row
                col = 0
                row += 1

        # Add utility buttons
        utils_frame = tk.Frame(numpad_frame)
        utils_frame.pack(fill=tk.X, padx=5, pady=10)

        self.space_btn = tk.Button(
            utils_frame, text="Space", width=8, command=lambda: self.insert_char(" "))
        self.space_btn.pack(side=tk.LEFT, padx=5)

        self.backspace_btn = tk.Button(
            utils_frame, text="Backspace", width=10, command=self.backspace)
        self.backspace_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(
            utils_frame, text="Clear All", width=8, command=self.clear_text)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.label_frame, text="Save Label", font=("Arial", 12),
                                     command=self.save_label, bg="#4CAF50", fg="white")
        self.save_button.pack(padx=5, pady=10)

        # Bottom frame widgets - Navigation
        self.prev_button = tk.Button(
            self.bottom_frame, text="Previous Image", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.img_counter_var = tk.StringVar(value="Image: 0/0")
        self.img_counter_label = tk.Label(
            self.bottom_frame, textvariable=self.img_counter_var)
        self.img_counter_label.pack(side=tk.LEFT, padx=20, pady=5)

        self.next_button = tk.Button(
            self.bottom_frame, text="Next Image", command=self.next_image)
        self.next_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.status_var = tk.StringVar(value="Status: No folder selected")
        self.status_label = tk.Label(
            self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Keyboard bindings
        self.root.bind("<Left>", lambda event: self.prev_image())
        self.root.bind("<Right>", lambda event: self.next_image())
        self.root.bind("<Control-s>", lambda event: self.save_label())

        # Disable buttons initially
        self.toggle_buttons(False)

    def insert_char(self, char):
        """Insert a character at the cursor position in the text field"""
        self.label_text.insert(tk.INSERT, char)
        self.label_text.focus_set()

    def backspace(self):
        """Delete one character before the cursor"""
        try:
            current_pos = self.label_text.index(tk.INSERT)
            line, char = map(int, current_pos.split('.'))
            if char > 0:
                # Delete the previous character
                self.label_text.delete(f"{line}.{char-1}", f"{line}.{char}")
        except Exception as e:
            print(f"Backspace error: {e}")
        self.label_text.focus_set()

    def clear_text(self):
        """Clear all text in the input field"""
        self.label_text.delete(1.0, tk.END)
        self.label_text.focus_set()

    def toggle_buttons(self, state):
        """Enable or disable navigation and save buttons"""
        state = "normal" if state else "disabled"
        self.prev_button["state"] = state
        self.next_button["state"] = state
        self.save_button["state"] = state
        self.jump_button["state"] = state
        self.jump_entry["state"] = state

    def browse_folder(self):
        """Open folder dialog and load images from selected folder"""
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return

        self.folder_path = folder_path
        self.folder_path_var.set(folder_path)

        # Create labels folder if it doesn't exist
        self.label_folder = os.path.join(self.folder_path, "labels")
        if not os.path.exists(self.label_folder):
            os.makedirs(self.label_folder)

        # Get all image files
        self.image_files = []
        for file in os.listdir(self.folder_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.image_files.append(file)

        self.image_files.sort()  # Sort files alphabetically

        if not self.image_files:
            messagebox.showinfo(
                "Info", "No image files found in the selected folder.")
            self.status_var.set("Status: No images found in folder")
            return

        self.current_image_index = 0
        self.toggle_buttons(True)
        self.load_current_image()
        self.update_progress_counter()
        self.status_var.set(
            f"Status: Loaded {len(self.image_files)} images from {self.folder_path}")

    def load_current_image(self):
        """Load and display the current image and its label if exists"""
        if not self.image_files:
            return

        # Get current image file
        image_file = self.image_files[self.current_image_index]
        image_path = os.path.join(self.folder_path, image_file)

        # Display image
        try:
            img = Image.open(image_path)
            # Resize while maintaining aspect ratio
            img_width, img_height = img.size
            frame_width = self.image_frame.winfo_width() - 10
            frame_height = self.image_frame.winfo_height() - 10

            # Calculate scaling factor
            width_ratio = frame_width / img_width
            height_ratio = frame_height / img_height
            scale_factor = min(width_ratio, height_ratio)

            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)

            img = img.resize((new_width, new_height), Image.LANCZOS)

            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            self.image_label.config(image=None)
            self.image_label.image = None

        # Update image counter
        self.img_counter_var.set(
            f"Image: {self.current_image_index + 1}/{len(self.image_files)}")

        # Load label if exists
        label_file = os.path.splitext(image_file)[0] + ".txt"
        label_path = os.path.join(self.label_folder, label_file)

        # Clear the text widget
        self.label_text.delete(1.0, tk.END)

        if os.path.exists(label_path):
            try:
                with open(label_path, 'r', encoding='utf-8') as f:
                    label_content = f.read()
                self.label_text.insert(tk.END, label_content)
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to load label: {str(e)}")

        self.status_var.set(f"Status: Viewing {image_file}")

    def save_label(self):
        """Save the current label text to a file"""
        if not self.image_files or not self.label_text.get(1.0, tk.END).strip():
            return

        image_file = self.image_files[self.current_image_index]
        label_file = os.path.splitext(image_file)[0] + ".txt"
        label_path = os.path.join(self.label_folder, label_file)

        label_content = self.label_text.get(1.0, tk.END).strip()

        try:
            with open(label_path, 'w', encoding='utf-8') as f:
                f.write(label_content)
            self.status_var.set(f"Status: Label saved for {image_file}")
            self.update_progress_counter()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save label: {str(e)}")

    def next_image(self):
        """Navigate to the next image"""
        if not self.image_files:
            return

        # Save current label first
        self.save_label()

        # Go to next image
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.load_current_image()

    def prev_image(self):
        """Navigate to the previous image"""
        if not self.image_files:
            return

        # Save current label first
        self.save_label()

        # Go to previous image
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_current_image()

    def update_progress_counter(self):
        """Update the progress counter showing how many images are labeled"""
        if not self.image_files:
            self.progress_label.config(text="0/0 images labeled")
            return

        labeled_count = 0
        for img_file in self.image_files:
            label_file = os.path.splitext(img_file)[0] + ".txt"
            label_path = os.path.join(self.label_folder, label_file)
            if os.path.exists(label_path):
                labeled_count += 1

        self.progress_label.config(
            text=f"{labeled_count}/{len(self.image_files)} images labeled")

    def jump_to_image(self):
        """Jump to a specific image number"""
        if not self.image_files:
            return

        try:
            # Get the image number (1-based index)
            image_num = int(self.jump_var.get())

            # Validate the image number
            if 1 <= image_num <= len(self.image_files):
                # Save current label first
                self.save_label()

                # Jump to the specified image (convert to 0-based index)
                self.current_image_index = image_num - 1
                self.load_current_image()
                self.jump_var.set("")  # Clear the entry
            else:
                messagebox.showwarning("Invalid Image Number",
                                       f"Please enter a number between 1 and {len(self.image_files)}")
        except ValueError:
            messagebox.showwarning(
                "Invalid Input", "Please enter a valid number")

        self.jump_entry.focus_set()


def main():
    root = tk.Tk()
    app = ImageLabeller(root)

    # Configure style for a modern look
    style = ttk.Style()
    if 'clam' in style.theme_names():
        style.theme_use('clam')  # Use 'clam' theme for a cleaner look

    root.mainloop()


if __name__ == "__main__":
    main()
