import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os


class UnityScriptGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("C Sharp Script Generator")
        self.root.geometry("600x600")  # Increased height to accommodate preview
        self.root.resizable(True, True)

        # Set default save path to desktop
        self.save_path = os.path.join(os.path.expanduser("~"), "Desktop")

        # Configure a centered layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Title
        title_label = ttk.Label(main_frame, text="C Sharp Script Generator", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Form container
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH)

        # Script type section
        ttk.Label(form_frame, text="Type of script", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))
        self.script_type = ttk.Combobox(form_frame, width=40)
        self.script_type['values'] = ('MonoBehaviour', 'ScriptableObject', 'EditorWindow', 'Editor', 'Custom')
        self.script_type.current(0)
        self.script_type.pack(fill=tk.X, pady=(0, 15))

        # Design section
        ttk.Label(form_frame, text="Design", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))

        # Options frame
        options_frame = ttk.Frame(form_frame)
        options_frame.pack(fill=tk.X, pady=(0, 15))

        # Include standard methods
        self.include_std_methods = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Jungle", variable=self.include_std_methods).pack(
            anchor="w")

        # Include regions
        self.include_regions = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Dungeon", variable=self.include_regions).pack(anchor="w")

        # Include serialized fields
        self.include_fields = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Default", variable=self.include_fields).pack(anchor="w")

        # Script name
        name_frame = ttk.Frame(form_frame)
        name_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(name_frame, text="Script Name:").pack(side=tk.LEFT)
        self.script_name = ttk.Entry(name_frame)
        self.script_name.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        self.script_name.insert(0, "NewBehavior")

        # Preview section
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Preview text widget
        self.preview_text = tk.Text(preview_frame, wrap=tk.WORD, height=10)
        self.preview_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Add scrollbar to preview
        scrollbar = ttk.Scrollbar(preview_frame, command=self.preview_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_text.config(yscrollcommand=scrollbar.set)

        # Update preview button
        update_button = ttk.Button(main_frame, text="Update Preview", command=self.update_preview)
        update_button.pack(pady=(0, 10))

        # Generate button
        generate_button = ttk.Button(main_frame, text="Generate", command=self.generate_script)
        generate_button.pack(pady=(0, 10))

        # Initial preview update
        self.update_preview()

        # Bind events to auto-update preview when options change
        self.script_type.bind("<<ComboboxSelected>>", lambda e: self.update_preview())
        self.script_name.bind("<KeyRelease>", lambda e: self.update_preview())

    def update_preview(self):
        self.preview_text.delete(1.0, tk.END)
        script_content = self.generate_script_content()
        self.preview_text.insert(tk.END, script_content)

    def generate_script(self):
        script_name = self.script_name.get()
        if not script_name:
            messagebox.showerror("Error", "Script name cannot be empty.")
            return

        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            initialdir=self.save_path,
            title="Save Unity C# Script",
            defaultextension=".cs",
            initialfile=f"{script_name}.cs",
            filetypes=[("C# Scripts", "*.cs"), ("All Files", "*.*")]
        )

        if not file_path:
            return  # User cancelled

        # Generate script content
        script_content = self.generate_script_content()

        try:
            with open(file_path, 'w') as file:
                file.write(script_content)
            messagebox.showinfo("Success", f"Script generated successfully at:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save script: {str(e)}")

    def generate_script_content(self):
        script_name = self.script_name.get()
        parent = self.script_type.get()

        content = ""

        # Add using statements
        content += "using UnityEngine;\n"
        if parent == "EditorWindow" or parent == "Editor":
            content += "using UnityEditor;\n"
        content += "using System.Collections;\n"
        content += "using System.Collections.Generic;\n\n"

        # Add class declaration
        content += f"public class {script_name} : {parent}\n{{\n"

        # Fields
        if self.include_fields.get():
            if self.include_regions.get():
                content += "    #region Fields\n\n"

            content += "    [SerializeField] private float exampleFloat = 1.0f;\n"
            content += "    [SerializeField] private string exampleString = \"Hello World\";\n"
            content += "    [SerializeField] private GameObject examplePrefab;\n\n"

            if self.include_regions.get():
                content += "    #endregion\n\n"

        # Standard methods
        if self.include_std_methods.get():
            if self.include_regions.get():
                content += "    #region Unity Lifecycle\n\n"

            if parent == "MonoBehaviour":
                content += "    private void Awake()\n    {\n        // Initialize components\n    }\n\n"
                content += "    private void Start()\n    {\n        // Start logic\n    }\n\n"
                content += "    private void Update()\n    {\n        // Update logic\n    }\n\n"
            elif parent == "EditorWindow":
                content += f"    [MenuItem(\"Window/{script_name}\")]\n"
                content += f"    public static void ShowWindow()\n    {{\n"
                content += f"        GetWindow<{script_name}>(\"Window Title\");\n    }}\n\n"
                content += "    private void OnGUI()\n    {\n        // Draw GUI\n    }\n\n"
            elif parent == "ScriptableObject":
                content += "    private void OnEnable()\n    {\n        // Initialize\n    }\n\n"
                content += "    private void OnValidate()\n    {\n        // Validate fields\n    }\n\n"

            if self.include_regions.get():
                content += "    #endregion\n\n"

            # Custom methods region
            if self.include_regions.get():
                content += "    #region Methods\n\n"
                content += "    public void ExampleMethod()\n    {\n        // Method implementation\n    }\n\n"
                content += "    #endregion\n"

        # Close class
        content += "}\n"

        return content


if __name__ == "__main__":
    root = tk.Tk()
    app = UnityScriptGenerator(root)
    root.mainloop()