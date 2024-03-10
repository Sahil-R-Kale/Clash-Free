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

            if teacherName not in clash[r]:
                if (teacherName != ""):
                    clash[r][teacherName] = [c]
            else:
                if (teacherName != ""):
                    clash[r][teacherName].append(c)

            if roomNumber not in clash[r]:
                if (roomNumber != ""):
                    clash[r][roomNumber] = [c]
            else:
                if (roomNumber != ""):
                    clash[r][roomNumber].append(c)

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

