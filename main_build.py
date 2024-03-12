import customtkinter as ctk
import tkinter as tk
import math
from tkinter import messagebox

from utilities.db_services import connect_to_db
from utilities.builder_data import classes,timings
from utilities.utils import load_data_from_PDF,make_pdf,make_id
from codescripts.timetable_tools import accumulate_cells,validation_algorithm,generate_timetable

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")

class MyWidget(tk.Frame):
    def __init__(self, pos,subject,teacher,room, master=None):
        super().__init__(master, background="white")
        self.label1 = ctk.CTkLabel(master, text=subject, fg_color="#4bcffa", text_color="black", padx=10, pady=5,
                                   corner_radius=8, font=("Britannic Bold", 12))  # Subject Name
        self.label2 = ctk.CTkLabel(master, text=teacher, fg_color="#B9E9FC", text_color="black", padx=10, pady=5,
                                   corner_radius=8, font=("Britannic Bold", 12))  # Teacher Name
        self.label3 = ctk.CTkLabel(master, text=room, fg_color="#95BDFF", text_color="black", padx=10, pady=5,
                                   corner_radius=8, font=("Britannic Bold", 12))  # Room Number
        self.postn = pos
        self.label1.grid(row=pos[0] + 0, column=pos[1] + 0)
        self.label2.grid(row=pos[0] + 1, column=pos[1] + 0)
        self.label3.grid(row=pos[0] + 2, column=pos[1] + 0)

    def clear(self):
        self.label1.grid_forget()
        self.label2.grid_forget()
        self.label3.grid_forget()
        self.grid_forget()


    def setdrop(self, ttobj, master=None):
        self.label1.bind("<Button-1>", ttobj.on_cell_click)
        self.label2.bind("<Button-1>", ttobj.on_cell_click)
        self.label3.bind("<Button-1>", ttobj.on_cell_click)

    def myconfigure(self, value, coord):
        if coord[0] == self.postn[0] + 0 and coord[1] == self.postn[1] + 0:
            self.label1.configure(text=value)
        if coord[0] == self.postn[0] + 1 and coord[1] == self.postn[1] + 0:
            self.label2.configure(text=value)
        if coord[0] == self.postn[0] + 2 and coord[1] == self.postn[1] + 0:
            self.label3.configure(text=value)

    def getTeacherName(self):
        return self.label2._text

    def getRoomNumber(self):
        return self.label3._text

    def getSubject(self):
        return self.label1._text
    
    def showErrorCell(self):
        self.config(bg="red")

    def resetColor(self):
        self.config(bg="white")


