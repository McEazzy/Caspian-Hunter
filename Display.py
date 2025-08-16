import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from Pull import get_skill_occurrences

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

#Our app frame
app = customtkinter.CTk()
app.geometry("900x600")
app.title("Job Scraper")

def graph():
    # Clear the previous widgets if any
    for widget in app.winfo_children():
        if isinstance(widget, customtkinter.CTkEntry) or isinstance(widget, customtkinter.CTkFrame):
            widget.destroy()
    
    x_data = list(get_skill_occurrences().keys())
    y_data = list(get_skill_occurrences().values())

    fig, ax = plt.subplots()
    ax.bar(x_data, y_data)
    ax.set_xlabel("Skills")
    ax.set_ylabel("Occurrences")
    ax.set_title("Job Skill Occurrences")
    fig.set_size_inches(8, 5)
    plt.tight_layout()

    # Create a canvas to embed the matplotlib figure in the tkinter app
    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(pady = 10)

    #Add standard matplotlib navigation toolbar
    toolbar = NavigationToolbar2Tk(canvas, app)
    toolbar.update()
    toolbar.pack(pady=5)

    # Create a search bar to filter skills on the graph
    def filter_skills():
        search_term = search_bar.get().lower()
        filtered_tuples = {k: v for k, v in get_skill_occurrences().items() if search_term in k.lower()}
        ax.clear()
        ax.bar(filtered_tuples.keys(), filtered_tuples.values())
        ax.set_xlabel("Skills")
        ax.set_ylabel("Occurrences")
        ax.set_title("Job Skill Occurrences")
        fig.tight_layout()
        canvas.draw()

    search_bar = customtkinter.CTkEntry(master=app, placeholder_text="Search for a skill")
    search_bar.pack(pady = 5)
    search_bar.bind("<KeyRelease>", lambda event: filter_skills())

# button to graph
my_butt = customtkinter.CTkButton(master = app, text= "Graph job skill occurrence", command = graph)
my_butt.pack(pady = 5)

#Run app
app.mainloop()