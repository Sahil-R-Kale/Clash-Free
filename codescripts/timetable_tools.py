from genetictabler import GenerateTimeTable

def accumulate_cells(table):  # Accumulating Cells Data into timetableCells
    timetableCells = table
    # Filling the clash dictionary
    clash = {}
    for r in range(1, len(timetableCells) + 1):
        clash[r] = {}

    for r in range(1, len(timetableCells) + 1):  # Slot-wise saving in the dictionary
        for c in range(len(timetableCells[r])):
            w = timetableCells[r][c]
            teacherName = str(w.getTeacherName())
            roomNumber = str(w.getRoomNumber())

            # Keep resource types separate: a teacher and a room can have the
            # same label without representing a clash.
            for resource_type, resource_name in (("teacher", teacherName), ("room", roomNumber)):
                if resource_name:
                    resource_key = (resource_type, resource_name)
                    clash[r].setdefault(resource_key, []).append(c)

    return clash


def validation_algorithm(clash):
    invalidCells = []
    for r in range(1, len(clash) + 1):
        for c in clash[r]:
            if len(clash[r][c]) > 1:
                invalidCells.append([r, clash[r][c]])
    return invalidCells

def generate_timetable(total_classes, no_courses, slots, total_days, daily_repetition):
    return GenerateTimeTable(total_classes, no_courses, slots, total_days, daily_repetition)