class TimetableApp():
    def __init__(self, master): 
        self.master = master
        
        # Create a Canvas widget and a Frame widget to hold your app
        self.canvas = tk.Canvas(master)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        
        xscrollbar = tk.Scrollbar(self.master, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=xscrollbar.set)
        xscrollbar.grid(row=1, column=0, sticky='ew')

        # Create a vertical scrollbar and associate it with the canvas
        yscrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.grid(row=0, column=1, sticky='ns')

        self.app_frame = tk.Frame(self.canvas)
        
        self.canvas.create_window((0,0), window=self.app_frame, anchor='nw')
        self.app_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.app_frame.bind('<MouseWheel>', self._on_mousewheel)
        self.app_frame.bind('<Configure>', lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        from utilities.builder_data import pdf_path 
        tup=load_data_from_PDF(pdf_path)
        self.subjects = list(tup[0])
        self.subject_widgets = []
        self.teachers = list(tup[2])
        self.teacher_widgets = []
        self.rooms = list(tup[1])
        self.room_widgets = []

        # total_classes = len(classes)
        # no_courses = len(self.subjects)
        # slots = 6
        # total_days = 1
        # daily_repetition = 3
        # table = generate_timetable(total_classes, no_courses, slots, total_days, daily_repetition)
        # self.passedSubjects = []
        # for row in table.run():
        #     for col in row:
        #         self.passedSubjects.append(col)

        self.day_menu = ctk.StringVar(value="Monday")
        drop = ctk.CTkOptionMenu(master=self.app_frame, variable=self.day_menu,
                                 values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],command=self._on_day_select)
        drop.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

        self.Class_select = ctk.StringVar(value="Select Class to Export")
        drop = ctk.CTkOptionMenu(master=self.app_frame, variable=self.Class_select,
                                 values=classes)
        drop.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        text_var = tk.StringVar(value="Teachers and Rooms")
        label1 = ctk.CTkLabel(master=self.app_frame,textvariable=text_var,width=50,height=25,fg_color="transparent",text_color="#3A58FF",corner_radius=8,font=("Britannic Bold", 14))
        label1.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        subject_var = tk.StringVar(value="Subjects")
        label2 = ctk.CTkLabel(master=self.app_frame,textvariable=subject_var,width=50,height=25,fg_color="transparent",text_color="#3A58FF",corner_radius=8,font=("Britannic Bold", 14))
        label2.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        SaveButton = ctk.CTkButton(master=self.app_frame, text="Save", border_width=2, fg_color="#C7E8CA", hover_color="#C7FFCA",
                                      text_color="black", border_color="#5D9C59", command=self._save_day,
                                      height=28, width=100, font=('Arial Bold', 15), corner_radius=8)
        
        ValidateButton = ctk.CTkButton(master=self.app_frame, text="Validate", border_width=2, fg_color="#C7E8CA", hover_color="#C7FFCA",
                                      text_color="black", border_color="#5D9C59", command=self.on_button_validation,
                                      height=28, width=100, font=('Arial Bold', 15), corner_radius=8)
        ExportButton = ctk.CTkButton(master=self.app_frame, text="Export", border_width=2, fg_color="#C7E8CA",hover_color="#C7FFCA",
                                      text_color="black", border_color="#5D9C59", command=self.exportPDF,
                                      height=28, width=100, font=('Arial Bold', 15), corner_radius=8)
        '''ImportButton = ctk.CTkButton(master=self.app_frame, text="Import", border_width=2, fg_color="#C7E8CA",hover_color="#C7FFCA",
                                      text_color="black", border_color="#5D9C59",
                                      height=28, width=100, font=('Arial Bold', 15), corner_radius=8)'''
        for i, subject in enumerate(self.subjects):
            widget = ctk.CTkLabel(self.app_frame, text=subject, fg_color="#4bcffa", text_color="black", padx=10, pady=5,
                                  corner_radius=8, font=("Britannic Bold", 12))
            
            widget.grid(row=i + 3, column=1, sticky="ew", padx=2, pady=2)
            widget.bind("<Button-1>", self.on_subject_click)
            self.subject_widgets.append(widget)

        for i, teacher in enumerate(self.teachers):
            widget = ctk.CTkLabel(self.app_frame, text=teacher, fg_color="#B9E9FC", text_color="black", padx=10, pady=5,
                                  corner_radius=8, font=("Britannic Bold", 12))
            widget.grid(row=3+i, column=0, sticky="ew", padx=2, pady=2)
            widget.bind("<Button-1>", self.on_subject_click)
            self.teacher_widgets.append(widget)

        for i, room in enumerate(self.rooms):
            widget = ctk.CTkLabel(self.app_frame, text=room, fg_color="#95BDFF", text_color="black", padx=10, pady=5,
                                  corner_radius=8, font=("Britannic Bold", 12))
            widget.grid(row=i + len(self.teachers)  + 2, column=0, sticky="ew", padx=2, pady=2)
            widget.bind("<Button-1>", self.on_subject_click)
            self.room_widgets.append(widget)

        ValidateButton.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        SaveButton.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        ExportButton.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.subject_widgets.append(ValidateButton)

        for i, day in enumerate(classes):
            widget = ctk.CTkLabel(self.app_frame, text=day, fg_color="#3A98B9", padx=10, pady=5, corner_radius=8,
                                  text_color="white", font=("Britannic Bold", 14))
            widget.grid(row=0, column=i + 4, sticky="ew", padx=5, pady=5)

        
        for i, section in enumerate(timings):
            widget = ctk.CTkLabel(self.app_frame, text=section, fg_color="#3A98B9", padx=10, pady=5, corner_radius=8,
                                  text_color="white", font=("Britannic Bold", 14))
            widget.grid(row=3 * i + 2, column=2, sticky="ew", padx=5, pady=5)

        self.table = {}
        for row in range(int(len(timings))):
            table_row = []
            for col in range(int(len(classes))):
                widget = MyWidget([3 * row + 1, col + 4], subject="",teacher="",room="", master=self.app_frame,)
                widget.grid(row=3 * row + 1, column=col + 4,
                            sticky="nsew", padx=5, pady=5, rowspan=3)
                widget.setdrop(self, master=self.app_frame)
                widget.bind("<Button-1>", self.on_cell_click)
                table_row.append(widget)
            self.table[row + 1] = table_row

    def _clear_grid(self):
        for row in range(int(len(timings))):
            for col in range(int(len(classes))):
                widget = self.app_frame.grid_slaves(row=3 * row + 1, column=col + 4)[0]
                widget.clear()
       
    def _on_mousewheel(self, event):
         self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_subject_click(self, event):
        subject = event.widget.cget("text")
        event.widget.configure(bg="white")
        self.dragged_subject = subject

    def on_cell_click(self, event):
        row = event.widget.master.grid_info()["row"]
        col = event.widget.master.grid_info()["column"]
        if not hasattr(self, "dragged_subject"):
            self.table[math.ceil(row / 3)][col - 4].myconfigure(value="", coord=[row, col])
            return
        if (row % 3 == 1 and self.dragged_subject not in self.subjects):
            return
        if (row % 3 == 2 and self.dragged_subject not in self.teachers):
            return
        if (row % 3 == 0 and self.dragged_subject not in self.rooms):
            return
        self.table[math.ceil(row / 3)][col - 4].myconfigure(value=self.dragged_subject, coord=[row, col])
        delattr(self, "dragged_subject")

    def on_button_validation(self):
        clash = accumulate_cells(self.table)
        invalidCells = validation_algorithm(clash)

        for r in self.table:
            for widget in self.table[r]:
                widget.resetColor()

        for r in invalidCells:
            for c in r[1]:
                self.table[r[0]][c].showErrorCell()

    def _save_day(self):
        try:
            day = str(self.day_menu.get())
            if day=='Select Day':
                messagebox.showinfo("Alert", "ERROR: Please select day to save")
                return
            collection = connect_to_db()
            table = []
            for row in range(1,len(self.table)+1):
                table_row = []
                for column in range(len(self.table[row])):
                    table_row.append(str(self.table[row][column].label1._text))
                    table_row.append(str(self.table[row][column].label2._text))
                    table_row.append(str(self.table[row][column].label3._text))
                table.append(table_row)
            tt_data = {
                'session_id':session_id,
                'day':day,
                'data':table
            }
            collection.replace_one({'session_id':session_id,'day':day},tt_data,upsert=True)
            messagebox.showinfo("Alert", f"Data for {day} saved successfully")
        except Exception:
            return

    def _on_day_select(self,value):
        self._clear_grid()
        self.table = {}
        collection = connect_to_db()
        data = collection.find_one({'session_id':session_id,'day':value})
        if data and 'data' in data:
            for row in range(int(len(timings))):
                table_row = []
                data_col = 0
                for col in range(int(len(classes))):
                    widget = MyWidget([3 * row + 1, col + 4], subject = data['data'][row][data_col],teacher=data['data'][row][data_col+1],room=data['data'][row][data_col+2], master=self.app_frame)
                    data_col +=3
                    widget.grid(row=3 * row + 1, column=col + 4,
                                sticky="nsew", padx=5, pady=5, rowspan=3)
                    widget.setdrop(self, master=self.app_frame)
                    widget.bind("<Button-1>", self.on_cell_click)
                    table_row.append(widget)
                self.table[row + 1] = table_row
        else:
            for row in range(int(len(timings))):
                table_row = []
                for col in range(int(len(classes))):
                    widget = MyWidget([3 * row + 1, col + 4], subject="",teacher="",room="", master=self.app_frame)
                    widget.grid(row=3 * row + 1, column=col + 4,
                                sticky="nsew", padx=5, pady=5, rowspan=3)
                    widget.setdrop(self, master=self.app_frame)
                    widget.bind("<Button-1>", self.on_cell_click)
                    table_row.append(widget)
                self.table[row + 1] = table_row
                
    def exportPDF(self):
        try:
            class_name=str(self.Class_select.get())
            day = str(self.day_menu.get())
            column=classes.index(class_name)
            result = make_pdf(class_name,column,timings,session_id)
            if result:
                messagebox.showinfo("Alert", "The timetable document has been generated, kindly check the outputs folder.")
            else:
                messagebox.showinfo("Alert", "ERROR: The timetable document could not be generated. Please select class and day")
        except Exception:
            messagebox.showinfo("Alert", "ERROR: The timetable document could not be generated. Please select class and day")

    def run(self):
        self.master.mainloop()

if __name__=="__main__":
    root = ctk.CTk()
    global session_id
    session_id = make_id(24)
    app = TimetableApp(root)
    width= root.winfo_screenwidth()
    height= root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    root.title("ClashFree")
    app.run()

