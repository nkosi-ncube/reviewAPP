import os
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from slack_sdk import WebClient
from slack_sdk.webhook import WebhookClient
from slack_sdk.errors import SlackApiError
import glob

# Set the color scheme
#bg_color = "#ADD8E6" # light blue
bg_color = "#0018a8" # dark blue
fg_color = "#fff"
button_color = "#87CEFA" # sky blue
button_hover_color = "#B0E0E6" # powder blue
button_active_color = "#00BFFF" # deep sky blue

# Set the font style
font_style = ("Arial", 12)

# Set the radius of the rounded buttons
button_radius = 10

# Set the folder path
folder_path = "/home/wtc/Desktop/"
text_files = glob.glob(folder_path + "/*.txt")

# Set the Slack API token
slack_token = "xoxb-123456789012-123456789012-abcdefghijklmn1234567890"

def send_slack_message():
    web_client = WebClient(token=slack_token)
    username = "Your Slack Username"
    channel_name = "CHANNEL_NAME" # Replace with the name of the channel you want to send the file to
    file_path = file_path_entry.get()

    # Upload the file to Slack
    try:
        # Get the user ID and channel ID from the username and channel name
        user_id = web_client.users_lookupByEmail(email=username)["user"]["id"]
        channel_id = web_client.conversations_list(types="public_channel,private_channel")["channels"][0]["id"]
        for channel in web_client.conversations_list(types="public_channel,private_channel")["channels"]:
            if channel["name"] == channel_name:
                channel_id = channel["id"]
                break

        # Upload the file to Slack
        with open(file_path, "rb") as file:
            response = web_client.files_upload(
                channels=channel_id,
                file=file,
                initial_comment="Here is the text file you requested."
            )
        print(response)
    except SlackApiError as e:
        print("Error uploading file: {}".format(e))

def create_text_file(email, iteration, project, comments, file_path):
    file_name = f"{project.replace('-', '_')}.txt"
    full_path = file_path + "/" + file_name
    file_content = f"<{email}>\n\n<<iteration_{iteration}>>\n\n<<{project}>>\n\n"

    for comment in comments:
        file_content += f"\t● <<{comment}>>\n\n\n"

    with open(full_path, "w") as file:
        file.write(file_content)

    messagebox.showinfo("File Created", f"Text file '{file_name}' created successfully at {file_path}.")

def validate_inputs(email, iteration, project, comments, file_path):
    if not email or not iteration or not project or len(comments) < 3 or not file_path:
        messagebox.showwarning("Incomplete Fields", "Please fill in all fields and provide at least 3 comments. Select a file path.")
        return False
    return True

def get_comments():
    return comment_listbox.get(0, tk.END)

def add_comment():
    comment = simpledialog.askstring("Add Comment", "Enter a comment:")
    if comment:
        comment_listbox.insert(tk.END, comment)

def browse_file_path():
    file_path = filedialog.askdirectory()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def on_create_button_click():
    email = email_entry.get()
    iteration = iteration_entry.get()
    project = project_entry.get().replace(' ', '-')
    comments = get_comments()
    file_path = file_path_entry.get()

    if validate_inputs(email, iteration, project, comments, file_path):
        create_text_file(email, iteration, project, comments, file_path)

# Create main window
root = tk.Tk()
root.title("Wethinkcode Group 12 Text File Creator")
root.geometry('450x700')
# Set the background color
root.configure(bg=bg_color)

# Create labels and entry widgets
tk.Label(root, text="Email:", fg=fg_color, bg=bg_color, font=font_style).grid(row=0, column=0, sticky="w", padx=5, pady=5)
email_entry = tk.Entry(root, bg='white')
email_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Iteration Number:", fg=fg_color, bg=bg_color, font=font_style).grid(row=1, column=0, sticky="w", padx=5, pady=5)
iteration_entry = tk.Entry(root, bg='white')
iteration_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Project Name:", fg=fg_color, bg=bg_color, font=font_style).grid(row=2, column=0, sticky="w", padx=5, pady=5)
project_entry = tk.Entry(root, bg='white')
project_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="File Path:", fg=fg_color, bg=bg_color, font=font_style).grid(row=3, column=0, sticky="w", padx=5, pady=5)
file_path_entry = tk.Entry(root, bg='white')
file_path_entry.grid(row=3, column=1, padx=5, pady=5)

# Browse button for file path
browse_button = tk.Button(root, text="Browse", command=browse_file_path, bg=button_color, fg=fg_color, font=font_style, relief=tk.FLAT, activebackground=button_active_color, activeforeground=fg_color)
browse_button.grid(row=3, column=2, pady=5)

tk.Label(root, text="Comments (type 'quit' to finish):", fg=fg_color, bg=bg_color, font=font_style).grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=5)

# Comment Listbox
comment_listbox = tk.Listbox(root, selectmode=tk.SINGLE, bg='white')
comment_listbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Add Comment button
add_comment_button = tk.Button(root, text="Add Comment", command=add_comment, bg=button_color, fg=fg_color, font=font_style, relief=tk.FLAT, activebackground=button_active_color, activeforeground=fg_color)
add_comment_button.grid(row=6, column=0, columnspan=2, pady=10)

# Create the "Create" button
create_button = tk.Button(root, text="Create Text File", command=on_create_button_click, bg=button_color, fg=fg_color, font=font_style, relief=tk.FLAT, activebackground=button_active_color, activeforeground=fg_color, borderwidth=0, highlightthickness=0, padx=20, pady=10, bd=0, cursor="hand2")
create_button.config(highlightbackground=button_color, highlightcolor=button_color, highlightthickness=button_radius)
create_button.grid(row=7, column=0, columnspan=2, pady=10)

#Create the "Send Slack Message" button
send_slack_button = tk.Button(root, text="Send Slack Message", command=send_slack_message, bg=button_color, fg=fg_color, font=font_style, relief=tk.FLAT, activebackground=button_active_color, activeforeground=fg_color, borderwidth=0, highlightthickness=0, padx=20, pady=10, bd=0, cursor="hand2")
send_slack_button.config(borderwidth=0, highlightthickness=0,  highlightbackground=button_color, highlightcolor=button_color)
send_slack_button.grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()