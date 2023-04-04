from matplotlib import pyplot as plt


def draw_4_functions_on_one_plot(data):
    # draw all functions on one plot
    for name, times in data.items():
        x = [time[0] for time in times]
        y = [time[1] for time in times]
        plt.plot(x, y)
        plt.xlabel('Amount of words searched')
        plt.ylabel('Time(s)')
    plt.legend(data)
    plt.title('All algorithms')


def plotter(data):
    draw_4_functions_on_one_plot(data)
    plt.savefig('all_in_one'+'.jpg', format='jpg', dpi=200)
    plt.show()

    # plot_4_functions(data)
    # figure = plt.gcf()
    # figure.set_size_inches(10, 7)
    # plt.savefig("all_functions.jpg", format='jpg', dpi=200)
    # plt.show()

    # draw_separately(data)
    # plt.show()


# def plot_4_functions(data):
#     # draw all functions on separate plots but on one 'sheet'
#     figure, axis = plt.subplots(2, 2)
#     iter = 0
#     indexes = [(0, 0), (0, 1), (1, 0), (1, 1)]
#     for name, times in data.items():
#         if name == 'sorted':
#             continue
#         row, col = indexes[iter]
#         x = [time[0] for time in times]
#         y = [time[1] for time in times]
#         axis[row, col].plot(x, y)
#         axis[row, col].set_title(name, loc='left')
#         iter += 1


# def draw_separately(data):
#     # draw each function on separate plot
#     for name, times in data.items():
#         plt.figure()
#         x = [time[0] for time in times]
#         y = [time[1] for time in times]
#         plt.plot(x, y)
#         plt.xlabel('Words sorted')
#         plt.ylabel('Time(s)')
#         plt.title(name)
#         plt.savefig(name+'.jpg', format='jpg', dpi=200)
